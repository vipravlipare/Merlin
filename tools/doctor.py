#!/usr/bin/env python3
"""Read-only setup checks. Captured command output is never printed verbatim."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str], root: Path = ROOT, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """Keep stdout/stderr private, including errors containing credentials."""
    try:
        return subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=30,
                              check=False, env=env)
    except (OSError, subprocess.TimeoutExpired):
        return subprocess.CompletedProcess(args, 127, '', '')


class Doctor:
    def __init__(self, root: Path, static: bool = False, expect_cluster: str | None = None):
        self.root, self.static, self.expect_cluster = root, static, expect_cluster
        self.failures = 0
        self.host_ports: dict[str, str] = {}

    def report(self, ident: str, ok: bool, reason: str, fix: str, warn: bool = False):
        status = 'PASS' if ok else 'WARN' if warn else 'FAIL'
        self.failures += int(status == 'FAIL')
        print(f'{ident} {status}: {reason}' + (f'; first fix: {fix}' if not ok else ''))

    def command(self, args: list[str]):
        return run(args, self.root)

    def compose(self, *args: str):
        return self.command(['docker', 'compose', *args])

    def static_checks(self):
        self.report('PYTHON', (3, 12) <= sys.version_info[:2] < (3, 13),
                    'Python 3.12 interpreter required', 'run uv run --locked python tools/doctor.py')
        try:
            data = tomllib.loads((self.root / 'pyproject.toml').read_text())
            declared = data['project']['requires-python']
            python_ok = declared in ('>=3.12,<3.13', '>=3.12, <3.13', '==3.12.*')
            empty = not data['project'].get('dependencies', [])
        except (OSError, ValueError, KeyError):
            python_ok, empty = False, False
        self.report('PYTHON-PIN', python_ok, 'project declares Python 3.12 only', 'correct requires-python')
        self.report('LOCKFILES', all((self.root / p).is_file() for p in ('uv.lock', 'pnpm-lock.yaml')),
                    'Python and JavaScript lockfiles present', 'restore committed lockfiles')
        if shutil.which('uv'):
            result = self.command(['uv', 'lock', '--check', '--offline'])
            self.report('UV-LOCK', result.returncode == 0, 'offline lock consistency checked', 'run uv lock and review changes')
        else:
            self.report('UV-LOCK', False, 'uv unavailable', 'install pinned uv', warn=self.static)
        self.report('APP-TESTS', False, 'application tests N/A: no application dependencies or features verified',
                    'define application test scope before claiming feature verification', warn=True)
        for tool, major in (('node', 24), ('pnpm', 12)):
            result = self.command([tool, '--version'])
            match = re.fullmatch(r'v?(\d+)\.\d+\.\d+\s*', result.stdout)
            self.report(tool.upper(), result.returncode == 0 and bool(match) and int(match[1]) == major,
                        f'{tool} major version {major} required', f'install planned {tool} version', warn=self.static)
        for client in ('psql', 'redis-cli'):
            self.report('HOST-' + client.upper(), bool(shutil.which(client)),
                        'native host client available', 'install host client from SETUP.md', warn=self.static)
        env = self.root / '.env'
        self.report('ENV-EXISTS', env.is_file(), 'local environment file present', 'copy .env.example and set local values', warn=self.static)
        if env.is_file():
            self.report('ENV-MODE', env.stat().st_mode & 0o077 == 0, 'environment file private', 'chmod 600 .env')
        ignored = self.command(['git', 'check-ignore', '-q', '.env'])
        self.report('ENV-IGNORE', ignored.returncode == 0, 'environment file ignored', 'add .env to .gitignore')
        tracked = self.command(['git', 'ls-files', '-z'])
        secrets = [p for p in tracked.stdout.split('\0') if Path(p).name == '.env' or
                   (Path(p).name.startswith('.env.') and Path(p).name != '.env.example')]
        self.report('TRACKED-SECRETS', tracked.returncode == 0 and not secrets,
                    'no environment secret files tracked', 'untrack secret files and rotate exposed credentials')
        ignored_venv = self.command(['git', 'check-ignore', '-q', '.venv/probe'])
        self.report('VENV-IGNORE', ignored_venv.returncode == 0, 'virtual environment ignored', 'add .venv/ to .gitignore')
        available = self.compose('version')
        self.report('COMPOSE', available.returncode == 0, 'Docker Compose available', 'install Docker Compose plugin', warn=self.static)
        if available.returncode == 0:
            config = self.compose('config', '--quiet')
            self.report('COMPOSE-CONFIG', config.returncode == 0, 'quiet Compose validation completed',
                        'check local environment and Compose syntax privately', warn=self.static and not env.is_file())
        return available.returncode == 0

    def inspect(self, container: str):
        # Never request Config.Env or a resolved Compose configuration.
        template = '{{json .State.Health.Status}}|{{json .HostConfig}}|{{json .Mounts}}|{{json .Config.Labels}}'
        result = self.command(['docker', 'inspect', '--format', template, container])
        if result.returncode:
            return None
        try:
            health, host, mounts, labels = [json.loads(part) for part in result.stdout.strip().split('|')]
            return health, host, mounts, labels
        except (ValueError, TypeError):
            return None

    def runtime_checks(self):
        for service, port, memory, cpus, destination in (
            ('postgres', '5432/tcp', 1073741824, 1000000000, '/var/lib/postgresql/data'),
            ('redis', '6379/tcp', 268435456, 500000000, '/data'),
        ):
            ids = self.compose('ps', '-q', service)
            container = ids.stdout.strip()
            info = self.inspect(container) if ids.returncode == 0 and re.fullmatch(r'[a-f0-9]{12,64}', container) else None
            prefix = service.upper()
            self.report(prefix + '-RUNNING', info is not None, 'service inspect available', 'start this project with docker compose up -d')
            if info is None:
                continue
            health, host, mounts, labels = info
            self.report(prefix + '-HEALTH', health == 'healthy', 'service healthy', 'inspect service health privately')
            bindings = host.get('PortBindings', {}).get(port) or []
            valid_port = len(bindings) == 1 and bindings[0].get('HostIp') == '127.0.0.1' and str(bindings[0].get('HostPort', '')).isdigit() and 0 < int(bindings[0]['HostPort']) <= 65535
            if valid_port:
                self.host_ports[service] = str(bindings[0]['HostPort'])
            self.report(prefix + '-PORT', len(bindings) == 1 and bindings[0].get('HostIp') == '127.0.0.1'
                        and str(bindings[0].get('HostPort', '')).isdigit() and 0 < int(bindings[0]['HostPort']) <= 65535,
                        'service port bound to loopback', 'use one 127.0.0.1 host port mapping')
            self.report(prefix + '-LIMITS', host.get('Memory') == memory and host.get('NanoCpus') == cpus,
                        'CPU and memory limits match budget', 'restore documented service limits')
            log = host.get('LogConfig', {})
            self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and log.get('Config', {}).get('max-size') == '10m'
                        and log.get('Config', {}).get('max-file') == '3', 'logs bounded', 'restore 10m / 3 log rotation')
            project = labels.get('com.docker.compose.project', '')
            matching = [m for m in mounts if m.get('Destination') == destination]
            self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and matching[0].get('Type') == 'volume'
                        and matching[0].get('Name') == f'{project}_{service}_data',
                        'project scoped named volume mounted', 'restore service named volume mount')
            uid = self.compose('exec', '-T', service, 'sh', '-c', "awk '/^Uid:/{print $2}' /proc/1/status")
            self.report(prefix + '-UID', uid.returncode == 0 and uid.stdout.strip() == '999',
                        'main process UID 999 and non-root', 'use documented image and non-root service process')
        self.postgres_checks()
        self.host_checks()
        pong = self.compose('exec', '-T', 'redis', 'redis-cli', 'ping')
        self.report('REDIS-PONG', pong.returncode == 0 and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service')
        for key, value in (('save', ''), ('appendonly', 'no'), ('maxmemory', '134217728'), ('maxmemory-policy', 'noeviction')):
            result = self.compose('exec', '-T', 'redis', 'redis-cli', '--raw', 'CONFIG', 'GET', key)
            self.report('REDIS-' + key.upper(), result.returncode == 0 and result.stdout.splitlines() == [key, value],
                        'Redis disposable cache policy matches', 'restore documented Redis command')

    def host_checks(self):
        pg_port = self.host_ports.get('postgres')
        if pg_port and shutil.which('psql'):
            credentials = self.compose('exec', '-T', 'postgres', 'sh', '-c',
                                       'printf "%s\\0%s\\0%s" "$POSTGRES_USER" "$POSTGRES_DB" "$POSTGRES_PASSWORD"')
            parts = credentials.stdout.split('\0')
            if credentials.returncode == 0 and len(parts) == 3 and all(parts):
                user, database, password = parts
                args = ['psql', '-X', '-w', '-h', '127.0.0.1', '-p', pg_port,
                        '-U', user, '-d', database, '-Atqc', 'SELECT 1']
                environment = dict(os.environ, PGPASSWORD=password, PGCONNECT_TIMEOUT='5')
                positive = run(args, self.root, environment)
                environment = dict(environment, PGPASSWORD=password + '__doctor_wrong')
                negative = run(args, self.root, environment)
                accepted = positive.returncode == 0 and positive.stdout.strip() == '1'
                rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()
                self.report('HOST-PG-POSITIVE', accepted, 'host TCP password accepted', 'check native psql and loopback mapping')
                self.report('HOST-PG-NEGATIVE', accepted and rejected, 'host TCP wrong password explicitly rejected',
                            'check PostgreSQL password authentication')
            else:
                self.report('HOST-PG-POSITIVE', False, 'private credential capture unavailable', 'check PostgreSQL environment privately')
        else:
            self.report('HOST-PG-POSITIVE', False, 'host PostgreSQL proof unavailable', 'install psql and check loopback mapping')
        redis_port = self.host_ports.get('redis')
        result = (run(['redis-cli', '-h', '127.0.0.1', '-p', redis_port, 'ping'], self.root)
                  if redis_port and shutil.which('redis-cli') else None)
        self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG',
                    'host Redis TCP responds PONG', 'install redis-cli and check loopback mapping')

    def postgres_checks(self):
        base = 'psql -X -w -h postgres -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atqc '
        positive = self.compose('exec', '-T', 'postgres', 'sh', '-c',
                                'PGPASSWORD="$POSTGRES_PASSWORD" ' + base + "'SELECT 1'")
        self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and positive.stdout.strip() == '1',
                    'configured password accepted over service TCP', 'check PostgreSQL credentials privately')
        negative = self.compose('exec', '-T', 'postgres', 'sh', '-c',
                                'PGPASSWORD="${POSTGRES_PASSWORD}__doctor_wrong" ' + base + "'SELECT 1'")
        # A generic connection failure is not proof of password rejection.
        rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()
        self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and positive.stdout.strip() == '1' and rejected,
                    'wrong password explicitly rejected over service TCP', 'configure password authentication and retry')
        cluster = self.compose('exec', '-T', 'postgres', 'sh', '-c',
                               'PGPASSWORD="$POSTGRES_PASSWORD" ' + base + "'SELECT system_identifier FROM pg_control_system()'")
        observed = cluster.stdout.strip()
        valid = cluster.returncode == 0 and bool(re.fullmatch(r'\d{1,20}', observed))
        self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster),
                    'cluster identifier observed' + (f' ({observed})' if valid else ''),
                    'check cluster identity against your recorded baseline')

    def execute(self):
        available = self.static_checks()
        if not self.static and available:
            self.runtime_checks()
        return int(bool(self.failures))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--static', action='store_true', help='validate prerequisites without requiring running services')
    modes.add_argument('--runtime', action='store_true', help='check running services (default)')
    parser.add_argument('--expect-cluster', type=lambda s: s if re.fullmatch(r'\d{1,20}', s) else parser.error('cluster must be numeric'))
    args = parser.parse_args()
    return Doctor(ROOT, args.static, args.expect_cluster).execute()


if __name__ == '__main__':
    raise SystemExit(main())
