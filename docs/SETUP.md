# Merlin local setup

Scope: reproducible **setup services**, not a runnable application. Use the Ubuntu filesystem and a WSL terminal. Windows is the host and editor interface. Follow the [command reference](planning/TERMINAL_COMMANDS.md) for Explorer, Codex and daily start/stop operations.

## Prerequisites — installed before the five project commands

Ubuntu/WSL2, Git, Docker Desktop with Ubuntu integration and a working Docker Compose plugin; uv 0.12.21 with Python 3.12 available; Node 24.21.0 and pnpm 12.8.1; native `psql` and `redis-cli`. Docker must run Linux containers. The project's Python constraint is >=3.12,<3.13, selected by `.python-version`; `uv.lock` is committed. No application dependencies are declared yet.

Official installation references: [WSL](https://learn.microsoft.com/en-us/windows/wsl/install), [Docker WSL integration](https://docs.docker.com/desktop/features/wsl/), [uv Python management](https://docs.astral.sh/uv/guides/install-python/), [Node releases](https://nodejs.org/en/about/previous-releases), [pnpm installation](https://pnpm.io/installation), [PostgreSQL clients](https://www.postgresql.org/docs/17/app-psql.html), [Redis CLI](https://redis.io/docs/latest/develop/tools/cli/). These are host prerequisites, not hidden project setup commands. Their installation can take additional time.

On ordinary Ubuntu, clients can be installed with:

```bash
sudo apt-get update
sudo apt-get install postgresql-client redis-tools
```

This learner's verified official Ubuntu clients are already installed independently of the repository under `~/.local/share/merlin-clients`, exposed by `~/.local/bin/psql` and `~/.local/bin/redis-cli`. A clone does not carry these host files. If a client is missing, install the prerequisite; do not copy `.env` or depend on another checkout's ignored `.tools` directory. Client versions may differ from the server major when protocol-compatible; the doctor tests the actual connection.

## Original checkout

Canonical learner path: `/home/vipra/Merlin`. Windows Explorer accesses the same files at `\\wsl.localhost\Ubuntu\home\vipra\Merlin` (also `\\wsl$\Ubuntu\home\vipra\Merlin`). The old `C:\Users\vipra\Merlin` is stale and is not synchronized. Open the **Merlin Ubuntu** desktop shortcut or run `code .` from the canonical WSL directory. Confirm VS Code says `WSL: Ubuntu`.

The existing original `.env` and PostgreSQL cluster are preserved. Never replace this file to fix an existing password: initialization variables do not rotate stored database roles. The original cluster baseline is `7691749973399031842`; named volume `merlin_postgres_data`. No fresh clone is permitted to reuse or delete that volume.

## Fresh clone — exactly five project commands

Choose a destination that does not already exist. These commands use the public setup branch and require the host prerequisites above. No source file or Compose override needs editing.

```bash
git clone --branch setup/E0-US01-environment https://github.com/vipravlipare/Merlin.git "$HOME/Merlin-fresh"
cd "$HOME/Merlin-fresh"
uv sync --locked
uv run --locked python tools/setup_local.py
uv run --locked python tools/doctor.py
```

The helper creates a **new ignored `.env`** only when absent, with mode 0600, a random local password, a checkout-specific project/network name and free loopback ports. It validates quietly and starts only PostgreSQL/Redis. It does not copy your original credentials, modify application source, drop volumes or overwrite an existing environment. Ports are selected immediately before startup; if another process takes one, startup stops with a safe error. Inspect/fix that collision privately rather than exposing a public port or deleting storage.

This file is private machine configuration, not a committed dependency. `.env.example` documents variable names without a usable password. Manual environments must use unique project/network/port identities for a second checkout. Do not copy the original `.env` into a fresh clone.

The fifth command checks interpreter/locks, secret boundary, clients, service health, resources/logs, loopback, native host and in-container correct/wrong-password behavior, non-root processes, volume identity and Redis policy. It prints safe check results and observed cluster identity. Application checks remain N/A; a healthy database is not an implemented API or secure per-user data model.

## Versions, resources and data policy

PostgreSQL: `postgres:17.11-bookworm` plus committed sha256 digest; 1 GiB/1 CPU; data mount `/var/lib/postgresql/data`. Redis: `redis:8.10.2-trixie` plus committed sha256 digest; 256 MiB/0.5 CPU; 128 MiB data ceiling; snapshots/AOF disabled and noeviction. Both have 30-second health start periods and 10m × 3 log rotation. Bindings stay on 127.0.0.1. PostgreSQL volume is durable across ordinary container removal; Redis's named mount does not override its intentionally disposable data policy.

Within Compose, the database service address is `postgres:5432`; from Ubuntu, use the published loopback host port shown by `docker compose port postgres 5432`. Clients inside a container have their own localhost. Docker administrators and local processes are inside this local trust boundary. Synthetic-only setup is not production authentication/TLS/backup acceptance.

## Start, diagnose and stop

```bash
uv run --locked python tools/setup_local.py
uv run --locked python tools/doctor.py
docker compose ps
docker compose port postgres 5432
docker compose port redis 6379
docker compose stop --timeout 30 postgres redis
```

Start helper preserves an existing `.env`. Doctor is read-only and never starts/stops services. Use `--static` when checking configuration prerequisites without running services. Use `--expect-cluster 7691749973399031842` only for the original checkout; a fresh clone correctly has a different cluster.

Ordinary `docker compose down` removes containers/network but retains named volumes. Recreate with the helper and compare cluster ID to prove storage retention. Never run `down --volumes`, prune or destructive migrations against the original checkout. Disposable test teardown with volumes is allowed only after verifying its unique project/volume names; CI's cleanup affects only its runner-generated isolated project.

| Symptom | First safe fix |
|---|---|
| Doctor says Docker unavailable/stopped | Start Docker Desktop; check Ubuntu integration/context, then rerun. |
| Wrong Python/lock | Use uv-managed 3.12 and `uv sync --locked`; do not silently regenerate lockfiles. |
| Missing psql/redis-cli | Install the declared native host prerequisites. |
| PostgreSQL auth failure | Inspect credentials and selected endpoint privately; preserve data volume. |
| Port occupied | Inspect the owning process and choose an unused loopback port for that checkout. |
| Fresh-clone project collision | Check `.env` project/network/ports; never copy the original configuration. |
| CI red | Open the first failed step, reproduce locally and record the failing gate; do not call unbuilt app tests green. |

## CI and what remains outside setup

`.github/workflows/setup.yml` runs on push, pull request and manual dispatch with read-only repository permissions, fixed runner/tool versions and full action commit pins. It installs host prerequisites, recreates locked environments, runs doctor safety tests, starts isolated services with synthetic credentials, runs static/runtime doctor and always tears down its own disposable resources. No provider secret, AWS step, deployment or private database dump is used.

Application dependencies, schemas/migrations, login, owner filtering, API/UI, models and measured AI features belong to later learner implementation. Global Caveman preferences are available to local Codex; OmniRoute inference is not configured as Codex's default and is not required here. Account/MFA facts, actual learning and minutes are recorded separately in Part 17, with attribution and unknowns.
