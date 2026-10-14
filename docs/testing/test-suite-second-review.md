# Test-suite necessity and effectiveness: final second review

Latest execution configuration: [parallel SQL investigation and verification](test-suite-parallel-sql-performance.md), complete default PASS **36.83 seconds** with all cases/faults retained and 128 infrastructure controls. Earlier timing observations below remain historical.

Reviewed October 12, 2026. Correctness is the acceptance condition; the user explicitly made the runtime target optional. The restored eight-worker default passed all ten stages in **53.08 seconds**. The earlier six-worker verification took 55.65 seconds; the fastest prior eight-worker trial took 43.11 seconds. All 773 ordinary cases and three subtest rows passed, and every scheduled valid fault met its detection gate. There were no unexpected surviving, invalid, unapplied or timed-out faults. Source preservation and owned-copy cleanup passed. This is strong evidence for the specific implemented contracts, not a guarantee that every possible bug is covered.

Run the same default configuration in Ubuntu/WSL:

```bash
cd /home/vipra/Merlin
.venv/bin/python tools/run_test_suite.py
```

## Every individual case and fault

The review examined all **801 original case/subtest rows**, all original fault implementations and applications, repeated stages, migration controls and infrastructure guards. The first review removed weak or redundant executions and repaired misleading detections. The second review found additional redundancy and an assertion that could fail for the wrong reason. It also independently checked the final migration evidence gate. No application or migration source was changed during these reviews; defects found here were in tests, fault recipes and the runner.

Use these artifacts for the full breakdown. The CSV includes the original rows and two added cases, including the exact final reason for each consolidation. Its 803 rows reconcile to 776 retained case/subtest rows and 27 merged rows. A unittest parent is bookkeeping for its three subtests, not an additional independent credential input.

| Scope | Individual decisions, inputs and assertions | Current implementation and observed outcomes |
|---|---|---|
| All original/current case identities | [Complete case index](test-necessity-review/complete-case-index.csv) | [Identity reconciliation](test-necessity-review/inventory-completeness.json) |
| Application Python | [231 original application cases and 89 faults](test-necessity-review/python-application-review.md); [source-level details](test-necessity-review/python-application-review.json) | [Every current Python catalogue entry](test-necessity-review/current-python-fault-review.json) |
| Setup/documentation Python | [118 original case/subtest rows and 150 faults](test-necessity-review/setup-documentation-review.md); [source-level details](test-necessity-review/setup-documentation-review.json) | Same current Python catalogue above, including aliases and excluded diagnostics |
| SQL | [Every original case, fault implementation and pair](test-necessity-review/sql-review.md); [original source details](test-necessity-review/sql-review.json) | [382 current SQL scripts, reconnect, all 607 pairs and 126 implementations](test-necessity-review/current-sql-review.json); [second-review changes](test-necessity-review/second-pass-sql-review.json) |
| Quiz and real browser | [Every original case and fault](test-necessity-review/quiz-review.md); [original source details](test-necessity-review/quiz-review.json) | [All 37 current logic mutations, concrete behavior and detections](test-necessity-review/current-quiz-fault-review.json); [second-review rationale](test-necessity-review/second-pass-necessity-review.json) |
| Committed lifecycle/migration | Original SQL review above contains each of five lifecycle cases and 36 migration controls | [Migration equivalence conditions](test-necessity-review/migration-replay-equivalence-review.md); [final runtime evidence](test-necessity-review/second-pass-verified-suite-results/summary.json) |
| Runner, prerequisites, transport and safety | [Every control and repeated legacy fault](test-necessity-review/suite-controls-review.md); [individual JSON](test-necessity-review/suite-controls-review.json) | [Real positive/negative result-gate and scheduling controls](test-necessity-review/second-pass-verified-suite-results/focused-execution-controls.json) |

Historical reviews are source snapshots, not claims that their old recommendations remain unresolved. Current source supplements and the final CSV resolve their dispositions. Detailed compressed stage reports are preserved in `docs/testing/test-necessity-review/second-pass-verified-suite-results/`; they contain individual outcomes rather than only totals. The [summary](test-necessity-review/review-summary.json) records current counts, limitations and all ten stage results.

## Problems found and fixed

The [first review](test-suite-necessity-review.md) records the full initial findings: duplicate legacy/F077 executions, redundant probe/Markdown/NBSP/quiz cases, 50 unrelated SQL fault applications, 30 SQL detections occurring before the intended assertion, overly broad worker mutations, weak UUID/security/index assertions, and incomplete or contradictory reports accepted by result gates. Those fixes remain, and the final complete run verifies them again.

Additional second-review findings:

1. **Two legal-batch SQL cases were exact script duplicates.** `sql-valid-batch-cleanup_expired_blank_notes-1` merged into `expiry-batch-one`; `sql-valid-batch-purge_deleted_notes-1` merged into `purge-batch-one`. Each surviving script retains both source-local limit-removal and order-reversal faults. The 607 case/fault applications and 126 distinct implementations remain; no relevant mutation was dropped.
2. **One Python fault was semantically redundant.** `ast-doctor-208-1251` used a conjunction that always refused the observed cluster, equivalent to `doctor-cluster-always-refuses`. The alias applies only with the exact reviewed Doctor source hash, faulty AST hash and selected canonical fault. Changed source or partial selection executes the fault normally. There are now 232 canonical executions, three explicit aliases and four excluded reversed-import diagnostics in the unchanged 239-entry catalogue. Four real terminal isolation/timeout regressions remain independent.
3. **The NULL-email assertion observed the wrong users.** F049-F050 inserted two new users but counted seed users. Preparing the uniqueness mutation changed those seed emails, so the old assertion could fail even without broken uniqueness enforcement. It now counts the actual inserted users and checks both omitted emails remain NULL. The real baseline and specific mutation passed their respective gates.
4. **The migration result gate accepted contradictory branch evidence.** A forged rebuilt branch could change both its own schema/runtime digest and its claimed reference digest, while falsely declaring equivalence. The gate did not bind those digests to the branch that actually executed business cases; its target-command digest was unchecked. [Three pre-fix counterfactuals](test-necessity-review/migration-result-gate-reproduction.json) reproduced acceptance. The gate now binds both branches to the executed branch, the assigned migration container/socket command and the exact seven current source hashes. New positive and nine negative controls verify accepted complete evidence and rejected contradictory schema/runtime, wrong target, missing source, false validation, malformed digest, wrong replay count/mode and missing branch.

The last fix strengthens reporting, rather than hiding a failed migration. The actual producer already compared rebuilt state. An [independent read-only review](test-necessity-review/second-pass-independent-gate-review.json) found no findings in the repaired command reconstruction, cross-branch binding or counterfactuals; the complete fresh run also passed the real gate.

## Retained inventory and what it protects

| Area | Current count | Distinct contract protected |
|---|---:|---|
| Ordinary Python | 329 | Text limits and representations, whitespace parity, maintenance behavior, sanitized probe errors, diagnostic and documentation contracts |
| Python subtest rows | 3 | Explicit credential inputs within their unittest parent |
| SQL/reconnect | 383 | 382 concrete SQL scripts plus real transaction failure/reconnect; constraints, roles, state transitions, Unicode and worker boundaries |
| Quiz logic | 40 | Scoring thresholds, critical answers, input validity, saved-state validation and permutation behavior |
| Real browser | 16 | Rendering, progress, submission, retry, restart, reload, malformed storage and print invocation |
| Committed lifecycle | 5 | Fresh-connection cascade, two-client expiry/purge locks, rollback of whole cleanup transaction, purge batch behavior |
| Canonical Python faults | 232 | Specific source changes; three proven aliases and four startup diagnostics are recorded separately |
| SQL fault applications | 607 | 581 assertion detections and 26 controlled behavior-error detections; diagnostic categories remain distinct |
| Distinct SQL implementations | 126 | Includes separately patched premature-commit reconnect experiment |
| Quiz/browser/lifecycle faults | 37 / 16 / 5 | Each retained mutation has a concrete operation and observed failure |
| Migration controls | 36 | Two actual undo/reapply branches, 14 gates, three concurrency checks and 17 repair regressions |
| Named infrastructure controls | 128 | Inventory/result consistency, transport equivalence and independent expected outputs, statement parsing, isolation, cancellation, scheduling and cleanup |

Counts are different dimensions: a fault can have several case applications, and controls are not counted as ordinary application cases. Successful mutation detection demonstrates sensitivity to that named change; it does not establish that every assertion is indispensable. Conditional retained checks are documented explicitly rather than being called universally necessary.

Distinct Unicode inputs remain because code points, combining forms and emoji grammar can fail differently in future changes. Python and PostgreSQL enforce separate boundaries. Different users/roles, insert/update/restore paths, time thresholds, committed reconnects and real lock contention remain separate requirements. Identical current detection sets alone are not sufficient grounds for deleting those contracts.

## Database speed changes and their safety conditions

Fresh copy preparation now overlaps preflight and rollback-only source baselines. Actual fault injection, including isolation-control faults, still waits until both baselines pass. The runner joins setup and cleans owned resources on baseline failure, prerequisite failure and interrupts; dedicated subprocess controls exercise those paths. Every run uses a fresh backup, verified recovered copies, identity/data-directory/empty-row/schema/durability gates and unchanged resource limits. No test results or prior database snapshots are reused.

PostgreSQL supports base backups of a running cluster while other clients are active; required WAL provides consistency. That does not automatically make every concurrent test setup safe. The current source fixtures roll back, and recovered copies must pass independent startup checks. A future baseline that commits lasting fixtures requires revisiting the overlap. Backup-file verification alone is not restoration proof. Official references verified October 12, 2026: [pg_basebackup](https://www.postgresql.org/docs/18/app-pgbasebackup.html), [WAL and recovery](https://www.postgresql.org/docs/18/continuous-archiving.html).

Both historical PUBLIC CREATE branches still actually undo and reapply both migrations and check their separate permission restoration. Business-case replay runs once on the rebuilt false branch. The second rebuilt branch may reuse that same-run proof only when ordered semantic schema, runtime/session settings, database encoding/collation/extensions, pinned Unicode probe, empty data, exact target command and all seven source hashes match. Nested metadata array order is preserved. Missing or mismatched proof fails the suite; nothing is borrowed from an earlier run. See the dedicated migration equivalence review for details.

## Actual results and timing

| Complete run | Configuration | Total | Observation |
|---|---|---:|---|
| First review | Default six workers, earlier schedule | 46.47 s | PASS; historical 34.48-second database window starts after baselines |
| Second-review trial | Eight workers, overlapping setup, equivalent migration replay | 43.11 s | PASS before the final report-gate counterfactual additions |
| Earlier full verification | Six workers, all current controls | **55.65 s** | PASS; exact terminal command above |

The six-worker verification active lane times were SQL faults **30.76 s**, lifecycle **14.05 s**, migrations **21.02 s**, and Python faults **36.18 s**. These overlap, so do not add them to obtain total runtime. The new 55.39-second copy lifecycle window begins before preflight and includes overlapped baseline work and waiting; it is not directly comparable to the old 34.48-second post-baseline database window. All timing claims are measurements from their named runs, not guarantees or proof that changing worker count alone caused the difference. The default has been corrected to eight workers. The latest repeat took 53.08 seconds; see the [configuration correction and exact stage comparisons](test-necessity-review/fast-default-restoration-results.json). The 43.11-second result remains the measured performance baseline; it is not replaced by a slower run or represented as a guaranteed deadline. All new correctness gates remain.

Latest restored-default evidence: [complete PASS summary](test-necessity-review/fast-default-verified-suite-results/summary.json). Full compressed stage reports are preserved alongside it.

## Limits and handoff

Finite tests cannot guarantee every possible present or future defect. Authenticated API cross-user denial remains PENDING until the API ownership boundary exists; database role/ownership checks cannot substitute for it. Quiz answer-key correctness is not proved by deriving scoring fixtures from the authored key. Exact question counts, critical IDs and Fisher–Yates expectations protect current authored contracts, with maintenance coupling documented. Browser print coverage checks invocation, not printed layout. Blocked-storage mutations establish uncaught-error sensitivity and the baseline workflow, not every storage failure mode. Original historical PUBLIC CREATE remains unknown; the migration tests exercise both synthetic alternatives.

Authored work: test assertions, fault recipes, result validators, conservative scheduling optimizations, provenance/inventory records and this handoff. Observed results: all ten stages PASS, source preserved, cleanup PASS. Actual minutes: unknown. First current blocker: none for this review; API ownership coverage remains pending work for the future API. Exact next action: inspect the individual CSV/JSON decisions, then resume MER-8 Day 7 using its existing checklist. No new API implementation, Jira status change, deployment or publication occurred.

📚 Learn first: [terminal commands and prerequisites](test-suite-commands.md), [PostgreSQL transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html), [migration equivalence dimensions](test-necessity-review/migration-replay-equivalence-review.md).

↩ Return: [testing documents](../README.md) and [current project state](../planning/STATE.md).
