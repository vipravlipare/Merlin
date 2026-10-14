# Day 6 coding preparation — observed October 7, 2026

This is a preparation and mentoring handoff. The learner writes all application code, migrations, tests and configuration. No application implementation or learning completion is claimed.

## Latest schema rewrite — review before using commands below

The active up.sql combines username/canonical and UUIDv4 with restored optional email, title/body, blank-note checks and the server-controlled 24-hour deadline/cleanup function. [Current design](../architecture/users-notes-design.md#current-schema--latest-explicit-rewrite-request) defines both server and device timestamps. Weighted Unicode validation, limited-role authenticated actor setup and scheduler execution remain pending. The migration is unapplied/untested. PostgreSQL17 and isolated storage are unchanged. Review current fields before using historical examples below.

## Step 3 dependency gate — verified October 8

The Step 2 Users/Notes design and expected outcomes are reviewed as specifications, not implementation evidence.

| Item | Recorded approach / observed evidence |
|---|---|
| Python | 3.12.14; project requires 3.12, interpreter pin retained |
| Driver | Synchronous Psycopg 3.3.6 with binary adapter 3.3.6 |
| Migration approach | Planned scratch numbered up/down files, to be personally authored and applied with existing psql; no Alembic/SQLAlchemy package required |
| Testing | pytest 9.1.1; learner-authored tests remain unwritten/unrun |
| Locked consistency | `uv sync --locked --check` exit 0; resolved 11, checked 8 packages; would make no changes |
| Imports | Existing virtualenv imports Psycopg and pytest successfully; adapter reports binary |

The first sandbox attempt was blocked by uv cache permissions. Approved cache access completed the consistency check; no dependency edits were made. This was an environment boundary, not a learner setup problem.

The Step 3 first checkbox can be marked complete for the recorded approach, pins, lock consistency and imports. Isolated-storage/connectivity evidence already exists in the sections below. Email approach approved October 8: one trimmed original-cased optional field and unique lowercase expression index; blank input becomes no value. Next verify weighted visible-character enforcement (emoji 4, other character 1), then learner authors the migration and connectivity attempt. Keep the 60-minute block; actual minutes remain unknown. Learner now reports successful app/database_connectivity_probe.py execution after read-only review; exact success output was not supplied. No migration or feature tests have run.

📚 Learn first: [Your reviewed design](../architecture/users-notes-design.md), Users email and character-counting rules; [Psycopg transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html), transaction scope.
↩ Return: email representation is chosen; verify weighted character validation/enforcement before applying the learner migration. Do not apply a migration until those technical choices and the authored migration are reviewed.

## Current next action — October 8

The learner's reviewed [Users/Notes design](../architecture/users-notes-design.md) supersedes the starter contract below: email/title are optional, limits are weighted limits 175/7,000 (each emoji 4, other visible character 1), deletion policy removes owned notes and timestamps follow device-reported instants. Historical required-email/title200/restricted-delete examples below are not the current acceptance contract. MER-2–7 have been deleted; use MER-1 only.

Earlier pyproject read-back had no dependencies. Learner October 8 output now confirms psycopg 3.3.6, psycopg-binary 3.3.6 and pytest 9.1.1 installed under /home/vipra/Merlin/.venv/lib/python3.12/site-packages. Package metadata, imports and test-target host connectivity are evidenced; feature tests have not run. Dependency install metadata is now evidenced. Learner port check was clear. October 8 outputs confirm healthy project merlin-d6-20261008105707, PostgreSQL at 127.0.0.1:55432 and volume merlin-d6-20261008105707_postgres_data. Learner outputs now confirm cluster 7694311451826794534 (different from original), network merlin-d6-20261008105707-network and password-based host database listing. Isolation/connectivity gate is evidenced. No migration or application tests have run. Routine commands are in docs/setup/terminal-commands.md. Psycopg 3.3.6 and pytest 9.1.1 metadata were rechecked on PyPI October 8; local installed versions and imports are evidenced. A scratch migration uses learner-authored ordered up/down files with psql, so Alembic is not required at this stage. Do not migrate before proving isolated storage.

Both Step 3 entry checkboxes pass from recorded October 8 evidence. Email representation is chosen; weighted character validation still needs an implementation approach before applying the migration. Existing Sprint 0 setup need not be repeated.

## Current work tracker and final readiness check

Use **[MER-1](https://vipravlipare.atlassian.net/browse/MER-1) and its 16 native checkboxes** as the Day 6 tracker. The latest handoff supersedes the original child-ticket workflow below: MER-2–7 were deleted by the learner; they do not add work or block starting Day 6. The mapping below is retained as creation history. This session did not inspect or change Jira.

Final read-only doctor check returned exit 0: prerequisites, private configuration, PostgreSQL/Redis health, loopback/resource limits, correct/wrong-password tests, original cluster `7691749973399031842` and Redis policy/PONG PASS. Document links and the 360-minute budget also pass. October 8 dependency/import and isolated-storage gates now pass as recorded above; feature implementation/mastery is not claimed.

📚 Learn first: [Day 6 steps 1–5](part-18-sprint1.md#day-6-checklist--steps-1–5), required evidence; stop before database changes.
↩ Return: follow MER-1 in order, using this guide for explanations/commands. Check a box only after its evidence exists; preserve the original database and keep the agreed cap.

## Steps 1–5 readiness decision — October 7 follow-up

**GO for Day 6 learning/design; coding is conditional.** The existing doctor was rerun read-only with expected original cluster `7691749973399031842` and returned exit 0. Python/locks/private configuration, Compose, health, loopback/resources, PostgreSQL host/service positive and negative authentication, retained identity and Redis policy/PONG passed. Application tests remain explicitly not applicable. No database changes or dependency installation were performed.

| Step | Ready to start? | Required next evidence |
|---|---|---|
| 1 — Setup review and database explanations | Yes | Your evidence review, three answers and ownership drawing |
| 2 — Users/notes design | Yes, after explanations are reviewed | Your two field tables, rule/index rationale and expected cases |
| 3 — First coding attempt | Start prerequisite checks; do not apply migrations yet | Compatible installed dependencies and a proven separate synthetic target, then your reviewed code |
| 4 — Verification | Plan ready; execute after code exists | Observed results for implemented cases; absent ownership boundary stays pending |
| 5 — Handoff | Yes; record progress throughout | Actual minutes or unknown, secret review, first blocker and exact restart action |

Jira creation/read-back evidence from the connected session is recorded below (MER-1 through MER-7); this follow-up session has no Jira tools and did not recheck live statuses. Missing Day 6 feature dependencies and target isolation are implementation-entry tasks, not a reason to repeat Sprint 0.

📚 Learn first: [Day 6 steps](part-18-sprint1.md#day-6-checklist--steps-1–5), evidence and budgets; stop before migration application.
↩ Return: begin Step 1, then share explanations/design for review. Keep the existing 360-minute cap; do not mark learner or coding outcomes complete from this infrastructure check.

## Current evidence and limits

📚 Learn first: [Sprint 0 closure](part-17-sprint0.md#setup-closure--october-6-2026), current evidence table; [Day 6 checklist](part-18-sprint1.md#day-6-checklist--steps-1–5), steps 1–5; stop before historical setup remediation.
↩ Return: D6-SETUP/MER-2; reuse completed setup, record personal explain-back gaps and actual time. Maximum 45 minutes; do not reinstall working tools.

| Prerequisite | Observed result |
|---|---|
| Ubuntu checkout | `/home/vipra/Merlin`; Ubuntu 26.04 LTS, WSL2 kernel `6.6.87.2-microsoft-standard-WSL2`. The editor's WSL status is not independently observed. |
| Python/uv | `.venv` Python 3.12.14; uv 0.12.21; interpreter pin and offline lock consistency PASS. |
| Private configuration | `.env` mode 0600, owned by vipra, ignored and not tracked. Contents were not printed. |
| Docker/Compose | Existing read-only doctor confirms service/configuration/runtime checks PASS. Initial sandbox Docker socket denial was an agent access restriction; approved outside-sandbox doctor passed. No learner Docker repair needed. |
| PostgreSQL connectivity | Host TCP and service TCP correct-password access PASS; deliberately wrong passwords rejected. Health, loopback binding and mounted volume PASS. |
| Preserved storage | Current cluster `7691749973399031842` matches original; original named volume `merlin_postgres_data`. No migration, reset, recreation or deletion performed. |
| Sprint 0 evidence reused | Eight existing doctor safety tests, published passing CI run `37535970773` at `f8799f7`, unchanged-clone proof: recorded in Part 17. Not rerun or republished this session. |
| Application dependencies | `pyproject.toml` has `dependencies = []`; psycopg, pytest, Alembic and SQLAlchemy imports absent. Coding dependency gate FAIL until learner resolves/installs selected packages. |
| Day 6 test storage | No Day 6 isolated project/volume/cluster identity has been proven. Historical clone isolation is not a current migration target. Gate PENDING. |
| Application tests/learning | No feature tests run; three explain-backs, learner design, migration and whiteboard unobserved. Actual learner minutes unknown. |

## Jira records actually created

📚 Learn first: [Day 6 Story contract](part-18-sprint1.md#jira-ready-ticket--day-6-database-foundation), completion criteria; [transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), commit/rollback; stop before expanding scope.
↩ Return: track evidence in the corresponding child; only change completion status after its outcome is observed. Jira work uses existing setup/ritual minutes.

Live Atlassian read-write access worked. MER project 10001 has board 2. Existing `MER Sprint 1`, ID 3, is **future**; it was not created, renamed or started. JQL `project = MER ORDER BY created ASC` returned no issues, with `isLast=true`, before creation: no existing Story/child duplicates or Epic found. Story sprint assignment succeeded; read-back confirmed seven issues, six parent relationships and all statuses To Do. Assignee, proposed points and due date were left unset rather than guessed. Children track parent work; points are not counted again.

| Record | Real link | Minutes |
|---|---|---:|
| Story | [MER-1](https://vipravlipare.atlassian.net/browse/MER-1) | 294 tracked total |
| D6-SETUP | [MER-2](https://vipravlipare.atlassian.net/browse/MER-2) | 45 |
| C-04.01 transactions/ownership | [MER-3](https://vipravlipare.atlassian.net/browse/MER-3) | 45 |
| C-04.02 users/notes design slice | [MER-4](https://vipravlipare.atlassian.net/browse/MER-4) | 60 |
| C-04.03 conditional migration/connectivity | [MER-5](https://vipravlipare.atlassian.net/browse/MER-5) | 60 |
| D6-VERIFY | [MER-6](https://vipravlipare.atlassian.net/browse/MER-6) | 39 |
| D6-EOD | [MER-7](https://vipravlipare.atlassian.net/browse/MER-7) | 45 |

Descriptions contain the relevant full checklists, Learn/Return blocks, boundaries and completion rules. Jira renders some Markdown checkboxes as text: child status and recorded evidence remain authoritative. Local relative document links name repository artifacts; open those files in the checkout, not through Jira. No paid checklist plugin is required.

Budget remains 294 + deferred/uncommitted DSA 30 + reserve 36 = **360 minutes**. AWS and DSA remain deferred. Dependency/isolation work uses the 15-minute entry gate inside C-04.03 and reduces its 45-minute coding attempt if it takes longer. Setup spill replaces feature minutes. No stretch, new scope or GitHub publication.

## First unchecked learner item and explain-back

📚 Learn first: [transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), transaction block and rollback, stop before savepoints; [row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), table-owner/superuser/BYPASSRLS exceptions, stop before writing policies.
↩ Return: C-04.01/MER-3, answer the three questions below in your own words and draw the identity boundary. Use the existing 45-minute learning block; share answers for review before design/coding.

The literal first checkbox remains the learner's review of Sprint 0 evidence; this assistant's checks do not prove that personal review. Use the evidence table above to close the operational portion without repeating setup. Remaining Sprint 0 retention/CI explain-back, whiteboard and spaced re-quiz remain separate learning gaps.

A transaction groups changes into one operation. Commit makes its successful changes durable; rollback cancels its uncommitted changes. A foreign key proves that a referenced user exists. Authorization decides whether the current actor may access that user's note. A submitted owner ID is untrusted input. A trusted backend identity must supply the owner and constrain reads/updates. Privileged database roles can bypass row-security policies, so their successful queries cannot demonstrate ordinary-user denial.

Answer without copying:

1. A user insert succeeds; a note insert fails inside the same transaction. After rollback, what remains? Would separate commits change the answer?
2. Actor B submits actor A's `owner_id` or guesses A's note UUID. Where must identity come from, and what must a read/update enforce?
3. Why does a successful administrative query fail to prove row-security denial? Which role properties must a meaningful RLS test avoid?

Draw browser/client → authenticated backend actor → owner-scoped repository → PostgreSQL. Synthetic actors can test the repository contract; they do not prove that production authentication exists.

## Users/notes design and expected tests

📚 Learn first: [starter contract](../architecture/part-11-schema-ai-architecture.md#day-6-usersnotes-starter-contract), two tables and acceptance table; [PostgreSQL tutorial](https://www.postgresql.org/docs/17/tutorial.html), tables and foreign keys; stop before future AI tables.
↩ Return: C-04.02/MER-4, write your own two plain Markdown tables and input/expected-result table, then share for review. Spend 30 minutes on fields/rules and 30 on cases. No SQL until reviewed.

Use the Part 11 candidate: users has UUID ID, required normalized unique email and time-zone-aware creation time. Notes has UUID ID, required user foreign key, nonblank title of at most 200 characters, required body allowing empty text, and creation/update timestamps. Choose normalization precisely, timestamp update behavior and restricted owner deletion. Explain primary/unique indexes and an owner-listing index using the actual query pattern. A UUID is an identifier, not permission.

| Test input/action | Expected result; currently all feature cases PENDING |
|---|---|
| Valid synthetic user and note; commit/reconnect | Both rows persist with intended owner and timestamps. |
| Same email after selected normalization | Second write rejected; original row unchanged. |
| Unknown owner | Foreign-key rejection; no invalid note retained. |
| Whitespace-only title; 201-character title | Each rejected; no invalid row retained. Test 200-character boundary succeeds. |
| Empty body | Accepted under the candidate contract; missing/null body rejected. |
| Delete user referenced by note | Rejected under restricted-delete choice; both rows preserved. |
| First write succeeds, second fails, rollback | Neither new row remains; pre-existing fixtures remain. |
| Migration down then up, disposable target only | Intended objects removed/recreated; unrelated objects untouched. Schema downgrade differs from transaction rollback. |
| A accesses own note; B guesses A's ID or changes owner input | A succeeds; B receives no unauthorized data/change. Pending until owner boundary exists; link C-04.04. |
| Errors/logging | No password, private content or credential-bearing URL exposed. |

## Dependency gate: commands for the learner, not executed

📚 Learn first: [Psycopg installation](https://www.psycopg.org/psycopg3/docs/basic/install.html), binary installation; [uv dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/), adding dependencies; [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html), install and first test; stop before copying examples.
↩ Return: C-04.03/MER-5, record selected approach and run the following only after design review. Stop on the first failure and share the sanitized message. Installation/import success is a dependency check, not a feature test.

Recommended narrow scratch path: synchronous Psycopg 3.3.6, pytest 9.1.1, PostgreSQL 17.11, learner-authored numbered up/down migration files applied with existing psql. No migration package is needed for this scratch approach; versions and ordered application/undo procedure must still be recorded. Alembic/SQLAlchemy are a later framework swap after scratch proof and comparison ADR, not missing setup that must be installed now. Published package versions were verified October 7; combined local resolution/imports are unproved. Psycopg's current documentation reports a development version, so verify any API you use against the pinned release.

These commands intentionally change your dependency metadata/lock/environment when **you** run them. They do not create application source:

```bash
cd /home/vipra/Merlin
uv add 'psycopg[binary]==3.3.6'
uv add --dev 'pytest==9.1.1'
uv sync --locked
uv run --locked python -c 'import psycopg, pytest; print(psycopg.__version__, pytest.__version__)'
git diff -- pyproject.toml uv.lock
```

Expected imports: 3.3.6 and 9.1.1. Do not replace the working Python pin. Record transaction scope as one explicit unit containing both writes; choose context-manager commit/rollback behavior only after explaining it. [Psycopg transaction management](https://www.psycopg.org/psycopg3/docs/basic/transactions.html) explains failure and connection contexts.

## Isolated storage gate: learner commands, not executed

📚 Learn first: [Compose environment precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/), interpolation; [psql](https://www.postgresql.org/docs/17/app-psql.html), connection options and ON_ERROR_STOP; stop before destructive cleanup.
↩ Return: C-04.03/MER-5, prove distinct project/network/ports/mounts/cluster before any migration. Stop if identities differ from the expected synthetic target or any command fails. Never alter original `.env` or use original storage.

Open a **separate Ubuntu terminal dedicated to Day 6 test storage**. The following shell overrides do not write configuration files. They use the existing reviewed Compose file and create new disposable PostgreSQL and Redis resources only when you run the startup command. Keep this terminal for the test session; do not run original-project commands here. Closing it removes the shell overrides, not Docker storage. No teardown/delete command is supplied.

First check that ports 55432 and 56379 have no listener; if either appears, stop and choose another pair before proceeding:

```bash
cd /home/vipra/Merlin
ss -ltn '( sport = :55432 or sport = :56379 )'
export MERLIN_PROJECT_NAME="merlin-d6-$(date +%Y%m%d%H%M%S)"
export MERLIN_NETWORK_NAME="${MERLIN_PROJECT_NAME}-network"
export POSTGRES_HOST_PORT=55432 REDIS_HOST_PORT=56379
export POSTGRES_USER=merlin_d6 POSTGRES_DB=merlin_d6
read -rsp 'New synthetic Day 6 password (keep private): ' POSTGRES_PASSWORD
printf '\n'
[ -n "$POSTGRES_PASSWORD" ] || { printf 'Empty password; stopping.\n'; exit 1; }
export POSTGRES_PASSWORD
docker compose config --quiet
docker compose up --wait --wait-timeout 120 postgres redis
docker compose ps
docker compose port postgres 5432
docker inspect "$(docker compose ps -q postgres)" --format '{{range .Mounts}}{{println .Name .Destination}}{{end}}'
docker network inspect "$MERLIN_NETWORK_NAME" --format '{{.Name}}'
docker compose exec -T postgres sh -c 'psql -X -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "SELECT system_identifier FROM pg_control_system();"'
psql -X -W -h 127.0.0.1 -p 55432 -U merlin_d6 -d merlin_d6 -v ON_ERROR_STOP=1 -c 'SELECT current_database(), current_user;'
```

Enter the synthetic password at the psql prompt. Stop immediately if password input was empty. Expected data mount: `${MERLIN_PROJECT_NAME}_postgres_data`, never `merlin_postgres_data`; distinct network; PostgreSQL port only `127.0.0.1:55432`; cluster must differ from `7691749973399031842`. Record the actual safe IDs. Inspect only names/mounts: full Docker inspection/resolved Compose output may disclose credentials. Docker administrators can inspect container environments; this local synthetic target is not a production secret boundary.

The initialization role is administrative. It can prove connectivity/migration behavior, **not ownership denial**. A later application/RLS role must have suitable limited privileges. Python connectivity must use this test endpoint explicitly, never fall back to original `.env`. Credentials belong in private runtime input, not code, command arguments, Git or Jira. At the end use a fresh ordinary Ubuntu terminal for the original read-only doctor:

```bash
cd /home/vipra/Merlin
uv run --locked --no-sync python tools/doctor.py --expect-cluster 7691749973399031842
```

## First learner migration/connectivity attempt, only after gates pass

📚 Learn first: [psql](https://www.postgresql.org/docs/17/app-psql.html), file execution, single-transaction and ON_ERROR_STOP; [Psycopg transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html), connection context; stop before framework expansion.
↩ Return: personally author the reviewed two-table migration, matching undo migration, connection probe and tests. Maximum 45 minutes minus prerequisite spill. Share your redacted attempt/first error for hints; no migration has been supplied or applied by the assistant.

Suggested learner-owned paths to agree at design review: `migrations/001_users_notes.up.sql`, `migrations/001_users_notes.down.sql`, `app/database_connectivity_probe.py`, `tests/test_users_notes.py`. These files do not exist from this preparation. You create them yourself. Up/down files must affect only the reviewed objects; record the revision and application order. Do not hide destructive reset logic in the probe or test fixtures.

Before applying, share the attempted migration and safe target IDs for read-only review. Once reviewed and both gates pass, the exact application command in the dedicated test terminal is:

```bash
psql -X -W -h 127.0.0.1 -p 55432 -U merlin_d6 -d merlin_d6 -v ON_ERROR_STOP=1 --single-transaction -f migrations/001_users_notes.up.sql
```

Your Python probe should accept the explicit synthetic target, perform a read-only readiness query, close its connection and report only a safe result. It must not load original credentials by default. Once you have authored it and the tests:

```bash
uv run --locked python app/database_connectivity_probe.py
uv run --locked pytest -q tests/test_users_notes.py
```

Do not run these against guessed/default targets. Review the learner-authored down migration before applying its analogous psql file command; downgrade/reapply is permitted only in the proven synthetic target. Missing files, no collected tests, errors or unimplemented owner filtering are PENDING/FAIL, never PASS. Existing setup CI does not prove these new cases.

Hint ladder: 1 — identify which layer owns the failed invariant. 2 — outline connection, transaction, two operations, rollback and independent state inspection. 3 — only after your redacted attempt or explicit request, a focused hint of at most 15 lines. After 25 focused stuck minutes, record the rung and first error; do not add time beyond the cap.

## Resource verification and exact restart

Official PostgreSQL transaction/row-security/tutorial/psql, Psycopg installation/transactions, uv dependency and pytest getting-started pages were retrieved October 7, 2026. PyPI published Psycopg 3.3.6 and pytest 9.1.1 were inspected. Docker Compose environment precedence and Docker run reference were retrieved. Local package compatibility and isolated runtime remain unverified. Context7 is unavailable in this session. Local planning links are repository cross-references, not external browse claims.

Exact next action: review the reused evidence table, then answer the three C-04.01 explain-back questions and share your ownership drawing. Next: learner users/notes tables and expected cases for review; then dependency commands and isolated target proof; only then your migration/connectivity attempt. No learner checkbox or Jira status was completed automatically.
