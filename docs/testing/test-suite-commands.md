# Run the complete Merlin test suite

This reference covers the current automated tests and fault-injection audits. Run it in Ubuntu/WSL, from the repository root. It does not advance MER-1 step 4.3 or commit a migration undo to your source database.

## Automatic GitHub verification

The same complete suite, all required faults and an additional committed migration roundtrip run on pushes and pull requests. Existing unit tests remain unit tests; real database checks retain their integration coverage. See [the execution map and confidentiality boundary](ci-test-coverage.md). GitHub does not observe local-only commits.

## One command

```bash
cd /home/vipra/Merlin
MERLIN_REDIS_TEST_URL=redis://127.0.0.1:6379/15 .venv/bin/python tools/run_test_suite.py
```

Start the repository's disposable local Redis service first with `docker compose up -d redis`. The integration case fails if Redis is unavailable; it does not silently skip when this URL is set. CI supplies a separate job-owned Redis service. The suite command does not create or remove the Compose service.

The runner checks prerequisites, runs the Python/database baseline, then overlaps independent work while keeping experiments on each database copy serial, and stops launching stages after the first failure. Its exit status is `0` only when every stage and its result validation pass. Missing dependencies fail the run; database tests are not silently skipped. Do not use Python's `-O` option: these audits require enabled assertions. The runner clears inherited `PYTEST_ADDOPTS` so a previous `-k`, `-m` or `--ignore` option cannot silently select only part of the suite.

The automatic runner has seven mandatory stages. Four independently guarded database copies cover two serial SQL case/fault partitions, committed lifecycle checks and migration rehearsal. Each copy has its own disk volume and Unix socket; the original source database stays protected. The canonical Python fault audit overlaps independent database lanes. The ordinary baseline finishes before faults start. Duplicate legacy fault executions and the duplicate focused F077 stage are consolidated into their canonical audits; their standalone commands remain available. Earlier quiz-inclusive measurements are historical; see [application-only scope and actual results](application-test-scope.md). The [final necessity review](test-suite-second-review.md) contains every case/fault decision, conditional migration replay proof and actual timings. Fresh preparation overlaps preflight and rollback-only baselines; faults remain gated on successful baseline and copy startup. Source/copy identity, preservation and cleanup gates remain mandatory.

The SQL audit uses two independent partitions by default. For the diagnostic single-SQL-copy fallback, run `MERLIN_SQL_SHARDS=1 .venv/bin/python tools/run_test_suite.py`. Every case and fault still runs. The final report includes both partition preservation proofs and the exact merged inventory.

Useful options:

```bash
# Check prerequisites without inserting fixtures or injecting faults.
.venv/bin/python tools/run_test_suite.py --check

# Print every stage command without executing it.
.venv/bin/python tools/run_test_suite.py --list

# Save results to a directory that is new or empty.
.venv/bin/python tools/run_test_suite.py --out-dir /tmp/merlin-suite-results
```

The default output is a new `/tmp/merlin-test-suite-...` directory. The terminal prints its exact location. `summary.json` records stages, elapsed seconds per stage, exit statuses, overall PASS/FAIL and the first failure. Each stage has a `.log` file; fault audits also save JSON evidence. Temporary files can disappear after restarting WSL. Copy evidence you want to retain to a deliberately named folder. Historical reports under `docs/testing/` are not overwritten.

## Prerequisites and database safety

Use the existing locked Python environment: Python 3.12 with pytest, psycopg, emoji and regex, plus Git and Docker. The Docker daemon must already be running. The runner does not install packages or apply setup migrations. It starts and removes four private temporary PostgreSQL copies during a full run. Those copies use freshly verified backups and private Docker disk volumes; the original database service is never stopped. A content-verified runtime image is retained for future runs, while database contents and test results are always fresh. A first image capture or changed source runtime adds time. Temporary copies require up to four additional CPUs and 4 GiB of configured memory limits.

Database audits are restricted to the existing empty Day 6 target: database `merlin_d6`, cluster identity `7694311451826794534`, Docker project `merlin-d6-20261008105707`, exposed on `127.0.0.1:55432`. Migration 001 and the whitespace-parity repair 002 must already be applied. The original Sprint 0 cluster and `merlin_postgres_data` volume are not test targets. Keep the scheduler stopped and users/notes empty before starting. Do not change target guards to make a failed prerequisite pass.

Run without another database audit, application client or maintenance worker. The runner prevents a second copy of itself from running simultaneously; it cannot lock out separately launched commands. Do not run these stages with pytest worker parallelism.

Personal learning quizzes are outside this suite. No Node, Playwright or Chromium installation is required by the application test runner. The broader Sprint 0 setup/doctor workflow still checks its existing Node/pnpm foundation. See [the reviewed scope change](application-test-scope.md).

The runner enables `MERLIN_FAST_DB_TESTS=1`: rollback-only SQL cases reuse a guarded connection inside the existing container. Each SQL statement keeps its own execution boundary and original assertions. After every experiment, rollback and session reset remove transaction and session state; target identity and empty tables are checked again. SQL experiments stay serial. Real reconnect, committed lifecycle, multi-client and psql migration checks retain their original separate connections. Native psql requests launch a fresh psql process and connection through one verified container transport; interactive concurrency holders retain separate Docker launches. Timeout and interruption cancel server queries before cleanup. The Python fault stage defaults to 20 isolated workers, bounded by CPU affinity; set `MERLIN_PYTHON_FAULT_WORKERS` from 1 through 20 to benchmark concurrency. The normal run executes the full Python baseline, then each executable mutation runs its validator-pinned witness case and any separately required assertion or safety probes. Each result must match the exact selected-case manifest, fail at the named assertion, and pass inventory/source checks. All retained test cases, fault IDs and assertions remain present; no result is cached. `MERLIN_PYTHON_FAULT_SCOPE=all` runs the full applicable collection per mutation, while socket/process side-effect and shared-fixture mutations keep their dedicated guarded tests. Each fault uses a fresh child process and isolated temporary storage.

SQL case faults and migration rehearsals execute inside transactions that are rolled back. The lifecycle audit also tests committed fixtures and then removes its own fixtures. Migration rehearsals test both synthetic historical-permission branches; neither establishes the genuine pre-001 baseline or authorizes a committed undo. Schema, role and permission fingerprints must match afterward.

If you interrupt a run, inspect the last log and verify target identity and empty tables before retrying. A lifecycle interruption can leave its committed fixtures. Investigate and remove only identified audit fixtures; never use blanket deletion to force a passing preflight.

## Individual stage commands

Use this setup when running stages individually. Choose a new output directory; this example creates one automatically. These commands do not include the runner's report validation, so a zero exit status from a print-only audit is insufficient evidence by itself.

```bash
cd /home/vipra/Merlin
export PYTHONPATH="$PWD"
export PYTHONOPTIMIZE=
export MERLIN_RUN_DB_TESTS=1
export MERLIN_FAST_DB_TESTS=1
export MERLIN_FAST_PYTHON_TESTS=1
suite_output=$(mktemp -d /tmp/merlin-manual-suite-XXXXXX)
```

Run the infrastructure checks first when executing the suite manually:

```bash
.venv/bin/python tools/verify_suite_execution.py
.venv/bin/python tools/verify_python_isolation.py --out "$suite_output/python-isolation-controls.json"
.venv/bin/python tools/verify_native_psql.py --out "$suite_output/native-psql-controls.json"
```

Run the stages in this order, one at a time:

```bash
# 1. Python and PostgreSQL cases, including tools/doctor.py tests.
.venv/bin/python -m pytest -q tests tools/test_doctor.py --tb=short

# 2. Per-case Python fault effectiveness.
.venv/bin/python tools/audit_python_cases.py --out "$suite_output/merlin-python-effectiveness-final.json"

# 3. PostgreSQL cases and injected schema/validation faults.
.venv/bin/python tools/audit_database_cases.py --out "$suite_output/merlin-sql-effectiveness-final.json"

# 4. Committed reconnect/cascade, locking, batch and rollback faults.
.venv/bin/python tools/audit_database_lifecycle.py --out "$suite_output/merlin-lifecycle-effectiveness.json"

# 5. Rollback-only migration round trips, safety gates and repair faults.
.venv/bin/python tools/audit_migration_undo.py --out "$suite_output/migration-undo-results.json"

# 6. Planning-document validation.
.venv/bin/python tools/prd_lint.py docs

# 7. Whitespace errors in tracked changes.
git diff --check
```

Optional diagnostics already covered by the mandatory canonical audits:

```bash
.venv/bin/python tools/check_mutations.py --report "$suite_output/legacy-python-faults.json"
.venv/bin/python tools/audit_database_cases.py --only F077 --out "$suite_output/merlin-sql-F077-final.json"
```

Without `MERLIN_RUN_DB_TESTS=1`, ordinary pytest runs skip the opt-in database cases. The complete runner always enables them. `git diff --check` checks tracked changes; it does not inspect every untracked file. The documentation validator currently checks the 25 numbered planning Parts, not every Markdown file. Read its warnings and unresolved learning links even when it returns zero.

## Reading PASS and FAIL correctly

A baseline must pass before a fault experiment counts. A valid injected defect should cause the relevant test to fail: the audit labels that **DETECTED**. An injected defect that leaves all relevant tests passing is **SURVIVED**, and requires investigation. A broken mutation experiment is **INVALID**, not proof that an application defect was caught.

The runner checks tests/suite-inventory.json for complete, duplicate-free reviewed case and fault inventories, validates source/scope hashes and underlying outcomes, and requires every audited Python, SQL and lifecycle case to demonstrate fault detection. Intentional changes require review and an explicit inventory update; never regenerate the inventory automatically merely to obtain PASS. It requires SQL faults to be detected somewhere in their selected suite; an unrelated case surviving a SQL fault is expected and is not counted as detection. Unexpected invalid, unapplied, timed-out or surviving faults fail the combined run.

Four structurally identified Python import-harness mutations are recorded as EXCLUDED_INVALID and not executed as application faults: `ast-database_connectivity_probe-30-11`, `ast-notes_maintenance-76-42`, `ast-doctor-229-52`, and `ast-prd_lint-181-88`. Their names are retained in the summary. They are not counted as valid detected faults. No other invalid Python fault is exempt. Three proven duplicates are recorded as ALIAS: two exact faulty-AST duplicates and one source/hash-guarded Doctor semantic duplicate, each naming its canonical executed fault. Five real terminal controls still exercise prompt isolation and true timeout rejection.

The application-only inventory records 1,195 Python/database tests plus three subtests. This includes 467 provider cases. It retains all 297 canonical Python faults, 607 SQL pairings and applicable migration/lifecycle checks. The sole removed Python node was the quiz-only link parameter. See [current scope and results](application-test-scope.md). Repeated migration/fault executions are not additional distinct application tests. Authenticated API cross-user denial remains pending until that boundary exists.

Runtime diagnostics (`tools/doctor.py`) and environment setup scripts are separate operational tools. They are not additional test cases; the doctor's automated cases are included in stage 1. The report renderer `tools/write_test_audit.py` formats evidence and is not required to execute or validate the suite.

## Current verification and historical measurements

The previous ten-stage measurements included personal quiz/browser work. They are historical and do not describe the current seven-stage scope. See [application-only verification](application-test-scope.md) for current measured runs. Worker limits, target guards, isolation, fresh execution and cleanup remain required; no reduced runtime is claimed until observed.

For the separate Day 6 4.3 acceptance proof, run the focused committed migration rehearsal below. It captures a real pre-migration baseline on fresh private storage and leaves your source database unchanged. The routine fast suite retains its rollback-only migration fault checks; this additional committed rehearsal is not silently added to its runtime.

```bash
.venv/bin/python tools/verify_migration_roundtrip.py --out /tmp/merlin-migration-roundtrip-results.json
```

See [4.3 results and preservation proof](database-step-four-verification.md#43-undoreapplication-current-review).

The fast configuration previously passed in **52.98 seconds**. Your subsequent Ubuntu run used exactly those source files but exposed an interactive password prompt in a main-guard mutation. Fault workers now detach from terminal input; four mandatory pseudo-terminal controls verify both input paths and preserve real timeout failure. The repaired complete command passed **12/12 stages in 53.36 seconds with a terminal attached**, including **41.16 seconds** of database work. Every original case, fault and detection set remains; all sixteen coverage comparisons passed. See [terminal failure and repair](test-suite-performance.md#terminal-only-probe-fault-timeout-repair) and [durable results](terminal-fault-isolation-results.json). Timings vary with machine load.

To additionally repeat every unrelated Python case for every fault, use the slower full-collection mode:

```bash
MERLIN_PYTHON_FAULT_SCOPE=all .venv/bin/python tools/run_test_suite.py
```

Preflight runs 126 coordinator/result controls, five real-terminal Python isolation controls, and native psql equivalence, fresh-connection, large-script, timeout, interruption and preservation checks. Native checks use the guarded disposable database; coordinator and terminal isolation controls do not touch it. Fault workers receive EOF instead of inheriting your terminal input, and are detached from the controlling terminal. An unexpected timeout still fails the suite; the existing four named invalid import mutations remain the only exclusions.

## Earlier verified run

On October 11, 2026, the combined command completed all **12 stages with PASS**, exit status **0**, in **782.24 seconds** (about 13 minutes). The run passed 735 Python/PostgreSQL cases plus three subtests, 42 quiz cases, all 16 browser workflows and five lifecycle cases. Fault-report validation passed, including 55 targeted Python faults, 235 valid per-case Python faults and 35 quiz faults. All 389 SQL cases demonstrated detection. Four known invalid Python import mutations were excluded and named in the summary.

Migration rehearsals passed both synthetic permission branches, with 388 SQL cases per branch, plus 14 gate checks, three concurrency checks and 17 repair checks. The installed database fingerprint and empty target were preserved. These are repeated case executions and focused migration observations, not additional distinct application tests.

No application failure or unexpected surviving fault was found in this run. Documentation checks reported zero errors, one planning warning and 27 unresolved verification items. The genuine pre-001 permission baseline remains pending for 4.3.

The earlier durable [run summary](test-suite-run-results.json) records the actual stages and excluded mutations. Full logs and raw audit reports are in `/tmp/merlin-test-suite-7igv087_/`; retain them separately if needed. Validator checks also confirmed that failed baselines, surviving faults, missing detection, preservation failures and a falsely labelled migration PASS are rejected.

Optimization and your reported failure: [test-suite speed and failure investigation](test-suite-performance.md).

📚 Learn first: [existing per-case effectiveness evidence](case-effectiveness-audit.md), [database verification and pending undo prerequisites](database-step-four-verification.md), and each stage's `--help` output where available.

↩ Return: run `--check`, run the full command, read `summary.json`, and investigate the first failure before proceeding with MER-1 4.3.
