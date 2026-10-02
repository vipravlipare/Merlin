# Part 04 — Environment setup and Section 8

One environment guide consolidates the setup documents; [Part 17](part-17-sprint0.md) separately owns the Sprint 0 calendar and Day 4 deliverables. Original details are recoverable in [the verified archive](archive/setup-sprint0-originals-2026-10-02.tar.gz). Canonical calendar: October 1–5, 2026; Days 1–5, **no separate Day 0**. Latest learner authorization permits assistant setup changes; application features remain learner-owned.

## Acceptance through Day 3

**Operational setup is complete.** Final read-only audit: October 2, 2026, 19:35 EDT. Day 3 work was performed early; its calendar date is not an invented execution date. Personal account facts and learning evidence remain separately attributed below. No feature, production deployment, application-data restore, Day 4 or Day 5 completion is claimed.

| Gate | Dated result |
|---|---|
| Day 1 baseline | Prior verified WSL2, Ubuntu, Git identity/GitHub SSH, VS Code WSL/Python extensions, Docker integration and core tools retained; installations not repeated |
| Day 2 accounts | Learner confirms Atlassian email verification, personal MFA, successful MFA sign-in, recovery stored privately in notes, Free plan, Scrum and no paid extras |
| S8-01/S8-02 | Exact registry pins, corrected configuration, quiet validation, ignored/untracked private inputs pass |
| S8-03 | Both healthy; host/container PostgreSQL authentication succeeds; deliberately wrong passwords rejected; Redis PONG; loopback ports and non-root processes pass |
| S8-04 | Stop/recreation preserves PostgreSQL volume `merlin_postgres_data`, cluster ID `7691749973399031842` and database list |
| S8-05 | Sanitized evidence recorded here; no passwords or resolved Compose output |
| Still unverified | GitHub browser MFA/repository visibility; Jira team-managed type/invitations; learner actual minutes, explain-back, whiteboard and re-quiz |
| Explicit deferrals | AWS signup/payment/CLI/deployment; DSA, independently at learner discretion; optional tools |

These unverified facts prevent an unqualified claim that **every learning/account item** is complete. They do not invalidate the observed local runtime proof. [Day 4 results and remaining learning/reproducibility gates](part-17-sprint0.md#day-4-closure-checklist) are recorded separately.

## One Ubuntu checkout

Use Ubuntu for development: the project tools and filesystem run together there. Windows remains the host/editor interface. Both active views access **the same files**, so there is no synchronization job.

📚 Learn first: [WSL installation][wsl], requirements; [VS Code WSL][vscode], opening a WSL folder; stop before alternate distributions/extensions (10 minutes inside setup learning).
↩ Return: open the verified Windows desktop shortcut **Merlin Ubuntu**, or Windows Explorer `\\wsl$\Ubuntu\home\vipra\Merlin`; done when VS Code shows `WSL: Ubuntu` and the terminal paths below match; if wrong, reopen the Ubuntu folder.

```bash
cd /home/vipra/Merlin
pwd
git rev-parse --show-toplevel
code .
```

Shortcut target is Windows VS Code with `--remote wsl+Ubuntu /home/vipra/Merlin`. Shortcut and Windows-share access were verified. Old `C:\Users\vipra\Merlin` remains retained, inactive and stale; do not edit it as the working project. Linux Python environments and package stores stay in Ubuntu. Never alternate Windows/Linux package managers for this environment.

Historical hardware: Intel i7-12700H, 16 GB RAM, RTX 3050 with 4 GB VRAM. Device visibility is not proof that a model uses CUDA. Recorded versions: Ubuntu 26.04 LTS; uv 0.12.21; Python 3.12.14; Node 24.21.0 LTS; pnpm 12.8.1; Docker Engine 29.7.2; Compose 5.4.0. Desktop application version, admin rights and NVIDIA driver details are not newly verified. Preserve working versions; Python 3.12.15 was an earlier candidate, not an upgrade instruction. Lockfile/fresh-clone acceptance remains Day 4 work.

📚 Learn first: [uv Python management][uv], version selection; [Node releases][node], LTS; [pnpm installation][pnpm], supported manager methods; stop before optional packages.
↩ Return: retain one project Python environment, explicit constraint and learner-owned lockfiles; record interpreter/tool paths during Day 4 doctor checks; do not install frontend or global feature dependencies now.

Alternative macOS/native Ubuntu routes use official Git/SSH, uv, Node/pnpm and [platform Docker prerequisites][docker-install]. Their GPU assumptions differ; neither was executed or changes the budget.

## Accounts and security

📚 Learn first: [Atlassian signup][signup], verification; [two-step verification][mfa], enrollment/recovery; [Jira space creation][jira], Free/team-managed Scrum selection; stop before organization administration or workflow customization (15 minutes).
↩ Return: Day 2, use existing accounts; allow 10 minutes verification, 10 MFA/private recovery, 10 space/sign-in/plan check; done when each fact is evidenced or explicitly pending; never select a paid trial to unblock setup.

Safe evidence: site `https://vipravlipare.atlassian.net`; space key `MER`; Scrum, Free, verified email, personal MFA and recovery storage **learner-confirmed**. Browser sign-in with MFA works. Team-managed type remains separately unconfirmed. Keep default workflow, written WIP limit two active items; skip imports, automation, invitations and extra products. Do not recreate the existing GitHub remote or change visibility.

MFA resists use of a stolen password by requiring another factor; it does not prevent every attack. GitHub SSH authenticates Git operations with a key; it does not secure Atlassian browser login or establish GitHub web MFA. Recover using privately stored recovery material through the account recovery flow; publish only its storage status. Never record recovery codes, tokens, private keys or passwords in commits, screenshots, Jira, logs or shell history.

📚 Learn first: [GitHub SSH][ssh], authentication testing; [AWS signup][aws], payment/plan conditions; [AWS Budgets][budgets], alert limitations; stop before enrollment.
↩ Return: record GitHub web MFA/visibility as pending until learner confirmation. AWS remains **deferred, local-only $0 release**, with no signup, CLI or resources; future signup requires learner acceptance of terms/payment conditions. Alerts are notifications, not spending caps; eligibility is unverified.

## S8-01 — Observe versions and images

📚 Learn first: [Compose application model][model], services/networks/volumes; stop before examples.
↩ Return: record timestamp, engine/context and manifest pins; completed October 2; rerun only after a relevant change, inside Day 3 capacity.

```bash
pwd
git rev-parse --show-toplevel
date -Iseconds
docker context show
docker version
docker compose version
docker info --format 'OS={{.OSType}} Architecture={{.Architecture}} MemoryBytes={{.MemTotal}}'
docker buildx imagetools inspect postgres:17.11-bookworm
docker buildx imagetools inspect redis:8.10.2-trixie
```

## S8-02 — Configuration contract

📚 Learn first: [Compose services][services], image, healthcheck, resources and logging; [PostgreSQL access][pg], basics; stop before advanced features.
↩ Return: compare every row, preserve project/storage, validate quietly; done when all fields and secret checks pass. Day 2 review is 15 minutes; authoring belongs to Day 3, not hidden extra time.

| Field | Required and observed |
|---|---|
| Project/services | `merlin`; only `postgres`, `redis`; containers `merlin-db`, `merlin-cache`; network `merlin-network`; no API placeholder |
| PostgreSQL pin | `postgres:17.11-bookworm@sha256:91eb910c44c7ed13f7f1a4ccadaa9ca72ef14cddc04cacb6e070e48eb44731a3` |
| Redis pin | `redis:8.10.2-trixie@sha256:7ef5b5cec96495a04ca7feff88a9492efeab8053fb284d24bdd73344c9245a48` |
| Private inputs | Required `POSTGRES_USER`, `POSTGRES_DB`, `POSTGRES_PASSWORD`; root `.env` mode 0600, ignored/untracked; no literal password |
| Ports | `127.0.0.1:5432:5432`; `127.0.0.1:6379:6379` |
| Health | PostgreSQL `pg_isready`; Redis exact `PONG`; interval 10s, timeout 5s, retries 5, start period 30s |
| Limits | PostgreSQL 1 GiB/1 CPU; Redis 256 MiB/0.5 CPU; Redis data maxmemory 128 MiB |
| Storage | `merlin_postgres_data` at `/var/lib/postgresql/data`; `merlin_redis_data` at `/data`; never delete PostgreSQL storage to fix authentication |
| Redis smoke policy | `save ""`, appendonly `no`, maxmemory-policy `noeviction`; intentionally disposable; unauthenticated trusted-local synthetic use only |
| Logs/lifecycle | `json-file`, max-size `10m`, max-file `3`; restart `unless-stopped`; stop grace 30s; processes observed UID 999 |

```yaml
    environment:
      POSTGRES_USER: ${POSTGRES_USER:?Set POSTGRES_USER in .env}
      POSTGRES_DB: ${POSTGRES_DB:?Set POSTGRES_DB in .env}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}
```

Compose reads `.env` for interpolation independently of VS Code Python terminal injection. The `python.terminal.useEnvFile` notice does not mean Compose cannot read it; enabling terminal injection is unnecessary here. Environment variables are not a secret vault: Docker administrators can inspect them. Do not print full `docker compose config`, unrestricted container inspection or environment dumps. Loopback blocks ordinary remote access but not other local processes; this is not production hardening.

```bash
cd /home/vipra/Merlin
docker compose config --quiet
printf 'validation exit=%s\n' "$?"
docker compose config --services
docker compose config --images
git check-ignore .env
git ls-files --error-unmatch .env
git diff --cached --stat
```

Expected: quiet validation exits 0; `.env` is ignored; `git ls-files --error-unmatch .env` fails because the file is untracked. Review staged content privately as well as its stat; do not stage secrets or `.tools/`. Changing an initialization variable does **not** change the password stored in an existing PostgreSQL cluster; rotation requires a deliberate database action, not volume deletion.

Hint ladder: 1—separate host settings from container settings. 2—compare one table row at a time and preserve project/volume identity. 3—after a redacted attempt or explicit request, provide a focused snippet of at most 15 lines. Assistant setup corrections are not learner-authorship evidence.

## S8-03 — Runtime, authentication and process proof

📚 Learn first: [Compose startup][up], waiting; [PostgreSQL psql][psql], connection/password options; [Redis PING][ping], reply; stop before application queries.
↩ Return: run checks after configuration changes, inspect failures safely, stop at first failed gate; Day 3 verification 30 minutes. Already passed; do not restart merely to check a box.

```bash
docker compose up --wait --wait-timeout 120 postgres redis
docker compose ps
docker compose images
docker compose port postgres 5432
docker compose port redis 6379
docker compose exec -T postgres sh -c 'pg_isready -h 127.0.0.1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
docker compose exec -T postgres sh -c 'psql -X --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --list'
docker compose exec -T redis redis-cli PING
docker compose top
```

Health means the process responds to its readiness probe. Authentication means it accepts the right credential and rejects a wrong one. Local socket access or readiness alone may bypass password authentication through trust rules; neither proves it. Container DNS `postgres` is the service address; host `127.0.0.1` is the published endpoint.

```bash
docker compose exec -T postgres sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql -X -h postgres -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-password --list'
docker compose exec -T postgres sh -c 'PGPASSWORD=merlin-deliberately-wrong-test psql -X -h postgres -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-password --list'
```

First command must succeed; second must fail with password authentication rejection. Do not paste the real credential or raw sensitive error output into evidence.

Rootless Ubuntu host clients were installed from official Ubuntu packages into ignored `.tools/ubuntu-clients`, without sudo or changes to the system package database. PostgreSQL client/libpq 18.6 and Redis CLI 8.0.5 were used against the pinned servers. These exports affect only the current shell:

```bash
export PATH="/home/vipra/Merlin/.tools/ubuntu-clients/usr/lib/postgresql/18/bin:/home/vipra/Merlin/.tools/ubuntu-clients/usr/bin:$PATH"
export LD_LIBRARY_PATH="/home/vipra/Merlin/.tools/ubuntu-clients/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```
```bash
command -v psql
command -v redis-cli
apt-cache policy postgresql-client redis-tools
```
```bash
read -r -p 'Configured PostgreSQL username: ' setup_pg_user
read -r -p 'Configured PostgreSQL database: ' setup_pg_database
psql -X --host=127.0.0.1 --port=5432 --username="$setup_pg_user" --dbname="$setup_pg_database" --password --list
redis-cli -h 127.0.0.1 -p 6379 PING
```

Repeat the `psql` command once, entering a deliberately wrong password at its private prompt; rejection is required. `command -v` must identify an Ubuntu executable, not a helper container. No secret goes in the command line. Check `compose top` for non-root service processes and `compose port` for exact loopback bindings.

Diagnostics only when needed; inspect locally and redact before saving:

```bash
docker compose logs --no-color --tail=50 postgres redis
docker stats --no-stream
docker system df
```

## S8-04 — Storage retention

📚 Learn first: [Docker volumes][volumes], lifecycle; [PostgreSQL pg_controldata][control], cluster identifier; stop before repair operations.
↩ Return: baseline mounts/limits/cluster, then compare after recreation; 15-minute Day 3 baseline plus already executed transition. Existing proof passes; do not run `down -v`, prune or remove volumes.

```bash
setup_pg_id="$(docker compose ps -q postgres)"
setup_redis_id="$(docker compose ps -q redis)"
printf 'postgres=%s\nredis=%s\n' "$setup_pg_id" "$setup_redis_id"
docker inspect --format '{{json .Mounts}}' "$setup_pg_id"
docker inspect --format '{{json .Mounts}}' "$setup_redis_id"
docker inspect --format 'Image={{.Config.Image}} Memory={{.HostConfig.Memory}} NanoCpus={{.HostConfig.NanoCpus}}' "$setup_pg_id" "$setup_redis_id"
docker compose exec -T --user postgres postgres sh -c 'pg_controldata "$PGDATA"'
docker compose exec -T redis redis-cli CONFIG GET save appendonly maxmemory maxmemory-policy
```
```bash
docker compose down
docker compose up --wait --wait-timeout 120 postgres redis
docker compose ps
docker compose exec -T --user postgres postgres sh -c 'pg_controldata "$PGDATA"'
docker compose exec -T postgres sh -c 'psql -X --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --list'
docker compose exec -T redis redis-cli PING
```

The same named volume **and** cluster ID must return, with the same database list and healthy endpoints. A new healthy empty database is failure. Container IDs can change; volume/cluster identity must not. Redis’s named mount does not make data durable while save/AOF are disabled.

Observed transition removed old `db`/`cache` containers only; recreated corrected services and preserved PostgreSQL storage. Databases: `merlin_db`, `postgres`, `template0`, `template1`. No startup/collation mismatch warning observed; no schema, reindex or collation change performed. This is an empty setup-cluster retention test, not a production migration or backup-restore test.

Private rollback artifacts: `/tmp/merlin-setup-backup/database-before.dump` (0600; directory 0700) and `compose-before.yml`. They are temporary, not durable backup. Preserve volume first; rollback requires reviewing image/data compatibility and prior configuration before recreation. Restore was not tested. Never publish the dump or overwrite a database blindly.

## S8-05 — Sanitized evidence and learning

📚 Learn first: [Git recording changes][git], reviewing/staging; stop before commit examples.
↩ Return: record observed result, actual minutes, blocker and next action; Day 2 ritual 15 minutes, Day 3 ritual 15 minutes. Record unknowns honestly; re-quiz Day 4/5 inside existing ritual time.

Final audit independently rechecked pins, health, limits, log rotation, loopback, host correct/wrong-password behavior, Redis policy, database list and cluster identity. Earlier transition proof includes container authentication and non-root process checks. `.env` and `.tools/` ignored; `.env` untracked; whitespace check passes. Approximate earlier idle snapshot: PostgreSQL 21.21 MiB/1 GiB, Redis 6.121 MiB/256 MiB; volume about 48.13 MB; Windows C: free space 38 GiB, above the 20 GiB planning threshold. These are observations, not performance benchmarks or future capacity guarantees. Unrelated Docker resources were not pruned.

Stand-up: completed local setup and storage/authentication proof; blockers are unreported personal/learning facts; next action Day 4 reproducibility. Planned minutes below are **not actual elapsed minutes**. Learner/assistant time ledger remains unreported; no invented learning success.

Explain-back questions: What extra attack does MFA resist? Why does SSH not protect another browser login? How is recovery kept private? Why is readiness different from authentication? Why does an initialization variable not rotate an existing password? Which feature minutes move when setup overruns? What is the difference between health, authentication and storage retention?

Answer guide: a second factor resists stolen-password access; SSH key authentication has a separate scope; private recovery material restores access without public disclosure; readiness tests availability while credential tests prove access control; initialization runs on an empty data directory and stored roles persist; spill replaces equal Day 6 feature minutes; persistence is proved by unchanged volume/cluster identity after recreation. Whiteboard/interview: explain loopback ports, service DNS and named volumes in 60 seconds. Learner explain-back and re-quiz are still pending.

## Troubleshooting and optional tools

📚 Learn first: [Docker troubleshooting][troubleshoot], diagnostics; stop before unrelated support features.
↩ Return: record first observed symptom/fix inside existing ritual/check time; preserve logs/storage and stop destructive cleanup.

| Symptom | First safe check/action |
|---|---|
| WSL/Docker unavailable | Distribution state, virtualization, disk/integration; documented update/restart |
| GPU invisible/OOM | Driver/pass-through/limits; CPU-only smaller model, stop concurrent workloads |
| Port occupied | Inspect owner; documented loopback port; never public binding |
| PostgreSQL auth fails | Inputs, endpoint and existing volume; no volume deletion |
| uv/pnpm mismatch | Interpreter/declared versions/locks; record compatible swap, no silent regeneration |
| AWS payment or clone failure | Stop enrollment or first failed command; local fallback/document fix |

📚 Learn first: [Ollama API][ollama], base URL only; stop before downloads.
↩ Return: install only at funded first use; verify licenses/pins/APIs then. Scratch version first, framework second, comparison ADR third; AI needs golden set, baseline, metric, latency and cost.

| Tool | First use and gate |
|---|---|
| Ollama/Qwen3 0.6B or 1.7B/embeddings | Day 8/16; hardware/digest/memory/TTFT/tokens per second |
| MongoDB; JDK 21/Maven/Spring | Conditional Day 31; funded swap after scratch traces |
| kind/kubectl | Conditional Day 32; core/hardware/swap |
| n8n | Conditional Day 28; handwritten workflow/license/swap |
| Chroma/Qdrant | Conditional comparison; same corpus/golden set/swap |
| Hugging Face/Colab/Kaggle | Conditional Day 30; licenses/quota/swap |
| AWS CLI | Conditional Day 25/32; accepted account terms, least privilege, local fallback |
| Playwright/k6 | Conditional Day 34; concrete browser/load gap and swap |

README, Compose down and Actions documentation opened successfully October 2 during Day 4 work. Resource access previously verified October 1–2, 2026; target manifests and local runtime verified October 2. This consolidation does not claim a new web/account audit. Context7 unavailable. Account-specific eligibility, optional APIs/licenses and all unexecuted paths remain 🔎 verify at first use.

[wsl]: https://learn.microsoft.com/en-us/windows/wsl/install
[vscode]: https://code.visualstudio.com/docs/remote/wsl
[docker-wsl]: https://docs.docker.com/desktop/features/wsl/
[docker-install]: https://docs.docker.com/get-started/get-docker/
[uv]: https://docs.astral.sh/uv/guides/install-python/
[node]: https://nodejs.org/en/about/previous-releases
[pnpm]: https://pnpm.io/installation
[signup]: https://support.atlassian.com/atlassian-account/docs/create-an-atlassian-account
[mfa]: https://support.atlassian.com/atlassian-account/docs/manage-two-step-verification-for-your-atlassian-account/
[jira]: https://support.atlassian.com/jira-software-cloud/docs/create-a-new-project/
[ssh]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
[aws]: https://docs.aws.amazon.com/accounts/latest/reference/sign-in-new.html
[budgets]: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
[model]: https://docs.docker.com/compose/intro/compose-application-model/
[services]: https://docs.docker.com/reference/compose-file/services/
[pg]: https://www.postgresql.org/docs/17/tutorial.html
[up]: https://docs.docker.com/reference/cli/docker/compose/up/
[psql]: https://www.postgresql.org/docs/17/app-psql.html
[ping]: https://redis.io/docs/latest/commands/ping/
[volumes]: https://docs.docker.com/engine/storage/volumes/
[control]: https://www.postgresql.org/docs/17/app-pgcontroldata.html
[git]: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
[readme]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
[actions]: https://docs.github.com/en/actions/get-started/understand-github-actions
[troubleshoot]: https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/
[ollama]: https://docs.ollama.com/api/introduction
