"""The setup checker must reject bad evidence without exposing command output."""

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from tools import doctor


def result(code=0, out="", err=""):
    return subprocess.CompletedProcess([], code, out, err)


@pytest.mark.parametrize("host,mounts,labels", [([], [], {}), ({}, None, {}), ({}, [], [])],
                         ids=["host-is-array", "mounts-are-null", "labels-are-array"])
def test_typed_malformed_inspect_data_is_rejected(host, mounts, labels):
    instance = doctor.Doctor(Path("/tmp"))
    payload = "|".join(json.dumps(value) for value in ["healthy", host, mounts, labels])
    with patch.object(instance, "command", return_value=result(out=payload)):
        assert instance.inspect("a" * 64) is None


def test_valid_inspection_is_preserved():
    instance = doctor.Doctor(Path("/tmp"))
    values = ["healthy", {"Memory": 1073741824}, [], {"com.docker.compose.project": "clone42"}]
    payload = "|".join(json.dumps(value) for value in values)
    with patch.object(instance, "command", return_value=result(out=payload)):
        assert instance.inspect("a" * 64) == tuple(values)


@pytest.mark.parametrize("host", [
    {"PortBindings": None}, {"PortBindings": []},
    {"PortBindings": {"5432/tcp": [None]}},
    {"PortBindings": {"5432/tcp": "secret"}},
    {"LogConfig": None}, {"LogConfig": []},
    {"LogConfig": {"Config": None}}, {"LogConfig": {"Config": []}},
], ids=["ports-null", "ports-array", "binding-null", "binding-string",
        "log-null", "log-array", "log-options-null", "log-options-array"])
def test_nested_malformed_inspection_is_rejected(host):
    instance = doctor.Doctor(Path("/tmp"))
    payload = "|".join(json.dumps(value) for value in ["healthy", host, [], {}])
    with patch.object(instance, "command", return_value=result(out=payload)):
        assert instance.inspect("a" * 64) is None


@pytest.mark.parametrize("positive", [result(2, err="connection failed"), result(0, "2")],
                         ids=["positive-connection-fails", "positive-output-is-wrong"])
def test_negative_auth_cannot_pass_without_a_valid_positive(positive, capsys):
    instance = doctor.Doctor(Path("/tmp"))
    with patch.object(instance, "compose", side_effect=[positive,
         result(2, err="password authentication failed"), result(0, "456")]):
        instance.postgres_checks()
    output = capsys.readouterr().out
    assert "PG-AUTH-POSITIVE FAIL" in output
    assert "PG-AUTH-NEGATIVE FAIL" in output
    assert instance.failures == 2


@pytest.mark.parametrize("observed,expected,passes", [("456", "456", True), ("456", "123", False),
                                                    ("not-a-cluster", None, False)])
def test_cluster_comparison_uses_the_expected_fingerprint(observed, expected, passes, capsys):
    instance = doctor.Doctor(Path("/tmp"), expect_cluster=expected)
    with patch.object(instance, "compose", side_effect=[result(0, "1"),
         result(2, err="password authentication failed"), result(0, observed)]):
        instance.postgres_checks()
    output = capsys.readouterr().out
    assert "PG-CLUSTER " + ("PASS" if passes else "FAIL") in output
    assert instance.failures == (0 if passes else 1)
    if not observed.isdigit():
        assert observed not in output


def test_auth_commands_use_tcp_and_different_passwords(capsys):
    instance = doctor.Doctor(Path("/tmp"))
    with patch.object(instance, "compose", side_effect=[result(0, "1"),
         result(2, err="password authentication failed"), result(0, "456")]) as compose:
        instance.postgres_checks()
    positive, negative, identity = [item.args[-1] for item in compose.call_args_list]
    for command in [positive, negative, identity]:
        assert '-h postgres' in command and '-X -w' in command
        assert '-U "$POSTGRES_USER"' in command and '-d "$POSTGRES_DB"' in command
    assert 'PGPASSWORD="$POSTGRES_PASSWORD"' in positive
    assert 'PGPASSWORD="${POSTGRES_PASSWORD}__doctor_wrong"' in negative
    assert positive.endswith("'SELECT 1'") and negative.endswith("'SELECT 1'")
    assert identity.endswith("'SELECT system_identifier FROM pg_control_system()'")
    assert instance.failures == 0


@pytest.mark.parametrize("fault,expected", [
    ("python-version", "PYTHON"), ("python-pin", "PYTHON-PIN"),
    ("lock-missing", "LOCKFILES"), ("lock-stale", "UV-LOCK"),
    ("node-version", "NODE"), ("pnpm-version", "PNPM"),
    ("env-public", "ENV-MODE"), ("env-not-ignored", "ENV-IGNORE"),
    ("env-tracked", "TRACKED-SECRETS"), ("env-variant-tracked", "TRACKED-SECRETS"),
    ("git-list-failed", "TRACKED-SECRETS"), ("venv-tracked", "VENV-IGNORE"),
    ("compose-invalid", "COMPOSE-CONFIG"),
    ("compose-invalid-static", "COMPOSE-CONFIG"),
])
def test_static_checker_rejects_each_bad_prerequisite(tmp_path, fault, expected, capsys):
    (tmp_path / "pyproject.toml").write_text('[project]\nrequires-python=">=3.12,<3.13"\n')
    for file in ["uv.lock", "pnpm-lock.yaml", ".env"]:
        (tmp_path / file).touch()
    (tmp_path / ".env").chmod(0o644 if fault == "env-public" else 0o600)
    if fault == "python-pin":
        (tmp_path / "pyproject.toml").write_text('[project]\nrequires-python=">=3.12"\n')
    if fault == "lock-missing":
        (tmp_path / "uv.lock").unlink()
    def command(args):
        if args == ["uv", "lock", "--check", "--offline"]:
            return result(1 if fault == "lock-stale" else 0)
        if args[-1] == "--version":
            major = {"node": 24, "pnpm": 12}[args[0]]
            return result(out=f"{major-1 if fault == args[0]+'-version' else major}.0.0")
        if args[:2] == ["git", "ls-files"]:
            return result(1 if fault == "git-list-failed" else 0,
                          ".env\0" if fault == "env-tracked" else
                          "nested/.env.production\0" if fault == "env-variant-tracked" else ".env.example\0")
        if args[:2] == ["git", "check-ignore"]:
            return result(1 if (args[-1] == ".env" and fault == "env-not-ignored") or
                          (args[-1] == ".venv/probe" and fault == "venv-tracked") else 0)
        if args == ["docker", "compose", "config", "--quiet"]:
            return result(1 if fault.startswith("compose-invalid") else 0)
        assert args == ["docker", "compose", "version"]
        return result()
    instance = doctor.Doctor(tmp_path, static=fault.endswith("-static"))
    with patch.object(instance, "command", side_effect=command), patch("tools.doctor.shutil.which", return_value="/client"), \
         patch("tools.doctor.sys.version_info", (3,11) if fault == "python-version" else (3,12)):
        assert instance.static_checks() is True
    lines = capsys.readouterr().out.splitlines()
    assert [line.split()[0] for line in lines if " FAIL:" in line] == [expected]
    assert instance.failures == 1


@pytest.mark.parametrize("manifest", ['project=[]', '[project]\nrequires-python=[]', '[project]\n'])
def test_malformed_manifest_is_reported_without_crashing(tmp_path, manifest, capsys):
    (tmp_path / "pyproject.toml").write_text(manifest)
    instance = doctor.Doctor(tmp_path, static=True)
    with patch.object(instance, "command", return_value=result(1)), patch("tools.doctor.shutil.which", return_value=None):
        instance.static_checks()
    assert "PYTHON-PIN FAIL" in capsys.readouterr().out


@pytest.mark.parametrize("fault,expected", [
    ("public-port", "PORT"), ("two-ports", "PORT"), ("zero-port", "PORT"),
    ("huge-port", "PORT"), ("unicode-digit-port", "PORT"),
    ("memory", "LIMITS"), ("cpu", "LIMITS"), ("log-type", "LOGS"),
    ("log-size", "LOGS"), ("log-count", "LOGS"), ("volume-name", "VOLUME"),
    ("volume-type", "VOLUME"), ("volume-missing", "VOLUME"),
    ("volume-duplicate", "VOLUME"), ("project-missing", "VOLUME"),
    ("unhealthy", "HEALTH"), ("uid-root", "UID"),
])
def test_runtime_checker_rejects_each_bad_postgres_boundary(fault, expected, capsys):
    instance = doctor.Doctor(Path("/tmp"))
    host = {"Memory":1073741824,"NanoCpus":1000000000,
            "PortBindings":{"5432/tcp":[{"HostIp":"127.0.0.1","HostPort":"55432"}]},
            "LogConfig":{"Type":"json-file","Config":{"max-size":"10m","max-file":"3"}}}
    mounts = [{"Destination":"/var/lib/postgresql/data","Type":"volume","Name":"audit_postgres_data"}]
    labels = {"com.docker.compose.project":"audit"}
    binding = host["PortBindings"]["5432/tcp"][0]
    if fault == "public-port": binding["HostIp"] = "0.0.0.0"
    if fault == "two-ports": host["PortBindings"]["5432/tcp"].append(dict(binding))
    if fault == "zero-port": binding["HostPort"] = "0"
    if fault == "huge-port": binding["HostPort"] = "65536"
    if fault == "unicode-digit-port": binding["HostPort"] = "²"
    if fault == "memory": host["Memory"] = 0
    if fault == "cpu": host["NanoCpus"] = 0
    if fault == "log-type": host["LogConfig"]["Type"] = "none"
    if fault == "log-size": host["LogConfig"]["Config"]["max-size"] = "1g"
    if fault == "log-count": host["LogConfig"]["Config"]["max-file"] = "100"
    if fault == "volume-name": mounts[0]["Name"] = "other_postgres_data"
    if fault == "volume-type": mounts[0]["Type"] = "bind"
    if fault == "volume-missing": mounts = []
    if fault == "volume-duplicate": mounts.append(dict(mounts[0]))
    if fault == "project-missing": labels = {}
    def compose(*args):
        if args[:2] == ("ps","-q"):
            return result(out="a"*64 if args[-1] == "postgres" else "")
        if args[-1].startswith("awk"):
            return result(out="0" if fault == "uid-root" else "999")
        if args[-1] == "ping": return result(out="PONG")
        values = {"save":"","appendonly":"no","maxmemory":"134217728","maxmemory-policy":"noeviction"}
        return result(out=args[-1]+"\n"+values[args[-1]]+"\n")
    payload = "|".join(json.dumps(value) for value in ["starting" if fault == "unhealthy" else "healthy",host,mounts,labels])
    with patch.object(instance,"compose",side_effect=compose), patch.object(instance,"command",return_value=result(out=payload)), \
         patch.object(instance,"postgres_checks"), patch.object(instance,"host_checks"):
        instance.runtime_checks()
    assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if " FAIL:" in line] == ["POSTGRES-"+expected,"REDIS-RUNNING"]
    if expected == "PORT": assert "postgres" not in instance.host_ports


@pytest.mark.parametrize("fault", ["positive-status","positive-output","credential-status","credential-count",
    "credential-empty","pg-client-missing","pg-port-missing","redis-client-missing","redis-port-missing",
    "redis-status","redis-output","healthy"])
def test_host_proof_requires_valid_credentials_clients_and_responses(fault, capsys):
    instance = doctor.Doctor(Path("/tmp"))
    instance.host_ports={"postgres":"55432","redis":"56379"}
    if fault == "pg-port-missing": del instance.host_ports["postgres"]
    if fault == "redis-port-missing": del instance.host_ports["redis"]
    def which(tool):
        return None if (tool == "psql" and fault == "pg-client-missing") or (tool == "redis-cli" and fault == "redis-client-missing") else "/client"
    credential = result(1 if fault == "credential-status" else 0,
                        "user" if fault == "credential-count" else "user\0db\0" if fault == "credential-empty" else "user\0db\0secret")
    def run(args, *_):
        assert args[args.index("-h")+1] == "127.0.0.1"
        assert args[args.index("-p")+1] in {"55432","56379"}
        if args[0] == "redis-cli": return result(1 if fault == "redis-status" else 0,"NO" if fault == "redis-output" else "PONG")
        environment = _[1]
        if environment["PGPASSWORD"].endswith("__doctor_wrong"):
            return result(2,err="password authentication failed secret")
        return result(1 if fault == "positive-status" else 0,"2" if fault == "positive-output" else "1")
    with patch("tools.doctor.shutil.which",side_effect=which), patch.object(instance,"compose",return_value=credential), \
         patch("tools.doctor.run",side_effect=run) as called:
        instance.host_checks()
    lines = capsys.readouterr().out
    pg_ok = fault not in {"positive-status","positive-output","credential-status","credential-count","credential-empty","pg-client-missing","pg-port-missing"}
    redis_ok = fault not in {"redis-client-missing","redis-port-missing","redis-status","redis-output"}
    assert "HOST-PG-POSITIVE "+("PASS" if pg_ok else "FAIL") in lines
    assert "HOST-REDIS-PONG "+("PASS" if redis_ok else "FAIL") in lines
    assert "secret" not in lines
    pg_calls = [call for call in called.call_args_list if call.args[0][0] == "psql"]
    assert len(pg_calls) == (2 if pg_ok or fault in {"positive-status","positive-output"} else 0)


@pytest.mark.parametrize("fault", ["ping-output","ping-status","save","appendonly","maxmemory","maxmemory-policy"])
def test_redis_runtime_proof_rejects_bad_responses_and_configuration(fault, capsys):
    instance = doctor.Doctor(Path("/tmp"))
    def compose(*args):
        if args[:2] == ("ps","-q"): return result(out="")
        if args[-1] == "ping": return result(1 if fault == "ping-status" else 0,"NO" if fault == "ping-output" else "PONG")
        values={"save":"","appendonly":"no","maxmemory":"134217728","maxmemory-policy":"noeviction"}
        return result(out=args[-1]+"\n"+("wrong" if fault == args[-1] else values[args[-1]])+"\n")
    with patch.object(instance,"compose",side_effect=compose),patch.object(instance,"postgres_checks"),patch.object(instance,"host_checks"):
        instance.runtime_checks()
    expected="REDIS-PONG" if fault.startswith("ping-") else "REDIS-"+fault.upper()
    assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if " FAIL:" in line] == ["POSTGRES-RUNNING","REDIS-RUNNING",expected]
