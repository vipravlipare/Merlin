# Individual test effectiveness audit — October 11, 2026

**Historical report; qualified and superseded by the [complete necessity review](test-suite-necessity-review.md).** The October 12 review found 30 SQL pair failures before the intended assertion, secondary-constraint attribution and redundant executions. The original blanket statement below that every case independently demonstrated its intended oracle was too strong. Raw historical outcomes remain unchanged; current repairs, reductions and verified results are in the newer review.

Every current executable case was run against the working implementation and at least one deliberately faulty implementation. **798 cases pass, plus three passing Python subtests. Every case and every subtest demonstrably detects an injected fault.** This is evidence about the implemented helpers, schema, quiz and setup tooling. It is not a guarantee that every possible application failure has been considered.

This report supersedes the totals and remaining-browser/concurrency statements in [the earlier repair report](test-hardening-and-repairs.md). The earlier probe, whitespace, maintenance-identity and array-cache repairs remain verified. The user explicitly authorized stronger tests and repairs to responsible code. No assertion was weakened, no failure was skipped to obtain a pass, and no production schema fault was installed.

## Results and individual evidence

| Suite | Passing cases | Individual fault detection | Evidence |
|---|---:|---|---|
| Python helpers, probe, maintenance and tooling | 346, plus 3 subtests | All 349 observations detect faults; 235 source-fault experiments detected | [Every Python case](case-effectiveness-evidence/python-cases.md) |
| Installed PostgreSQL rules | 389 | Every case detects a fault; all 71 distinct SQL faults detected across the suite | [Every SQL case](case-effectiveness-evidence/database-cases.md) |
| Actual quiz calculation and saved-state functions | 42 | Every case detects a fault; all 35 injected faults detected | [Every quiz logic case](case-effectiveness-evidence/quiz-logic-cases.md) |
| Real Chromium workflows | 16 | Every workflow detects its deliberately broken behavior | [Every browser case](case-effectiveness-evidence/quiz-browser-cases.md) |
| Committed database reconnect and concurrent locks | 5 | Every case detects its deliberately broken behavior | [Every lifecycle case](case-effectiveness-evidence/database-lifecycle-cases.md) |
| Total | **798, plus 3 subtests** | **No case without demonstrated fault detection** | [Machine-readable summary](case-effectiveness-evidence/audit-summary.json) |

The [fault catalogue](case-effectiveness-evidence/fault-catalogue.md) maps each case's fault IDs to the exact experiment. Full outputs, assertions, source fingerprints and individual fault outcomes are retained in compressed JSON: [Python](case-effectiveness-evidence/python-test-results.json.gz), [SQL](case-effectiveness-evidence/database-test-results.json.gz), [timestamp rerun](case-effectiveness-evidence/timestamp-case-results.json.gz), [quiz](case-effectiveness-evidence/quiz-logic-results.json.gz), [browser](case-effectiveness-evidence/quiz-browser-results.json.gz), [lifecycle](case-effectiveness-evidence/database-lifecycle-results.json.gz). A passing parent unittest and its three subtests are listed separately for traceability; the subtests are not silently added to the 798 case count.

Four Python source experiments were invalid because reversing an import-time `__name__` guard caused the harness to execute a CLI during import. Those four are explicitly excluded from detections. There were no surviving valid Python experiments, timeouts or unapplied recipes. One quiz fault deliberately breaks script syntax; the complete-script parsing case detects that fault, while the other 34 quiz faults change behavior.

The SQL audit ran **653 case/fault pairs**: 550 assertion failures, 53 rejected valid operations caused by faulty behavior, and 50 surviving pairs. Each of the 71 distinct faults was detected by a relevant case. A fault need not break an unrelated case: for example, changing a cleanup return count should not change the permission test that rejects a call before cleanup runs. The full pair outcomes remain visible; surviving pairs are never described as detections.

📚 Learn first: [Node.js test runner](https://nodejs.org/api/test.html), read assertions and individual tests; [PostgreSQL locking clauses](https://www.postgresql.org/docs/17/sql-select.html), read `FOR UPDATE` and `SKIP LOCKED`; [Playwright BrowserContext](https://playwright.dev/docs/api/class-browsercontext), read isolated contexts. Official pages opened October 11, 2026.
↩ Return: choose a row from each evidence table, identify its intended behavior and its fault ID, and explain why that exact assertion fails under the injected fault. Done when you can distinguish a normal pass, a detected behavioral fault, an invalid harness run and an unrelated surviving pair. Time box: 15 minutes inside the existing learner budget; no extra funded feature work is implied.

## Real defects found and repaired in this audit

| Defect | Reproduced failure | Code repair and regression proof |
|---|---|---|
| Incomplete quiz cache marked submitted | A cache containing two selected questions but only one answer was accepted with `submitted=true`. Restored UI refused later submissions because it already considered the attempt submitted. | `validSaved` now requires an own answer entry for every selected question when the saved attempt is submitted. The new pure test failed before repair. A real-browser case now completes successfully and catches removal of this guard. Valid partial unsubmitted attempts still restore. |
| Nested Docker inspection data had unsafe shapes | Eight inputs, including NULL/array port maps, non-object bindings and malformed logging configuration, were accepted by `inspect` and could reach unsafe `.get()` calls. | `tools/doctor.py` validates the nested structures before returning inspection data. All eight new negative cases failed before repair and pass after it; the valid-inspection cases remain passing. |
| Malformed project metadata crashed the checker | Valid TOML containing `project=[]` raised `TypeError` instead of reporting failed Python configuration. | The existing configuration-parsing handler now also handles the expected `TypeError`. The new malformed-manifest case failed before repair and now produces a controlled failure report. Missing or incorrectly typed Python pins remain rejected. |
| Unicode digit port crashed conversion | `HostPort='²'` passed `str.isdigit()` but failed `int()`, causing a traceback during runtime checks. | The port must match one to five ASCII digits and be within 1–65535. The same validated result controls both reporting and later host checks. The new negative case failed before repair; removing the ASCII guard is detected. |

These are four responsible-code defects, not four hundred independent defects. Their targeted pre-repair reproductions contained 11 failing cases: eight nested inspection inputs and one case for each other defect. The assistant authored these repairs under the user's explicit authorization; they do not establish learner mastery.

Python's digit classification deliberately includes some characters that cannot be parsed as ordinary decimal integers. That API behavior supports treating port syntax as an explicit ASCII input contract. [Python string classification](https://docs.python.org/3.12/library/stdtypes.html#str.isdigit) was opened October 11, 2026.

## Weak tests strengthened and missing coverage added

- **F077 timestamp equality:** the old assertion inspected rows already created by shared setup. An insert-time fault applied after setup therefore escaped that case. The case now performs fresh user and note inserts itself and checks their initial timestamps. This changes what is exercised, not the timestamp requirement.
- **Quiz unknown IDs:** the old negative input also lacked a valid option order, so rejection could come from the unrelated permutation guard. The case now supplies a valid order for the unknown ID, forcing the ID check to matter.
- **Quiz permutation length:** a three-element order also failed the independent uniqueness count. A five-element order with exactly four distinct valid choices now isolates the required length boundary.
- **Private timeout output:** the setup-checker test now requires completely empty output after a captured timeout. Merely checking for the word `secret` missed a fault that printed other command arguments.
- **Setup boundaries:** added separate checks for interpreter/runtime pins, missing or stale locks, environment permissions and tracking, tool availability, private credential capture, positive authentication evidence, Redis responses/configuration, loopback ports, resource budgets, log limits, service UID and named-volume ownership.
- **Documentation tooling:** added separate checks for root entrypoint links, non-legacy subfolders, exact skill/day warnings, peer-section Learn/Return boundaries and valid versus invalid fence closure. Code examples must remain examples; real links after a closed fence must be audited.
- **Real browser behavior:** rendering, radio changes, progress, reload/order preservation, incomplete submissions, completed restoration, duplicate submission, retry selection and denominator, restart, storage failures, critical warnings and printing are now executed in Chromium.
- **Database lifecycle:** new committed synthetic rows prove visibility after a fresh connection, account-delete cascade after reconnect, expiry/purge lock skipping, batch limits and rollback of the first cleanup when the second operation fails.

Added **100 cases** since the earlier 698-case repaired baseline: 77 Python, two quiz logic, 16 browser and five lifecycle cases. The SQL case count stayed 389; F077 was strengthened. Cases remain separate so one failure cannot conceal later boundaries.

Two audit setup errors were also exposed and corrected. F077's first new fixture used a username longer than the existing limit; the bounded replacement fixture was rerun and its genuine result replaces that row in the human-readable table. The original failed run and the explicit rerun are both retained in the archives. The first lock test did not guarantee that the locked row sorted first, so removal of `SKIP LOCKED` could survive by selecting the other row. Historical fixture timestamps now force the locked row first, and assertions identify the exact unchanged and changed rows. Both corrected lock cases detect the fault.

The earlier suspicion that the existing cleanup grant test might falsely pass was not reproduced: granting the forbidden execution privilege made its existing assertion fail. That was an investigative hypothesis, not a discovered application defect.

## Isolation and preservation

Python faults execute in fresh child processes or temporary linter scripts. Quiz faults use temporary copies or in-memory HTML; the product HTML is not overwritten. Real-browser contexts isolate storage, and intercepted requests serve only the local quiz content. Browser tooling was pinned to Playwright 1.58.2 and Chromium 145.0.7632.6 in `/tmp`. This Ubuntu 26.04 environment required the Ubuntu 24.04 browser build override and three temporary extracted runtime packages; system package installation did not succeed and no system packages were changed. These temporary browser dependencies are not part of the project's lockfile and must be provisioned again on a clean machine.

The only allowed database target was `merlin_d6`, cluster `7694311451826794534`, Compose project `merlin-d6-20261008105707`. Standard cases and schema faults roll back. The five lifecycle cases briefly commit synthetic UUID fixtures so separate sessions can see them. Teardown deletes only each case's synthetic owner, with its notes cascading, and verifies both tables are empty. Function, constraint, policy, owner/ACL, RLS, index, role-power/membership, column/default, schema, trigger and view fingerprints matched before and after. The final full PostgreSQL pytest run passed all 389 cases and its identity/empty-table teardown.

The preserved Sprint 0 cluster `7691749973399031842` and `merlin_postgres_data` were excluded. No migrations were applied in this audit. Applied migrations 001 and 002 must not be rerun. No commit, push, Jira edit, upload or scheduler start was performed.

## Reproduce the evidence

Run the database suites and lifecycle audit serially. The empty-database suite must never run concurrently with committed lifecycle fixtures. Docker permission is required. The browser command below assumes the temporary audited Playwright installation and runtime libraries still exist.

```bash
.venv/bin/python -m pytest -q --tb=short
MERLIN_RUN_DB_TESTS=1 .venv/bin/python -m pytest -q tests/test_users_notes_database.py --tb=short
node --test --test-isolation=none tests/quiz.test.js
.venv/bin/python tools/audit_python_cases.py --out /tmp/merlin-python-effectiveness-final.json
.venv/bin/python tools/audit_database_cases.py --out /tmp/merlin-sql-effectiveness-final.json
.venv/bin/python tools/audit_database_cases.py --only F077 --out /tmp/merlin-sql-F077-final.json
.venv/bin/python tools/audit_quiz_cases.py --out /tmp/merlin-quiz-effectiveness.json
.venv/bin/python tools/audit_database_lifecycle.py --out /tmp/merlin-lifecycle-effectiveness.json
```

```bash
LD_LIBRARY_PATH=/tmp/merlin-browser-audit/runtime/usr/lib/x86_64-linux-gnu \
PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64 \
PLAYWRIGHT_BROWSERS_PATH=/tmp/merlin-browser-audit/browsers \
MERLIN_PLAYWRIGHT_MODULE=/tmp/merlin-browser-audit/node_modules/playwright/index.mjs \
node tools/audit_quiz_browser.mjs /tmp/merlin-browser-effectiveness.json
.venv/bin/python tools/write_test_audit.py
git diff --check
```

The final standard Python run passed 346 cases and three subtests; its 389 database skips are opt-in controls, not counted as passes. The separate database run passed 389 in 126.25 seconds. The JavaScript run passed 42. Browser and lifecycle audit baselines passed 16 and five respectively.

## Remaining limits

The authenticated backend, API login/session handling, browser note editor and sync routes do not exist yet; their full end-to-end security cannot be tested as implemented behavior. `SET ROLE` proves database role behavior, not authenticated API identity. The current foreground maintenance CLI still names the disposable `merlin_d6` login; limited-role SQL tests do not establish a dedicated least-privilege worker login. Its fixed cluster gate is not a replacement for production worker credentials and privileges. Simultaneous note-edit-versus-cleanup races, multi-worker stress, long-running scheduling, process/host crashes, connection loss during commit, large data performance, backup restoration and every migration environment remain outside this evidence. Committed synthetic rows prove reconnect persistence, not survival of a PostgreSQL/host restart. The print check proves event dispatch to `window.print`, not the quality of a generated PDF.

Migration 001's down migration is still missing; migration 002's previously verified rollback does not fill that gap. Windows Desktop skill activation remains a separate pending check. OmniRoute routing and token savings remain unverified because its server was not running. Passing tests do not certify unfinished features or learner mastery. Actual learner minutes remain unknown; this audit adds no funded roadmap hours.

📚 Learn first: [PostgreSQL explicit locking](https://www.postgresql.org/docs/17/explicit-locking.html), read row locks and their transaction lifetime; [PostgreSQL transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), read commit and rollback. Pages opened October 11, 2026.
↩ Return: explain why a rollback-only fixture cannot prove cross-session visibility, why the locked row must sort first in the fault test, and which failures still require a future implemented backend. Done when you can describe what each test proves without claiming exhaustive coverage. Time box: 10 minutes within the existing learner budget.
