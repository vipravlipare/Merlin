# Test-suite failure and performance investigation

Latest MER-12 local run: all seven stages PASS in **57.397 seconds** (60-second limit), with 1,288 Python tests +3 subtests, all 341 executable Python faults, 392 SQL cases, 624 SQL case/fault pairs, SQL/lifecycle/migration gates, source-preservation and cleanup checks. The run used temporary loopback Redis; service startup and teardown were outside the runner's elapsed timer. One runpy warning remains. Runtime varies with host load; this result clears the cap by 2.603 seconds. Earlier performance measurements below are historical.

Hosted cumulative CI also passed for code and documentation commit `430193fb1103b96edbd09768b4553370a93ed3a0`: [run 40161140540](https://github.com/vipravlipare/Merlin/actions/runs/40161140540). All five required jobs passed: `prepare`, `database`, both Python fault shards and final `setup`. CI service startup and queue time are outside the 60-second test-lane limit.

## October 25, 2026: MER-12 auth additions and full run

The final seven-stage run completed in **57.397 seconds**. Python baseline: **1,288 passed plus 3 subtests**, no skipped cases. Python mutation audit: **899 inventoried cases** and **341/341 executable faults detected** at required assertions; zero survived, invalid, timed out or unapplied. SQL audit: **392 cases** and **624 case/fault pairs** validated. Lifecycle, migration rollback/refusal/repair, source preservation and disposable cleanup passed. The suite report is `/tmp/merlin-test-suite-_uss_gpu/summary.json`; the summary status is `PASS`, and its seven stage records all pass.

The Redis integration case ran against a temporary Redis container bound to loopback. The container and its dedicated network were removed after the run. Redis service setup was outside the suite's 57.397-second timer, as GitHub Actions service startup also is. The run used isolated disposable PostgreSQL copies and preserved the source. One `runpy` warning remains in the legacy-entrypoint test. No speed guarantee follows from this single run; the margin to 60 seconds is 2.603 seconds.

Earlier retained configuration and measurements: [final combined optimization decision](#final-combined-optimization-decision). Earlier sections below preserve the investigation history.

## October 24, 2026: verified fault scope and full run

The prior MER-12 run took **103.891 seconds**: every stage passed, but the 60-second cap failed. It ran each fault across its dependent test modules. Reducing the worker count to eight was slower on this 20-CPU-affinity host: that full run took **118.153 seconds**. More workers alone did not address the repeated collection and unrelated case executions.

The normal audit now first runs the full Python baseline, which executes all **896 inventoried cases plus 3 subtests**. It then runs each of the **340 executable faults** against its validator-pinned test and assertion. The validator also requires the separately mapped health/auth/provider assertion where applicable; socket/process side-effect faults retain their three dedicated trap cases. The baseline and each fault's exact selected-case manifest are checked, every worker still runs in a fresh process, and the existing full-collection mode remains available. No case, fault ID, assertion or timeout was removed. This changes the recorded incidental case-by-fault matrix: the current run reports 208 cases with at least one demonstrated fault, while every mutation must still fail its required named check. Cases without an assigned mutation still must pass the full baseline.

An initial scope prototype failed closed: the parent manifest was narrowed while the serialized worker request still selected the broader suite, so 311 mutations were marked `INVALID`. The request was fixed and regression-tested. A second prototype exposed 35 mutations whose designated witness differed from a separate required API/provider assertion; those cases were added to the run selection. The final report contains 340 `DETECTED`, zero `SURVIVED`, `INVALID`, `TIMEOUT` or `UNAPPLIED`, plus the existing three aliases and four known invalid-import exclusions.

The exact-scope full run took **58.614 seconds** with 20 workers. A repeat at **8 workers** took **61.669 seconds** and failed only the runtime cap; all seven test/fault stages passed, including 340 detected mutations. The accepted **20-worker** run took **56.374 seconds** after auth schema preparation was parallelized across the three independent disposable PostgreSQL copies. Its Python baseline took 17.076s, Python faults 25.084s, SQL faults 9.733s, lifecycle 8.127s and migration checks 10.618s; setup, isolation controls and cleanup were included. Source fingerprint was preserved and cleanup passed. It clears the 60-second gate on this machine by **3.626 seconds**. Two other exact-scope 20-worker runs measured 58.614s and 59.002s, so host-load variation remains material.

Vertical scaling to the 20 CPU slots available to the Python workers beat eight workers for this workload. A local horizontal trial ran two 10-worker shards concurrently and merged them: **24.078 seconds** parallel wall time, **347 fault records** (340 executable faults plus existing aliases/exclusions), all 340 detected and **896 cases** validated. The full single-run Python fault stage measured 25.084 seconds while sharing the host with SQL/lifecycle/migration audits, so those timings are not a controlled end-to-end comparison. Each local shard reruns the complete baseline on the same CPU pool. Hosted CI already distributes the shards onto two independent jobs; the simpler single coordinator remains in the local full runner until a same-load complete-suite trial demonstrates an end-to-end gain. No Docker CPU or memory limit was raised. The two rejected experiments above retain all failure evidence. All baseline cases still pass; each fault still must fail its intended assertion and any separate required probe. The current exact-witness matrix records 208 cases with at least one assigned mutation; the other baseline cases are still executed, but no cross-case mutation effect is claimed for them.

Verification evidence: `/tmp/merlin-test-suite-au71i16g/summary.json` and its case/fault reports; `/tmp/merlin-fault-shards/merged-report.json` contains the horizontal merge. These paths are local run evidence, not committed artifacts.

## Your reported failure

The run in `/tmp/merlin-test-suite-r5zafcu4/` stopped with `No module named 'tools'`. The migration audit process returned exit status zero: both round trips, safety gates, concurrency checks and repair checks passed. Its result validator then failed to import `tools.audit_database_cases`.

Running `.venv/bin/python tools/run_test_suite.py` puts the `tools/` directory on Python's import path. It does not automatically put the repository root there. The runner previously set `PYTHONPATH` for child processes but did not fix its own import path. That explains why imported-module validation worked during earlier checks while direct terminal execution failed later. This was a runner defect, not a failed migration assertion. Documentation and whitespace stages were not reached in your run.

The runner now explicitly adds its repository root to `sys.path`. A regression check reproduced the original missing-module error with the direct-script import path, then successfully validated your unchanged migration report after the fix. The [original failure summary](test-suite-failure-results.json) is preserved.

## What makes the suite faster

The SQL baseline and fault audits previously launched Docker Compose, a psql process and a database connection for almost every experiment. Your entire run took 791.15 seconds. Its Python/PostgreSQL baseline alone took 137.99 seconds; SQL fault checks consumed roughly another six and a half minutes, measured from stage log completion times.

The complete runner now enables a reusable database test session for rollback-only SQL cases. It uses Python and PostgreSQL's existing libpq library inside the same disposable container; no packages, credentials or services are added. It still executes every original SQL statement, assertion, case baseline and case/fault pair. Statements are not merged into one query. A quoted-string/comment lexer preserves the original statement text, including dollar-quoted function bodies and escaped semicolons.

After each experiment, failed or open transactions are rolled back. `DISCARD ALL` resets session roles, settings, temporary objects, prepared statements and advisory locks. Target identity and empty users/notes are checked again. Database experiments remain serial. The suite closes the reusable connection before tests that require a real reconnect. Committed lifecycle, multi-client locking and psql migration behavior keep their original connections and commands.

The first optimization ran the full Python collection in a fresh interpreter per fault, using up to eight workers bounded by CPU affinity. The latest optimization below reduces process startup and unrelated repetitions. No results are cached and no assertions are removed.

The old per-experiment Docker/psql transport remains available for individual SQL checks: unset `MERLIN_FAST_DB_TESTS`, or set it to `0`. The complete runner deliberately enables the optimized transport. All twelve stages remain included.

## Failure caught while optimizing

The first transport prototype sent an entire experiment as one server query. This caused **F081** (content edits advance server edit time) and **F094** (returning to blank restarts its countdown) to fail: PostgreSQL treated the statements as sharing one statement timestamp. The initial trial recorded **387 PASS / 2 FAIL** in 6.23 seconds.

The fix was to submit each original statement separately, keeping transaction boundaries and first-error behavior. Neither assertion nor application function was changed. The corrected transport passed **389/389** database cases, including real reconnect, in **6.82 seconds**. Additional comparisons matched original psql exit statuses and stdout for successful requests, expected errors, intermediate mutation-ready markers, temporary objects, role changes and rollback cleanup. Lexer checks covered nested comments, quoted semicolons, escaped quotes, exact text retention and rejected unterminated input.

## First complete optimization

The complete terminal command passed **12/12 stages** in **184.91 seconds** (about **3 minutes 5 seconds**), compared with your **791.15 seconds** (about **13 minutes 11 seconds**). That is **4.28 times faster**, a **76.63% reduction** on this machine. Timing depends on the machine and concurrent activity.

| Stage | Optimized seconds |
|---|---:|
| Python and PostgreSQL baseline | 8.765 |
| Quiz baseline | 0.094 |
| Targeted Python mutations | 8.380 |
| Full Python case/fault audit | 91.554 |
| SQL case/fault audit | 14.740 |
| Focused timestamp audit | 0.589 |
| Quiz fault audit | 1.300 |
| Browser cases and faults | 8.621 |
| Database lifecycle cases and faults | 19.518 |

Migration rehearsals, documentation checks, whitespace checks, preflight and report validation account for the remaining time. All stage timings are stored in the [performance results](test-suite-performance-results.json).

Comparisons against your original reports confirmed the exact same Python and quiz case inventories, fault statuses and per-case detection sets. SQL comparisons matched every case/fault recipe and detection status, including unrelated surviving pairs. The targeted mutation report matched exactly. Browser and lifecycle case inventories matched, and every baseline and mutation passed its validator. Migration source hashes, both 388-case round trips, 14 gate checks, three concurrency checks and 17 repair checks matched. That first optimization removed no test or fault experiment.

The full run returned exit status zero, with no new application failure. Four known invalid Python import mutations remain explicitly excluded. The document validator still reports one planning warning and 27 verification items. Storage fingerprints, target identity and empty users/notes were preserved. 4.3 remains pending the genuine pre-001 permission baseline.

Full raw evidence is in `/tmp/merlin-test-suite-61blqqhn/`. The durable performance JSON preserves the summary and coverage comparison; temporary raw files need separate retention if wanted.

## Second optimization: 82.68 seconds

On October 11, 2026, the unchanged full command passed all twelve stages in **82.68 seconds**, compared with **184.91 seconds** after the first optimization and **791.15 seconds** in your reported run. This is **2.24 times faster** than the previous version and **9.57 times faster** than the original. Measurements include preflight and validation; hardware and concurrent activity affect runtime.

The runner overlaps an independent Python/browser lane with a database lane. Database stages remain serial, including migration rehearsals. Baselines finish before fault stages start. A failure stops new stages; an already active stage finishes its cleanup. Interruption signals whole process groups and waits for cleanup before escalating termination. Three adversarial runner checks verify overlap, database serialization, rejection of a zero-exit invalid report, and interrupted-child cleanup. These controls run during preflight.

Each Python fault runs in a fresh child process forked from a parent that has loaded pytest but has not imported application modules. Children are never recycled between experiments. This removes repeated interpreter and pytest startup. Recognized PRD-linter subprocess requests execute the actual CLI script in another fresh child, retaining arguments, working directory, output and exit status. Other commands retain normal subprocess execution; the ordinary baseline still tests the actual subprocess path. Forking refuses a multithreaded parent.

Every Python baseline case and all 239 mutation recipes remain included: 235 valid faults are detected and the same four known invalid import mutations remain explicitly excluded. Each fault now runs all dependent test modules rather than repeating unrelated modules. A transitive import walk computes dependencies. Uncertain dynamic imports, unknown targets, shared fixtures, and new or changed test modules conservatively run against every fault. Reviewed modules are pinned by source hashes; changing one cannot silently inherit an outdated scope. Each experiment must collect exactly its expected case manifest. Every case retains its **exact previous fault-detection set**, verified against the earlier full-collection report.

This intentionally reduces unrelated Python case/fault repetitions. For the slower full Cartesian Python audit, use:

```bash
MERLIN_PYTHON_FAULT_SCOPE=all .venv/bin/python tools/run_test_suite.py
```

SQL case/fault pairs are unchanged. Native reconnect and migration checks still launch separate psql processes; their Docker commands now use a cached container identity only after checking that the container is running and its project/service labels match the disposable target. Target and storage guards remain mandatory.

An early fork experiment exposed a pytest temporary-directory cleanup race: one extra mutation was INVALID and one case lacked demonstrated detection. Each experiment now has its own temporary directory. The fault was rerun and detected; it was never added to the invalid-fault exclusions. No application assertions were changed to fix this harness failure.

The final comparison matched all Python and quiz case detection sets and fault statuses; every SQL pair and baseline; the complete legacy mutation report; browser and lifecycle case outcomes; migration source, round trips, gates, repairs and concurrency checks; and the preserved database fingerprint. All 798 baseline case executions plus three Python subtests remain covered. No new application failure was found. Documentation still reports one planning warning and 27 verification items. MER-1 4.3 remains pending its genuine historical permission baseline.

See [latest durable results](test-suite-fast-run-results.json) for timings, comparisons and runner-control evidence. Raw logs are in `/tmp/merlin-test-suite-fyhssnxa/`. The previous result file is retained. Future features and faults add real work; this improvement does not guarantee constant runtime or coverage of every possible bug. New or changed modules deliberately use conservative full fault scope until reviewed.

## Latest optimization: 59.36 seconds

The final full run on October 11, 2026 passed **12/12 stages in 59.36 seconds**, compared with **82.68 seconds** previously: a **28.2% runtime reduction**, or **1.39 times faster**. This did not achieve another threefold speedup. The suite is approximately **13.33 times faster** than your original 791.15-second run. No constant speedup for future features is promised.

Eight-worker and four-worker complete trials passed in 67.28 and 64.71 seconds respectively. Six workers gave the best measured balance, completing the Python fault stage in 26.05 seconds and the SQL fault stage in 22.28 seconds. Lifecycle faults took 8.51 seconds and migration rehearsal took 13.22 seconds. Trials also include the corrected and streamlined preflight, so they are observations rather than a controlled isolated comparison of worker counts. Machine load affects these measurements.

All sixteen final coverage comparisons passed: Python and quiz inventories and exact detection sets; all valid/invalid fault statuses; exact selected-case manifests; all SQL pairs and baselines; the legacy mutation report; browser/lifecycle outcomes; migration source, round trips, gates, repairs and concurrency; and preserved fingerprints. All 798 baseline executions plus three subtests remain. The same four invalid import mutations remain excluded; no new exemption was added. No new application failure was found. The two optimization defects above were repaired in the transport and covered by mandatory regressions.

[Durable final results and failed-prototype evidence](test-suite-native-run-results.json) retain the full summary, comparisons, controls and source fingerprints. Raw logs are in `/tmp/merlin-test-suite-7p7wudjy/`. Previous evidence files remain available. The complete terminal command is unchanged; no migration was committed and MER-1 4.3 remains pending.

This revision removes repeated Docker CLI startup from native psql checks. A verified container process receives each unchanged psql command and SQL script. It launches a **new psql process and PostgreSQL connection for every request**, captures stdout, stderr and exit status, and closes that process before accepting another request. It holds no database connection between requests. Interactive concurrency holders still use their original separate Docker/psql processes. Migration scripts, commits used by lifecycle fixtures, transaction boundaries, target checks and per-experiment fingerprint checks are unchanged.

Python fork parents now preload pytest's built-in plugin modules and the ordinary emoji, regex and psycopg dependencies. They still never import application modules or execute tests. The Python case/fault stage also uses a measured worker balance with a conservative cap of eight workers and the process CPU-affinity limit. Reducing contention can speed the database lane even when individual Python experiments take longer. The 55 legacy mutations now use the same fresh-process mechanism and separate temporary directories as the other Python mutations; their standalone real-exec fallback remains available. Baselines still run normally. SQL scanning skips ordinary text and dollar-quoted bodies without rewriting statements. Two thousand randomized comparisons matched the previous lexer, including malformed input rejection.

The first timeout regression revealed that killing a psql client can leave its server query running until PostgreSQL observes the disconnect. The native transport now sends SIGINT, allowing psql/libpq to cancel the query, and requires ON_ERROR_STOP so no later statement can commit. It waits for cleanup, fails if cancellation does not finish, and also cancels when the requesting process disconnects. Regression checks verify that both timed-out and interrupted server connections disappear. These checks are mandatory preflight, together with native/direct stdout, stderr and exit equivalence, fresh connection identity, container rejection and preserved storage. The failed prototype was not accepted based on a green application suite alone.

The first full run with cancellation also exposed a compatibility defect in the container Python: repeated `communicate()` calls stopped writing a partially delivered large migration script. The migration stage timed out; its final fingerprint was preserved, and later stages correctly remained pending. Every native request now receives its unchanged script through a fresh temporary input file, eliminating partial-pipe retries. Mandatory preflight delays execution before a 400,000-character SQL comment larger than pipe capacity, then verifies both result rows. The comment adds transport volume without repeating thousands of unrelated database queries. The timeout remains 45 seconds; it was not increased to hide the failure.

No further case selection was introduced in this revision. The previous conservative dependent-module scopes remain; the full-collection option still runs every Python case for every fault. All SQL pairs, application assertions, real lock timeouts and migration safety checks remain.

## Additional optimization investigation

On October 11, 2026, further complete trials tested PostgreSQL pipeline transport and narrower Python scopes. A pipeline/module-scope run passed all twelve stages in **58.88 seconds**. A pipeline/function-scope run passed in **60.05 seconds**. Both retained exact Python/quiz detection sets, every SQL pair and all migration observations when compared with the earlier full-collection evidence. Neither demonstrated a meaningful improvement over 59.36 seconds.

Pipeline mode submits separate ordered statements before waiting for prior results; errors skip subsequent queued statements until synchronization. See the official [PostgreSQL 17 pipeline documentation](https://www.postgresql.org/docs/17/libpq-pipeline-mode.html), checked October 11, 2026. The trial used nonblocking send/receive, verified timing and first-error behavior, and tested large buffers, state reset and cancellation. Its first diagnostic failed because pipeline statuses were initially misidentified; symbolic libpq status names fixed that prototype. All controls subsequently passed. The pipeline implementation and controls were removed because their extra complexity and preflight time did not produce a meaningful complete-suite gain.

The function-level trial computed structural dependencies and used reviewed source guards, rather than selecting from previous fault outcomes. Its exact detection sets matched, but runtime did not improve. That extra function-scope implementation was also removed. The retained runner continues to use whole dependent test modules.

A small dependency-analysis correction remains: `subprocess.CompletedProcess` and `subprocess.TimeoutExpired` construct data or exceptions, rather than launch commands. The analyzer distinguishes these from actual execution functions. The reviewed doctor's setup-client boundary is source-hash guarded; changes restore conservative full scope. Doctor cases therefore need not repeat for unrelated application faults. Warm dependency imports now also include unittest.mock and tomllib. Every baseline, fault and assertion remains; no application or migration source was edited during this investigation.

The final simpler runner passed **12/12 stages in 58.50 seconds**, effectively unchanged from **59.36 seconds**. All sixteen coverage comparisons passed. The serial database lane alone took **44.21 seconds**: SQL fault cases 22.19, timestamp checks 0.92, lifecycle checks 8.08 and migration rehearsal 13.02. The Python case/fault stage took 23.63 seconds. These timings identify the remaining substantial work; no threefold improvement was demonstrated. The final retained changes are the small dependency-analysis correction and warm standard-library imports, rather than either experimental subsystem.

[Additional durable results](test-suite-additional-run-results.json) preserve the final summary, both experimental summaries, exact coverage comparisons and source fingerprints. Raw final logs are in `/tmp/merlin-test-suite-o4cr02ua/`. All 798 baseline executions plus three subtests and the complete fault inventory remain; the same four known invalid import mutations remain excluded. No new application failure or unexpected surviving fault was found. Documentation retains one planning warning and 27 verification items. MER-1 4.3 remains pending.

These results do not establish another threefold speedup. Real database validation, transaction behavior, migration rehearsals and isolated Python fault execution remain substantial work. A faster foundation does not make future test growth free. No test result caching, assertion weakening, shorter real lock timeouts or database-stage parallelism was introduced.

## Database profiling and scheduling investigation

The requested further twofold or threefold database speedup was **not achieved**. The retained change moves migration rehearsal and lifecycle checks before the SQL fault audit, with six Python fault workers. Both normal baseline collections still finish before faults begin, and database stages never overlap. The scheduling controls now exercise this order, including first-failure reporting and interruption cleanup.

| Measured configuration | SQL fault audit | Migration rehearsal | Database lane total | Complete suite |
|---|---:|---:|---:|---:|
| Fresh original-order baseline, six workers | 24.59 s | 13.10 s | 46.51 s | 62.09 s |
| Retained reordered stages, six workers | 14.53 s | 19.41 s | 44.25 s | 58.75 s |
| Reordered stages, three workers | 14.58 s | 16.20 s | 38.75 s | 67.40 s |

The largest SQL audit improved by 1.69 times against this session's baseline, but migration checks became slower. The retained database lane improved only about 4.9%. The previous 58.50-second complete run was slightly faster than this retained run, so these single measurements do not establish a reliable overall improvement. Three workers reduced database contention further but extended Python fault execution to 37.72 seconds; that worker setting was rejected for the complete-suite default.

A standalone profiled SQL audit passed all 389 cases in 14.24 seconds, with every case detecting a fault and the fingerprint preserved. About 12.03 seconds of the host profile was waiting for responses; this includes database execution and transport, not just network delay. The container has a one-core CPU quota and 1 GiB memory limit. Approximately 0.092 seconds of additional throttling was observed across the standalone profiling interval, which does not support CPU-quota throttling as its principal bottleneck. Table statistics reported no live or dead rows, with users approximately 0.56 MB and notes 1.74 MB; no vacuum, table rewrite or resource-limit change was performed.

The installed `note_weighted_length` function repeats two package-version lookups for every call. A read-only rollback microbenchmark of 1,000 iterations measured **954.58 ms** for those lookups and **6.25 ms** for counting short varying ASCII strings with the existing emoji and grapheme algorithm. Calling the actual database function with 1,000 distinct short inputs took **1,000.86 ms**. This identifies a real cost in that function, but does not establish its share of total suite time or performance for long bodies. The constant-input comparison was folded during query planning; it was not treated as 1,000 function executions.

[Python's package metadata reference](https://docs.python.org/3.12/library/importlib.metadata.html) describes the installed-distribution lookup. [PostgreSQL's PL/Python sharing reference](https://www.postgresql.org/docs/17/plpython-sharing.html) documents per-function `SD` storage. These suggest investigating bounded caching through a separately reviewed migration, with explicit missing-package, wrong-version, stale-cache, function-replacement and backend-lifecycle regressions. No cache was injected into the tests, no package validation was bypassed, and the applied migration sources and installed definitions remain unchanged. [PostgreSQL's vacuuming reference](https://www.postgresql.org/docs/17/routine-vacuuming.html) explains storage maintenance; current observations did not establish a vacuum-related problem. Official references checked October 11, 2026.

Both reordered full trials passed all 12 stages and all sixteen exact coverage comparisons against the earlier full audit. All 798 baseline executions plus three subtests, all fault recipes, SQL pairs, migration gates, two 388-case round trips, real reconnect and lock checks remain. The same four known invalid Python import mutations are excluded; no new exclusion was added. No new application failure was found. Final read-only verification preserved identity, empty tables and fingerprint `37acb7647f0a140d3047bf62d64e6209`.

Durable evidence: [retained scheduling results](test-suite-database-scheduling-results.json), [rejected three-worker trial](test-suite-database-worker-trial-results.json), and [database profile](database-stage-profile-results.json). Raw full runs are `/tmp/merlin-test-suite-y4meekw6/`, `/tmp/merlin-test-suite-29bnz9pc/` and `/tmp/merlin-test-suite-k3sx62g0/`. The complete terminal command is unchanged. MER-1 4.3 remains pending its historical baseline.

📚 Learn first: [terminal commands](test-suite-commands.md), [PostgreSQL libpq result processing](https://www.postgresql.org/docs/17/libpq-async.html), and [PostgreSQL DISCARD](https://www.postgresql.org/docs/17/sql-discard.html). Both official references were checked October 11, 2026.

↩ Return: run the unchanged complete-suite command, inspect the first failure or final PASS, and use per-stage seconds in `summary.json` to compare runtime on your machine.

## Final combined optimization decision

The retained combined configuration passed all **12 stages in 52.98 seconds**, with **40.56 seconds** for the complete database work, including fresh backup, copy creation, isolation controls and cleanup. This reaches the requested approximately 54-second complete-suite target. The earlier 30-second database target was not reached. Timings vary with machine load; these are measured runs, not runtime guarantees.

| Configuration | Complete database work | Complete suite |
|---|---:|---:|
| Earlier simplest runner | 44.21 s | 58.50 s |
| Three isolated copies, six Python workers, sequential preparation | 40.45 s | 60.21 s |
| Three isolated copies, concurrent preparation | 39.36 s | 61.59 s |
| Private disk volumes, four Python workers | 34.86 s | 66.96 s |
| Two SQL partitions, six Python workers | 42.42 s | 63.92 s |
| Two SQL partitions, four Python workers | 36.49 s | 68.48 s |
| Two SQL partitions, two CPUs per copy | 40.82 s | 62.73 s |
| Three private disk copies, overlapping prerequisites | 41.21 s | 56.82 s |
| Independent Python and quiz fault lanes | 40.82 s | 53.41 s |
| Final prerequisite-control trial | 40.56 s | 52.98 s |

The first isolated-copy attempts improved database elapsed time but slowed the complete suite. They were initially rejected and their experimental images removed. Your subsequent request explicitly asked to combine the faster database work with the faster remaining tests. The retained configuration does that: the full Python case/fault audit starts independently of the legacy Python, JavaScript and browser fault sequence. Both ordinary baseline collections still finish before any fault is launched. The source code and application files are never rewritten by these fault processes.

Prerequisite scheduling checks and runtime checks now overlap the serial database transport/preservation checks. Every prerequisite remains mandatory and must finish successfully before baseline tests start. Timeout limits remain unchanged. The final control trial also ran independent coordinator scenarios concurrently in separate temporary folders; the selected measured configuration is the faster of the two complete passing runs. Failure, timeout, zero-exit invalid evidence, target assignment and interrupt cleanup controls remain enabled.

The SQL fault audit, lifecycle checks and migration rehearsal run on three independent PostgreSQL copies. The focused timestamp audit follows the SQL audit on its copy. Each copy uses a private Docker disk volume, private Unix socket, disabled external networking, a one-CPU limit and a 1 GiB memory limit. The source remains running with its original one-CPU/1 GiB limits. PostgreSQL fsync, full-page writes and synchronous commits remain enabled. A newly verified physical backup supplies current schema/data on every run; no test results or database snapshots are reused across runs. Only a content-verified runtime image containing the installed code/dependencies is cached. The first capture or a changed runtime adds startup time.

The official [PostgreSQL base-backup reference](https://www.postgresql.org/docs/17/app-pgbasebackup.html) describes full cluster backups and WAL collection. The runner includes required WAL, verifies the backup using [pg_verifybackup](https://www.postgresql.org/docs/17/app-pgverifybackup.html), and rejects custom tablespaces before a plain backup could write their original paths. [Docker's volume guidance](https://docs.docker.com/engine/storage/volumes/) recommends volumes for high-performance I/O; the retained copies have independently owned volumes and never mount the source database volume. Official references checked October 11, 2026.

On this machine, copies inheriting Docker Desktop forwarding labels took approximately three seconds per inspect/exec operation. Clearing stale forwarding labels on copies reduced measured inspect time to about 0.04 seconds. The source labels and published port were unchanged. Actual port bindings, networking, resource caps, storage ownership and runtime content are checked before any fault runs. Twenty-one real isolation controls include a deliberately wrong function in one live transaction: the source and both other copies must still return the correct result. The wrong function is rolled back and checked again before the audits start.

The restoration trial failed because one control still referenced the removed fourth SQL copy. The run correctly reported database-isolation failure, rolled back its live fault, cleaned its copies and preserved the source. The fix makes the control verify all other configured copies dynamically. No assertion was weakened and no application fault was reclassified to obtain a passing run. Earlier failed startup/guard prototypes and their first failures remain in the durable results.

Every passing retained run matched all **16 exact coverage comparisons** against the earlier complete audit: all 798 baseline executions plus three subtests, all original fault recipes and detection sets, all SQL case/fault pairs, committed reconnect behavior, real lock checks, two 388-case migration round trips, 14 gates, three concurrency checks and 17 repairs. The same four known invalid Python import mutations remain explicitly excluded; 50 unrelated SQL pairs remain expected survivals. No new application failure or unexpected surviving fault was found. The source fingerprint remains `37acb7647f0a140d3047bf62d64e6209`, with the original identity and empty tables preserved. Applied migration definitions and application code were unchanged during this optimization.

The extra SQL partitions and two-CPU copy configuration remain removed. The original serial database fallback remains available for diagnosis with `MERLIN_DB_ISOLATION=0`; it also retains every stage and assertion. The default one-command runner uses the selected combined configuration. MER-1 4.3 still requires its actual historical pre-001 permission baseline; these rehearsals do not complete that requirement. Authenticated cross-user API denial remains pending its ownership boundary.

Durable evidence: [complete trials, first failures and retained results](database-optimization-trial-results.json). Selected raw reports: `/tmp/merlin-test-suite-ihpvspwa/`. Documentation validation reports zero errors, one existing planning warning and 27 verification items.

📚 Learn first: [complete terminal command and prerequisites](test-suite-commands.md), [PostgreSQL base backups](https://www.postgresql.org/docs/17/app-pgbasebackup.html) and [Docker volumes](https://docs.docker.com/engine/storage/volumes/).

↩ Return: run the unchanged complete-suite command, read PASS/FAIL and the first failure in its summary, and compare total elapsed time plus the database wall time under `execution.database_isolation`.

## Terminal-only probe fault timeout repair

Your run in `/tmp/merlin-test-suite-6z7owxi4/` used exactly the retained fast source files: every recorded Python source hash matched the 52.98-second run. It used six Python fault workers, independent Python/quiz lanes and three isolated database copies. Its database work passed in **39.83 seconds**. The suite correctly failed because `ast-database_connectivity_probe-21-11` timed out; documentation and whitespace checks remained pending. All 349 Python case/subtest rows still demonstrated fault detection, and all 235 valid Python faults were detected.

That artificial mutation reverses the probe's `if __name__ == "__main__"` comparison. Importing the mutant therefore starts its interactive password prompt before its tests can run. A forked worker had already detached from its controlling terminal but still inherited an open terminal file descriptor as standard input. The password prompt waited for your input until the existing 45-second fault timeout. Earlier noninteractive runs encountered EOF immediately and recorded the same mutation as one of the four already named invalid import faults. The timeout was not CPU contention or a failing application assertion.

A real pseudo-terminal reproduced the exact mutation as `TIMEOUT`, with `Password: ` in stderr. After redirecting worker input, it produced `INVALID` with `EOFError`. A complete terminal-mode prerequisite run then caught a second input path: subprocess workers could still open their controlling terminal directly. Those workers now start a separate session and receive `DEVNULL`. Fork workers keep their separate sessions and additionally redirect both file descriptor zero and Python's `sys.stdin` to `/dev/null`. Application probe behavior is unchanged.

Four mandatory infrastructure regressions now run during every complete-suite preflight. They create a real pseudo-terminal and acquire it as the parent worker's controlling terminal, so they reproduce the input channels available in your Ubuntu terminal. Both the forked and subprocess versions of the actual probe mutation must stop with EOF and retain their existing invalid classification. A separate input check must receive EOF, and a deliberately sleeping worker must still report a real timeout. All original fault recipes, timeout limits, assertions and the four-name exclusion list remain unchanged. This repair does not accept timeouts as passing results.

The complete suite was rerun with a terminal attached: **12/12 stages PASS in 53.36 seconds**, with **41.16 seconds** for the database work. Its Python audit reported **235 detected, zero survived, four known invalid, zero timed out and zero unapplied**. All sixteen exact coverage comparisons matched the earlier complete audit. Source identity, empty tables, fingerprint and disposable-copy cleanup passed. All 798 original baseline executions plus three subtests and every original fault remain. The four new input-isolation checks are additional infrastructure controls. Timing depends on machine load; 52.98 seconds was a measurement, not a fixed runtime.

Evidence: [terminal reproduction, original failure and repaired complete run](terminal-fault-isolation-results.json). The original failed report is preserved. Run the unchanged command in [the terminal reference](test-suite-commands.md). MER-1 4.3 remains pending its historical permission baseline.

📚 Learn first: Python's [getpass reference](https://docs.python.org/3.12/library/getpass.html) explains controlling-terminal input and its standard-input fallback; its [subprocess reference](https://docs.python.org/3.12/library/subprocess.html) documents `DEVNULL` and separate process sessions. Official references checked October 11, 2026.

↩ Return: rerun `.venv/bin/python tools/run_test_suite.py` from Ubuntu, then inspect the printed summary. Any unexpected timeout or surviving fault still requires investigation.
