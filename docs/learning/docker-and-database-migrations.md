# What the Docker setup and first migration did

## What is working now

Your migration attempt completed without a reported SQL error. A fresh assistant connection confirmed that public.users, public.notes and public.active_notes exist in merlin_d6, cluster7694311451826794534. Both tables contain zero rows. The installed database weighting function returns4 for a smiley. The three permission groups exist and have no login, superuser or row-security-bypass privileges.

This proves the schema committed and an embedded Python function works. It does not prove every constraint, trigger, permission or cleanup rule behaves correctly. Your earlier probe proved Python can connect; your90unit tests exercise helpers and mocked maintenance. Real SQL acceptance/transaction/limited-role tests remain next. The scheduler has not been started. No login/API/UI exists from this migration.

## Why we used a separate Docker database

Docker runs PostgreSQL in a container: a separate operating-system environment with its own installed programs. Compose groups related resources under a project name. The Day6 project is merlin-d6-20261008105707. It is a practice target for this project's schema, separate from the preserved Sprint0 database.

Its port127.0.0.1:55432 lets your local Python program reach PostgreSQL's internal5432 port. Its network connects services in that project. Its named volume stores the database independently of the container. Its cluster identifier fingerprints the actual PostgreSQL storage, helping detect accidental reuse of Sprint0 storage. Database merlin_d6 is the named database inside that cluster.

The original volume merlin_postgres_data and cluster7691749973399031842 must remain untouched. All schema work here targeted the separate cluster7694311451826794534.

## Commands used and their purpose

| Command or group | What it did | When to use it |
|---|---|---|
| ss -ltn with55432/56379 filter | Checked whether proposed local ports were already occupied | Before initially choosing test ports; not every coding session |
| Shell project/network/port/database overrides | Chose distinct names and endpoints using the existing Compose file | Original isolated-target setup; inspect existing settings before restarting anything |
| docker compose config --quiet | Checked Compose configuration without dumping secrets | Before a proposed setup change |
| docker compose up --wait ... | Created/started selected services and waited for readiness | Initial startup or reviewed service restart, not repeated blindly |
| docker compose ps | Showed service health and published ports | Regular readiness check; use the explicit project name |
| docker compose port postgres5432 | Showed which host endpoint reaches PostgreSQL | When confirming Python/psql connection settings |
| docker inspect mounts | Showed which volume stores PostgreSQL data | Initial isolation proof or after container changes; inspect only needed fields |
| docker network inspect | Confirmed the separate network name | Isolation proof or networking investigation |
| pg_controldata / pg_control_system() | Read the cluster fingerprint | Before risky database operations or after storage changes |
| psql database listing / identity query | Connected and showed database names or current target | Verify where SQL will execute; pager output can be exited with q |
| docker compose exec ... apt-get update | Downloaded package lists inside the disposable container | Before installing missing container packages |
| apt-cache policy | Compared available/installed package versions | Before selecting compatible extension packages |
| apt-get -s install | Simulated dependency installation without installing | Before accepting a package installation plan |
| apt-get install | Installed matching PL/Python plus Python/pip inside the disposable container | Completed prerequisite setup; do not repeat needlessly |
| python3 --version | Confirmed the server-container Python interpreter | Runtime prerequisite check; it is separate from application Python |
| python3 -m pip install --target ... | Installed pinned emoji/regex packages in a shared server-Python directory | Completed Unicode prerequisite setup |
| postgres-user pip show and import checks | Confirmed the database operating-system user could see/load the packages | After runtime installation or rebuild |
| CREATE EXTENSION plpython3u | Enabled Python functions in the specific disposable database | Completed database extension setup; not needed every session |
| psql extension listing | Confirmed the extension was enabled | Extension readiness check |
| app/database_connectivity_probe.py | Connected from your Python application environment and performed a read-only identity query | Connectivity investigation; it does not migrate or test data rules |
| pytest unit suite | Exercised Python validators and simulated worker behavior | After relevant Python changes; not a SQL verification substitute |
| Migration command below | Created the database structure and rules from your existing SQL file | Once for this migration on this target; do not rerun unchanged CREATE statements |

The server has Python3.11.2 for PL/Python; your app uses its own Python3.12 environment. They do different jobs. Matching emoji/regex versions keep the two validators' Unicode rules aligned. The successful migration preflight demonstrated that the embedded server runtime could load its dependencies.

## The migration command, piece by piece

```bash
docker compose -p merlin-d6-20261008105707 exec -T postgres psql -X -U merlin_d6 -d merlin_d6 -v ON_ERROR_STOP=1 --single-transaction -f - < migrations/001_users_notes.up.sql
```

| Piece | Meaning |
|---|---|
| docker compose -p merlin-d6-20261008105707 | Select the explicit isolated project |
| exec -T postgres | Run a command in the existing PostgreSQL service without an interactive terminal |
| psql | Run PostgreSQL's SQL client inside that container |
| -X | Ignore personal psql startup settings, making execution more predictable |
| -U merlin_d6 -d merlin_d6 | Choose the database login role and named database; the login role is distinct from the new permission groups |
| -v ON_ERROR_STOP=1 | Stop at the first SQL error and return failure |
| --single-transaction | Wrap the file in one transaction; commit when successful, roll back migration changes on failure |
| -f - | Read SQL from standard input |
| < migrations/001_users_notes.up.sql | Your Ubuntu shell feeds the existing local file into that input |

The output is PostgreSQL confirming each statement, not a test report:

| Output | What was created or changed |
|---|---|
| DO | Ran the prerequisite check |
| CREATE FUNCTION and result5 | Created the weighted-count helper and confirmed it counted the word check as5 |
| CREATE ROLE | Created owner/app/maintenance permission groups; no login passwords/accounts were created |
| CREATE TABLE | Created empty users and notes tables with their constraints |
| CREATE INDEX | Added structures for uniqueness and efficient listing/cleanup lookups |
| CREATE FUNCTION / CREATE TRIGGER | Added reusable database behavior and automatic checks/timestamp/lifecycle handling |
| ALTER TABLE / CREATE POLICY | Enabled and defined conditional row-level access rules |
| CREATE VIEW | Added active_notes, a filtered view excluding trash |
| ALTER ... OWNER | Assigned ownership of migration objects to the owner group |
| GRANT / REVOKE | Allowed selected operations and removed default permissions |

There is no explicit COMMIT line in your supplied output, but fresh-session object visibility confirms the schema committed. This is schema persistence evidence, not yet committed user/note-row evidence. Empty tables are expected: the migration builds storage rules; it does not create real users, notes or a dataset.

Changes to the database schema live in the volume. Packages installed interactively live in the container layer and are lost if that container is recreated. Therefore a future rebuild needs a reproducible runtime plan; do not assume the database extension will remain usable merely because its catalog record survives in the volume.

## Exact next action

Step3.3 now has successful migration-attempt evidence and the earlier learner-reported probe success. Keep Step4 database test boxes open. Next, prepare one otherwise-valid synthetic user/note case and run it on this isolated target, then test duplicate email, missing owner and title limits with exact constraint results. Follow with actual transaction rollback/reconnect, and only later a reviewed down migration and disposable reapplication. Do not rerun this up migration simply to test connectivity.

No assistant migration or maintenance execution occurred; assistant verification was read-only. Actual minutes remain unknown. This work consumes the existing Day6implementation/verification allocations within360minutes. AWS/DSA deferred; no commit/push/upload.

📚 Learn first: [current migration](../../migrations/001_users_notes.up.sql), [database verification matrix](../testing/users-notes-database-verification.md). The matrix's old dependency blocker/unit counts are historical; this snapshot supersedes those results.

↩ Return: explain the difference between a created table, an inserted record, a passing unit test and a passing database acceptance test. Then begin the first actual insert case.
