"""Runtime bootstrap checks with generated keys and isolated fake services."""

from contextlib import contextmanager
import base64

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from psycopg.pq import TransactionStatus

import app.runtime as runtime


def settings_env(*, db_host="127.0.0.1", redis_host="127.0.0.1", other_key=False):
    private = Ed25519PrivateKey.generate()
    other = Ed25519PrivateKey.generate()
    private_bytes = private.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    public = (other if other_key else private).public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    encode = lambda value: base64.b64encode(value).decode("ascii")
    return {
        "MERLIN_DATABASE_DSN": f"postgresql://merlin_api:synthetic@{db_host}:5432/merlin_db",
        "MERLIN_REDIS_URL": f"redis://{redis_host}:6379/0",
        "MERLIN_AUTH_SIGNING_KEY_B64": encode(private_bytes),
        "MERLIN_AUTH_VERIFICATION_KEY_B64": encode(public),
        "MERLIN_RATE_LIMIT_KEY_B64": encode(b"r" * 32),
    }


def test_runtime_accepts_matching_local_keys_and_fixed_loopback_services():
    result = runtime.load_runtime_settings(settings_env())
    assert result.database_dsn.startswith("postgresql://merlin_api:")
    assert result.redis_url.startswith("redis://127.0.0.1:")
    assert len(result.rate_limit_key) == 32
    assert "synthetic" not in repr(result)


@pytest.mark.parametrize("name", [
    "MERLIN_DATABASE_DSN", "MERLIN_REDIS_URL", "MERLIN_AUTH_SIGNING_KEY_B64",
    "MERLIN_AUTH_VERIFICATION_KEY_B64", "MERLIN_RATE_LIMIT_KEY_B64",
])
def test_runtime_requires_each_setting_without_echoing_values(name):
    environment = settings_env()
    sentinel = "synthetic-private-sentinel"
    environment[name] = sentinel
    del environment[name]
    with pytest.raises(runtime.RuntimeBootstrapError) as error:
        runtime.load_runtime_settings(environment)
    assert sentinel not in str(error.value)


@pytest.mark.parametrize("environment", [
    settings_env(db_host="database.example.invalid"),
    settings_env(db_host="localhost"),
    settings_env(redis_host="cache.example.invalid"),
    settings_env(redis_host="localhost"),
    settings_env(other_key=True),
])
def test_runtime_rejects_remote_services_and_mismatched_signing_pair(environment):
    with pytest.raises(runtime.RuntimeBootstrapError):
        runtime.load_runtime_settings(environment)


def test_runtime_rejects_non_loopback_database_address():
    environment = settings_env(db_host="database.example.invalid")
    with pytest.raises(runtime.RuntimeBootstrapError):
        runtime.load_runtime_settings(environment)


def test_runtime_rejects_remote_database_hostaddr():
    environment = settings_env()
    environment["MERLIN_DATABASE_DSN"] += "?hostaddr=203.0.113.10"
    with pytest.raises(runtime.RuntimeBootstrapError):
        runtime.load_runtime_settings(environment)


def test_runtime_rejects_short_rate_limit_key_and_malformed_key_without_leak():
    environment = settings_env()
    environment["MERLIN_RATE_LIMIT_KEY_B64"] = base64.b64encode(b"short").decode("ascii")
    with pytest.raises(runtime.RuntimeBootstrapError, match="^Authentication runtime configuration is invalid$"):
        runtime.load_runtime_settings(environment)
    environment = settings_env()
    sentinel = "SYNTHETIC_INVALID_KEY_SENTINEL"
    environment["MERLIN_AUTH_SIGNING_KEY_B64"] = base64.b64encode(sentinel.encode()).decode()
    with pytest.raises(runtime.RuntimeBootstrapError) as error:
        runtime.load_runtime_settings(environment)
    assert sentinel not in str(error.value)


class FakeConnection:
    def __init__(self, row):
        self.info = type("Info", (), {"transaction_status": TransactionStatus.IDLE})()
        self.row = row
        self.query = None

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    @contextmanager
    def cursor(self):
        yield self

    def execute(self, query):
        self.query = query

    def fetchone(self):
        return self.row


SAFE_ROLE = (True, True, False, False, False, False, False, False, True, True, True)


@pytest.mark.parametrize("row", [
    (False, *SAFE_ROLE[1:]),
    (True, False, True, *SAFE_ROLE[3:]),
    (True, True, True, *SAFE_ROLE[3:]),
    (True, True, True, False, False, False, False, True, True, True, True),
    (True, True, True, False, False, False, False, False, False, True, True),
])
def test_runtime_database_gate_rejects_wrong_identity_or_privilege(row):
    connection = FakeConnection(row)
    with pytest.raises(runtime.RuntimeBootstrapError, match="^Authentication database role is not ready$"):
        runtime.verify_runtime_database(lambda: connection)
    assert "pg_has_role" in connection.query


def test_runtime_database_gate_accepts_only_restricted_auth_login():
    connection = FakeConnection(SAFE_ROLE)
    runtime.verify_runtime_database(lambda: connection)
    assert "current_user = 'merlin_api'" in connection.query
    assert "role.rolbypassrls" in connection.query


def test_runtime_database_gate_rejects_missing_credential_lookup():
    missing_lookup = (*SAFE_ROLE[:9], False, SAFE_ROLE[10])
    with pytest.raises(runtime.RuntimeBootstrapError, match="^Authentication database role is not ready$"):
        runtime.verify_runtime_database(lambda: FakeConnection(missing_lookup))


def test_runtime_database_gate_rejects_missing_refresh_schema():
    missing_refresh_schema = (*SAFE_ROLE[:10], False)
    with pytest.raises(runtime.RuntimeBootstrapError, match="^Authentication database role is not ready$"):
        runtime.verify_runtime_database(lambda: FakeConnection(missing_refresh_schema))


def test_runtime_database_gate_rejects_notes_role_membership():
    notes_role_member = (*SAFE_ROLE[:8], False, *SAFE_ROLE[9:])
    connection = FakeConnection(notes_role_member)
    with pytest.raises(runtime.RuntimeBootstrapError, match="^Authentication database role is not ready$"):
        runtime.verify_runtime_database(lambda: connection)
    assert connection.query.count("NOT pg_has_role(") == 1


def test_runtime_database_failure_suppresses_private_driver_detail():
    sentinel = "SYNTHETIC_DATABASE_SENTINEL"

    def unavailable():
        raise OSError(sentinel)

    with pytest.raises(runtime.RuntimeBootstrapError) as error:
        runtime.verify_runtime_database(unavailable)
    assert str(error.value) == "Authentication database is not ready"
    assert error.value.__cause__ is None


def test_runtime_factory_uses_bounded_connections_and_injected_dependencies(monkeypatch):
    environment = runtime.load_runtime_settings(settings_env())
    observed = {}
    connection = FakeConnection(SAFE_ROLE)

    def connect_factory(dsn, **options):
        observed["dsn"] = dsn
        observed["connect_options"] = options
        return connection

    class FakeRedis:
        pass

    def redis_factory(url, **options):
        observed["redis_url"] = url
        observed["redis_options"] = options
        return FakeRedis()

    monkeypatch.setattr(runtime, "create_api_app", lambda **kwargs: kwargs)
    app = runtime.create_runtime_app(
        environment,
        connect_factory=connect_factory,
        redis_factory=redis_factory,
    )
    assert observed["connect_options"] == {"connect_timeout": 3, "application_name": "merlin-auth-api"}
    assert observed["redis_options"] == {"socket_connect_timeout": 1, "socket_timeout": 1}
    assert app["store"]._connect is not None
    assert app["rate_limiter"]._redis is not None


def test_runtime_factory_refuses_database_with_bypass_privilege(monkeypatch):
    environment = runtime.load_runtime_settings(settings_env())
    unsafe_role = (True, True, True, True, False, False, False, True, True, True, True)
    connection = FakeConnection(unsafe_role)
    monkeypatch.setattr(runtime, "create_api_app", lambda **kwargs: kwargs)
    with pytest.raises(runtime.RuntimeBootstrapError):
        runtime.create_runtime_app(
            environment,
            connect_factory=lambda *_args, **_kwargs: connection,
            redis_factory=lambda *_args, **_kwargs: object(),
        )


def test_regular_server_bootstrap_uses_loopback_and_disables_proxy_trust(monkeypatch):
    called = {}
    monkeypatch.setattr(runtime, "load_runtime_settings", lambda _environment: object())
    monkeypatch.setattr(runtime, "create_runtime_app", lambda _settings: object())
    monkeypatch.setattr(runtime.os, "environ", {})
    monkeypatch.setattr("uvicorn.run", lambda app, **kwargs: called.update(app=app, **kwargs))
    runtime.main()
    assert called["host"] == "127.0.0.1"
    assert called["port"] == 8000
    assert called["proxy_headers"] is False


def test_regular_server_startup_error_is_fixed_and_suppresses_cause(monkeypatch, capsys):
    sentinel = "SYNTHETIC_STARTUP_SENTINEL"

    def fail(_environment):
        raise runtime.RuntimeBootstrapError(sentinel)

    monkeypatch.setattr(runtime, "load_runtime_settings", fail)
    with pytest.raises(SystemExit) as error:
        runtime.main()
    assert str(error.value) == "Authentication runtime could not start"
    assert error.value.__cause__ is None
    assert error.value.__suppress_context__ is True
    assert sentinel not in capsys.readouterr().out


def test_health_server_module_entrypoint_dispatches_to_runtime(monkeypatch):
    import runpy

    called = []
    monkeypatch.setattr(runtime, "main", lambda: called.append("runtime"))
    runpy.run_module("app.health_server", run_name="__main__")
    assert called == ["runtime"]
