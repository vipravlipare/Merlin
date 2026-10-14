# Restoring and improving the complete test-suite runtime

Verified October 13, 2026. The final normal one-command default passed all ten stages in **36.83 seconds**, including the direct parent-gate controls. A previous normal-default verification passed in **35.77 seconds**. A preceding two-copy SQL trial passed in **41.63 seconds**. Both retained every application case, fault injection and existing correctness gate. The final default also included all new partition/merge controls. Source preservation and owned-copy cleanup passed.

```bash
cd /home/vipra/Merlin
.venv/bin/python tools/run_test_suite.py
```

## What changed between 43 and 51 seconds

The earlier 43.11-second trial used eight Python workers. Leaving six workers as the subsequent default was a real configuration mistake; eight were restored. However, the eight-worker repeats still took 51.61 and 53.08 seconds, so worker count did not explain the entire difference.

The exact Python execution scopes, cases and detections matched. SQL case IDs, mutation source and outcomes matched, as did the browser source and database runtime image. The slowdown affected several independent concurrent lanes, while the baseline stayed nearly unchanged. Relative to the 43.11-second run, the 51.61-second run increased Python faults from 23.34 to 32.07 seconds, SQL from 24.23 to 30.61, lifecycle from 11.42 to 14.66 and migrations from 18.14 to 23.18. Isolation controls also delayed the SQL start by another 0.85 seconds. New result-gate checks do not directly explain these independent child-stage increases. Host conditions or contention are plausible, but historical measurements do not prove a specific environmental cause.

A candidate removing duplicate pytest terminal failure rendering preserved every outcome and diagnostic but did not improve complete runtime. It was reverted. No application function, migration, constraint or security check was changed to make the suite faster.

## Retained optimization

The serial SQL audit now splits its 382 ordinary scripts into two deterministic partitions. Each partition runs serially on a separate, independently recovered PostgreSQL copy. The real reconnect baseline and premature-commit fault execute only in partition zero. Together the partitions still execute exactly 383 SQL/reconnect cases and all 607 fault applications, covering the same 126 distinct implementations.

The suite now owns four temporary containers: first SQL partition, second SQL partition, lifecycle and migrations. Every container retains its one-CPU/1-GiB cap, private disk volume and Unix socket, disabled external networking and PostgreSQL durability settings. This increases the number of independently capped copies from three to four; it does not raise any individual container's limit. Fresh backup, runtime verification, source protection and failure/interrupt cleanup remain mandatory. `MERLIN_SQL_SHARDS=1` retains the single-SQL-copy diagnostic fallback. Serial database mode also retains its original full audit.

Each child must exit successfully and preserve its own schema fingerprint. The merger requires the exact expected case IDs for each partition, no duplicates or overlap, identical current source hash, correct reconnect ownership and distinct target containers. It writes the combined report only after both children finish. The parent reconstructs that report from the two actual child reports and assigned manifests, then runs the existing exact full-case/fault-pair and underlying-outcome validators. A missing recipe, false preservation claim, altered report or failed baseline cannot become a combined PASS.

Fifteen new helper/selector controls exercise the real merger and command selector: one complete positive, nine deliberately incorrect partition reports and five invalid/ambiguous selectors refused before opening database transport. The second copy also has an actual route check, and the live faulty-function containment check now verifies it alongside the other copies and source. Six additional controls exercise the real parent gate itself: complete positive evidence and rejection of contradictory merged proof, changed child outcome, missing child, wrong source and crossed target. Named infrastructure controls increase from 106 to 128; ordinary application-case and fault counts remain unchanged.

The coordinator and both SQL children share the stage process group, so interruption reaches all three. The outer owner joins execution before removing its resources. A failed partition waits for its sibling to finish before the coordinator reports failure; this is a failure-reporting delay, not a false PASS. An [independent read-only safety review](test-necessity-review/parallel-sql-independent-review.json) found no blocking finding.

## Actual results

| Configuration | Complete suite | Python faults | SQL audit | Migrations |
|---|---:|---:|---:|---:|
| Earlier fast trial, one SQL copy | 43.11 s | 23.34 s | 24.23 s | 18.14 s |
| Recent eight-worker repeat, one SQL copy | 53.08 s | See raw summary | See raw summary | See raw summary |
| First two-partition trial | 41.63 s | 23.37 s | 17.89 s | 17.89 s |
| Earlier normal default | 35.77 s | 21.68 s | 15.43 s | 16.06 s |
| Final normal default, all new controls | **36.83 s** | **23.51 s** | **18.14 s** | **18.14 s** |

The SQL partitions overlap, as do other independent lanes. Do not sum lane times to derive total runtime. The last two runs are measurements on a shared environment, not guarantees or controlled attribution of every second. The old 43–44-second baseline is surpassed by both passing partition trials; it was not redefined to accept the slower run.

Exact comparisons confirmed unchanged Python case outcomes, scopes and fault detections; unchanged SQL cases, mutation implementations and statuses; and unchanged quiz/browser/lifecycle outcomes. All 773 ordinary cases plus three subtest rows remain. Python retains 232 canonical executions, three proven aliases and four explicitly excluded startup diagnostics. Quiz/browser/lifecycle fault counts remain 37/16/5. Both actual migration undo/reapply branches, 14 gates, three concurrency checks and 17 repair checks remain. The same-run migration replay-equivalence gate remains enforced.

Evidence: [exact comparisons, trials and source hashes](test-necessity-review/parallel-sql-performance-results.json), [final complete summary](test-necessity-review/parallel-sql-verified-suite-results/summary.json), [positive and negative infrastructure controls](test-necessity-review/parallel-sql-verified-suite-results/focused-execution-controls.json). Complete compressed stage and partition reports are preserved beside the summary. Raw final run: `/tmp/merlin-test-suite-iv5g50ng/`.

## Routing finding and handoff

The Codex configuration inspected during this work uses the default OpenAI provider, with no verified OmniRoute endpoint/profile. Therefore active routing and automatic fallback were not established for this session. An OmniRoute health response appeared stale; it was not treated as fresh server-health proof. No model connection or credentials were changed.

Authored work: partition selector, coordinator/merge proof, additional guarded copy and controls, result validation and this evidence. Application/migration sources unchanged. Observed results: complete PASS in 36.83 seconds, source preservation PASS, cleanup PASS. Actual minutes: unknown. First current blocker: none for the performance verification. Next action: run the unchanged command above in Ubuntu/WSL and inspect its summary; then resume Day 7. Authenticated API ownership coverage remains pending until that boundary exists. Finite tests cannot guarantee every possible defect.

📚 Learn first: [full commands and prerequisites](test-suite-commands.md), [every case and fault decision](test-suite-second-review.md), [PostgreSQL transactions](https://www.postgresql.org/docs/18/tutorial-transactions.html).

↩ Return: [project state](../planning/STATE.md).
