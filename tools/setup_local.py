#!/usr/bin/env python3
"""Create private local inputs when absent, then start this checkout's services."""
from pathlib import Path
import hashlib
import os
import secrets
import socket
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def command(args):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode:
        raise SystemExit("Setup stopped: " + " ".join(args[:3]) +
                         " failed. Check Docker integration/configuration privately; no secrets printed.")
    return result


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def main():
    env = ROOT / ".env"
    command(["git", "check-ignore", "-q", ".env"])
    if not env.exists():
        project = "merlin-" + hashlib.sha256(str(ROOT).encode()).hexdigest()[:10]
        pg_port, redis_port = free_port(), free_port()
        while redis_port == pg_port:
            redis_port = free_port()
        contents = ("POSTGRES_USER=merlin\nPOSTGRES_DB=merlin_db\nPOSTGRES_PASSWORD=" +
                    secrets.token_hex(32) + "\nMERLIN_PROJECT_NAME=" + project +
                    "\nMERLIN_NETWORK_NAME=" + project + "-network\nPOSTGRES_HOST_PORT=" +
                    str(pg_port) + "\nREDIS_HOST_PORT=" + str(redis_port) + "\n")
        fd = os.open(env, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as stream:
            stream.write(contents)
        print("Created ignored private .env; isolated project " + project + ".")
    else:
        print("Preserving existing .env and its project/storage identity.")
    if env.is_symlink() or env.stat().st_mode & 0o077:
        raise SystemExit("Setup stopped: .env must be a regular private file (chmod 600 .env).")
    command(["docker", "compose", "config", "--quiet"])
    command(["docker", "compose", "up", "--wait", "--wait-timeout", "120", "postgres", "redis"])
    print("PostgreSQL and Redis started; run uv run --locked python tools/doctor.py next.")
    print("No database volumes removed; existing PostgreSQL passwords were not rotated.")


if __name__ == "__main__":
    main()
