# Complete test-suite necessity review

Historical first-review snapshot. The [final second review](test-suite-second-review.md) supersedes its current counts, timings and source supplements; original observations remain below.

Reviewed October 12, 2026. The first complete guarded command passed all ten stages in **46.47 seconds**, with **34.48 seconds** for the database lanes, setup, guards and cleanup. The under-52-second target was met in this environment; it is not a guaranteed deadline on every machine or under every load. All current baseline cases and scheduled valid fault experiments passed their acceptance gates. No application code or migration source was changed in this review.

This was not a decision to keep every AI-written test. I reviewed every one of the original **801 baseline case/subtest rows**, all **239 Python catalogue faults**, **55 repeated legacy executions**, **71 SQL implementations and 653 SQL case/fault pairs**, **35 JavaScript faults**, **16 browser faults**, **five lifecycle faults**, **36 migration controls**, and every default runner stage and named prerequisite/safety control. [Inventory reconciliation](test-necessity-review/inventory-completeness.json) checks identities, not merely matching totals.

## Read the full individual breakdown

| Area | Human-readable review | Full inputs, assertions, changed source and observations |
|---|---|---|
| Application Python | [Every case and fault](test-necessity-review/python-application-review.md) | [Original detailed JSON](test-necessity-review/python-application-review.json); [current Python catalogue](test-necessity-review/current-python-fault-review.json) |
| Setup and documentation Python | [Every case and fault](test-necessity-review/setup-documentation-review.md) | [Detailed JSON](test-necessity-review/setup-documentation-review.json) |
| PostgreSQL, lifecycle and migrations | [Every original case, fault and pair](test-necessity-review/sql-review.md) | [Original detailed JSON](test-necessity-review/sql-review.json); [current repaired SQL and all pairs](test-necessity-review/current-sql-review.json) |
| Quiz logic and browser | [Every case and fault](test-necessity-review/quiz-review.md) | [Detailed JSON](test-necessity-review/quiz-review.json); [logic repair mapping](test-necessity-review/quiz-focused-verification.json); [current quiz catalogue](test-necessity-review/current-quiz-fault-review.json) |
| Runner, prerequisites and safety | [Every control and repeated legacy fault](test-necessity-review/suite-controls-review.md) | [Detailed JSON](test-necessity-review/suite-controls-review.json) |
| Original-to-current case disposition | [Complete CSV index](test-necessity-review/complete-case-index.csv) | [Summary](test-necessity-review/review-summary.json) |

The original source reviews remain historical snapshots. The CSV's final_disposition and final_reason columns resolve removals, repairs and retained input partitions. Current SQL and verified runtime evidence supersede old source fingerprints; do not interpret a historical IMPROVE recommendation as still unverified after its recorded repair.

An independent agent also reviewed the integrated runner, inventory, transport, sandbox cleanup and browser concurrency. [Its scoped read-only review](test-necessity-review/independent-integration-review.json) found no critical correctness findings. It did not run tests; the complete runtime evidence is separate.

## What was unnecessary and removed or consolidated

1. The legacy stage repeated **55 identical Python faults** already present in the stronger canonical case audit. Their implementations and relevant baselines remain; only the second mandatory execution was removed. The standalone diagnostic command remains available.
2. Two Python fault names produced identical complete-module faulty ASTs. They now alias the canonical fault, with explicit provenance. Four reversed import guards are excluded startup diagnostics, not claimed application detections. Real terminal regressions still execute.
3. The standalone F077 timestamp stage repeated the same complete-audit case and recipes. Its independent assertions remain in the SQL audit; `--only F077` remains available for debugging.
4. **50 SQL pairings** applied faults to unrelated cases and survived as expected. Those applications were removed; all relevant fault implementations and baseline requirements remain.
5. Probe failures used a 24-row class-by-stage Cartesian product despite one shared outer exception handler. Nine representatives preserve every stage and all four exception classes. A weaker duplicate ProgrammingError/query test is covered by that stronger representative. Operational query cleanup assertions remain independently checked.
6. Two weaker Markdown example-ignore functions were consolidated into stronger closed-fence tests. Triple-tilde input remains explicitly tested, along with the real broken link after the fence.
7. Five older NBSP SQL checks were consolidated into their parity successors. Same literal values, operations, roles and error diagnostics remain. The successor countdown and draft-deletion checks additionally preserve body data or the other owner's row.
8. Two JavaScript cases repeated empty-array validation or serialized JSON repeatedly without invoking application persistence. Empty-array rejection and actual browser reload tests remain.

The retained suite has **775 ordinary cases plus three subtest rows**. Removing a repeated execution is different from deleting its requirement. Each removal above has a named surviving assertion or representative partition.

## Weak evidence and harness bugs repaired

- Six result validators accepted fabricated truncated reports. [The reproduction](test-necessity-review/result-validator-reproduction.json) preserves the original failure. Three additional gates accepted [contradictory baseline or preservation evidence](test-necessity-review/contradictory-baseline-reproduction.json). Validators now compare exact reviewed case/fault/pair inventories, reject duplicates and omitted source/scope evidence, and cross-check declared detections, baselines and preservation against actual outcomes. Independent positive and negative regression controls run in preflight. The inventory is reviewed explicitly; it is not regenerated automatically to make a run pass.
- **30 original SQL pair detections occurred before the target assertion**, including 29 whitespace-maintenance fixtures and missing-email seeding. Maintenance faults now alter the tested worker selection predicate for the named code point; nullable-email uniqueness is tested after valid preparation with explicit missing-email inserts. Fixture-only failure no longer substitutes for the intended behavior proof.
- Title-counting faults no longer fail an unrelated body constraint. User-ID immutability targets an unreferenced user, isolating the trigger from the owner FK. First cleanup effects and the exact restored 24-hour deadline are asserted. Both user and note UUID defaults must generate two distinct valid values; new constant-valid-UUID faults catch accidental reuse that a single insert would miss.
- Legal batch sizes act on eligible rows with exact returned counts and row effects. Worker and invalid-batch constant-return stubs were replaced with source-local selection, ordering, limit or validation mutations. Restore behavior has its own source-local fault. Purge permission denial is independently covered.
- The reconnect mutation now prematurely commits only its synthetic first write. The second write still fails its real FK; the actual reconnect assertion detects the retained row. Gated cleanup removes exactly that synthetic user. No schema fault is committed.
- The committed lifecycle cascade fault now changes the deletion predicate to a guaranteed nonexistent user, commits that no-op, and reaches the same new-connection assertion as the baseline. It no longer substitutes a transaction-local pre-reconnect assertion for the committed workflow's oracle. Original FK-removal sensitivity remains in direct SQL cases.
- Index checks inspect catalog keys, direction/null ordering, predicate, readiness, validity and B-tree method instead of relying on text formatting. Quiz scoring fixtures derive correct indexes from the authored bank. Composite scoring/permutation mutations are narrowed.
- The combined role-security assertion now has independent faults for LOGIN, SUPERUSER, CREATEDB, CREATEROLE, REPLICATION and BYPASSRLS, with LOGIN checked for every permission group. RLS enablement and forced-owner enforcement are independently faulted on both users and notes. A single LOGIN fault was insufficient evidence for all those conjuncts.
- Native fresh-connection proof requires successful positive numeric backend IDs. Independent expected outputs prevent two equally broken transports from passing equivalence. SQL statement-boundary and malformed-string/comment controls cover the optimized transport. Browser artifacts now contain source hashes, and isolated browser contexts execute two workflows concurrently.

The earlier effectiveness report's claim that every SQL case independently demonstrated its intended fault oracle was too strong. Its raw results are preserved, but setup failures and unrelated-constraint failures are not valid substitutes for the assertion being audited. This necessity review corrects that claim.

## Why retained checks are useful

A retained check protects a named current requirement: a threshold, data representation, normalization rule, state transition, permission boundary, transaction boundary, UI behavior or harness safety condition. Exact concrete inputs and assertions are in the linked JSON, not inferred from a test name alone. The CSV records the individual reasoning and final disposition.

Unicode code points are not interchangeable just because one constant mutant breaks them all. Python and PostgreSQL are separate enforcement layers. Mocked calls cannot replace real committed/reconnected rows or two-client locks. Application and worker roles differ. Insert, update, restore, expiry and purge change different state. Below/at/above thresholds, bool-versus-int, JSON object-versus-array/null, negative-versus-zero interval consequences, and draft field paths are defensible input partitions. Eight remaining conditional Python reduction suggestions were retained for those explicit contracts; there is no automatic deletion based on a common kill set. The unittest parent exists to run its three subtests and is not counted as a fourth independent credential input.

This is a justified regression suite, not a mathematical proof that no smaller suite could work. Unique fault ASTs are not automatically necessary merely because they differ; their changed guards, functions and detected requirements are recorded. Finite tests cannot certify every possible future bug.

## Verified current inventory

| Category | Count |
|---|---:|
| Python ordinary cases | 329 |
| Python subtests | 3 |
| Direct PostgreSQL/reconnect cases | 385 |
| Quiz logic cases | 40 |
| Real browser cases | 16 |
| Committed lifecycle cases | 5 |
| Canonical Python faults | 233 |
| SQL case/fault applications | 607 |
| Distinct SQL implementations including reconnect | 126 |
| Quiz faults | 37 |
| Browser faults | 16 |
| Lifecycle faults | 5 |
| Migration controls | 36 |
| Infrastructure controls | 93 |

SQL outcomes: {'DETECTED_ASSERTION': 581, 'DETECTED_BEHAVIOR_ERROR': 26}. Python: 233 valid canonical detections, two aliases and four excluded diagnostics; no valid survivor, invalid experiment or timeout. JavaScript: 37 detected faults. All 16 browser and five lifecycle paired faults were detected. Both migration permission branches, all gates, concurrency checks and repairs passed. Source identity, schema/permissions fingerprint, empty tables and copy cleanup were preserved.

Durable evidence: [final summary](test-necessity-review/verified-suite-results/summary.json), compressed per-case reports in the same folder, [review summary](test-necessity-review/review-summary.json), and [command reference](test-suite-commands.md). Runtime before this review was 53.88 seconds in the referenced prior run; the unchanged baseline measured 61.68 seconds during this session. Intermediate repaired configurations passed in 49.22 and 43.22 seconds. These are complete runs, including guards and cleanup, not sums of overlapping stage times.

## Limits and exact next action

Print testing proves invocation, not paper layout. Browser cache/storage fault results establish error containment, not all storage-failure modes. Routine migration verification uses disposable synthetic historical permission branches; it does not recover the unknown original PUBLIC CREATE baseline. Authenticated API cross-user denial remains pending until that API boundary exists. No claim of complete application security or all possible future failures is made.

Current action: run `.venv/bin/python tools/run_test_suite.py` from the repository root. Resume Day7 MER-8 only after reading this review and the Day6 handoff. New application features must add requirement-linked acceptance and fault coverage; do not preserve today's case count as a quota. Actual review labor minutes are unknown. No current failing stage remains; no Jira status, application feature, dependency or migration source was changed.
