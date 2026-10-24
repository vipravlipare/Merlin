# MER-0–MER-11 full test and fault review

Reviewed October 24, 2026. This is a review of the current local working tree after adding validator-enforced per-fault check witnesses. It does not claim hosted CI, learner authorship, or complete security.

## Result

The complete guarded suite passed in four final-code runs under the 60-second gate: 55.43s and 56.183s with 16 workers, then 58.477s and 59.125s with 20 workers after the hosted-CI and copied-source fixes. The final fresh CI-entry rehearsal passed in 91.826s overall, including original-source Python tests, the complete suite, and a separate migration roundtrip. It used the current uncommitted working tree (`--include-untracked`); it is local evidence, not hosted CI. The evidence matrix links the final nested suite run `/tmp/merlin-day10-ci-entry-20261024-r8/suite/summary.json` and CI summary `/tmp/merlin-day10-ci-entry-20261024-r8/ci-summary.json`. All seven suite stages, CI steps, cleanup, and source preservation passed.

| Inventory | Reviewed result |
|---|---|
| Python cases | 821/821 collected IDs passed baseline; each ID has at least one fault detection. |
| Python fault catalogue | 321 entries: 314 executed and detected with a validator-enforced test/check witness, 3 identical-AST aliases, 4 invalid import-guard reversals excluded. No executable fault survived, timed out, failed to apply, or produced an invalid run. Aliases and exclusions are not counted as detections. |
| SQL cases and fault pairs | 383 cases and 607 exact case/fault pairs. Every baseline passed and every pair was detected. 581 detections reached an explicit SQL assertion; 26 reached the test behavior phase and failed on an unexpected result/error. Every mutation reached its `MUTATION_READY` marker first. |
| Lifecycle and migration | All 5 lifecycle cases, 14 undo gates, 17 repair checks, 3 concurrency controls, and migration preservation checks passed. The executed migration roundtrip replayed 382 SQL cases; the second branch used a validated equivalent-rebuild witness rather than claiming a second live replay. |
| Test process controls | Terminal isolation, timeouts, failure ordering, interrupt cleanup, disposable target identity, sandbox isolation, source preservation, and cleanup checks passed. |

The run tested 1,201 Python tests plus 3 subtests. It also ran both SQL shards (191 and 192 case results). Disposable database cleanup and protected-source preservation passed. The documentation check reported zero errors, one expected warning for unwritten future days, and 27 verification items. `git diff --check` passed. The final copied-source suite used 20 fault workers; its 314 executable Python faults took 37.477 seconds and full suite took 59.125 seconds. The runner and outer CI validator both reject a run over 60 seconds. Timings vary with machine load; the final pass had 0.875 seconds of headroom, so runtime margin remains narrow.

## Test-by-test source review

I reviewed every collected Python case ID against its test body and expected result, then matched it to the current fault-detection matrix. The 821 IDs expand from these 153 test functions/methods:

| Test source | Collected IDs | Main behavior checked |
|---|---:|---|
| `tests/test_local_provider.py` | 467 | Byte splits, coalescing, Unicode, strict JSON/schema, completion and EOF, terminal/error precedence, byte caps, source failures, no partial success, no disclosure, caller cleanup, and no external side effects. |
| `tests/test_note_rules_and_maintenance.py` | 202 | Weighted Unicode and text boundaries, normalization, draft/save behavior, invalid inputs, target identity, bounded cleanup calls, safe errors, and CLI behavior. |
| `tests/test_doctor_failure_cases.py` | 70 | Malformed inspection data, auth evidence, cluster identity, setup prerequisites, runtime boundaries, credential handling, and Redis responses. |
| `tests/test_prd_lint.py` | 35 | Links, Markdown fences, moved documents, schedule parsing, IDs, and precise failure locations. |
| `tests/test_health_api.py` | 17 | HTTP status/body/headers, routing, sensitive paths, generic errors, recovery, timeout, loopback binding, import safety, and cleanup. |
| `tests/test_database_connectivity_probe.py` | 13 | Read-only connection, sanitized failures at connection/query stages, and propagation of unrelated programming errors. |
| `tools/test_doctor.py` | 11 | Command timeout/capture, negative authentication proof, private-output handling, runtime checks, and alternate loopback ports. |
| `tests/test_notes_repository.py` | 6 | Title preview, active-view SQL, owner binding, read-only transaction, invalid/missing actor, busy connection, and two actors on one mocked connection. |

The 383 SQL cases use synthetic users/notes in the guarded isolated database path. They cover weighted constraints, database-side identity, permissions, RLS, ownership, content state changes, deadlines, retention, Unicode whitespace, and rollback. Each case transaction rolls back. Faults run on disposable database copies. Migration and lifecycle faults never run against protected storage.

## Fault review and attribution limits

All 314 executable Python faults changed behavior in isolated child processes. Each now has a static entry in [the Python fault witness manifest](../../tests/python-fault-witnesses.json): the intended case, exact source file and line, and check statement. The audit requires that case to fail and that its failure record contain the pinned source location and statement. Test-source hashes invalidate stale mappings. The suite validator independently checks exact witness inventory and evidence; it rejects wrong case/check/line, unrelated failures, setup-only errors, skipped tests, and incomplete selected runs. Health API and provider faults retain their additional contract-specific attribution checks. Three aliases and four harness-only exclusions remain outside the 314 executable witnesses.

The witness records identify the exact source check that failed for each isolated mutation. Some failures are assertion mismatches; others are unexpected exceptions at a positive-path or expected-exception check. The worker rejects collection and setup errors, and the validator requires the pinned case and source location. These records do not prove every check is necessary or nonredundant, nor that tests cover all possible defects.

I separately inspected the 19 Python faults whose recorded detecting tests failed through an exception rather than a conventional assertion. Each exercised a checked boundary: invalid input raised the wrong exception, valid input was rejected, a forbidden operation was reached, malformed data crashed instead of being safely rejected, a programming error was swallowed, or a bounded health request timed out. These are test failures in the call phase, not fixture or collection failures. The current matrix records all affected cases; the older [necessity and effectiveness review](test-suite-second-review.md) contains the source-level review of the previous inventory and its duplicate/weak-detection repairs.

The 26 SQL behavior-error detections are also not setup failures: each mutation was confirmed applied before the case ran. Their failures occur while executing the case's expected behavior, such as a legal boundary being rejected, a required denial returning the wrong SQLSTATE, or a state transition being blocked. The matrix keeps `DETECTED_ASSERTION` separate from `DETECTED_BEHAVIOR_ERROR` so those outcomes are not conflated.

Three Python catalogue entries are aliases of identical complete faulty ASTs, so only the canonical mutation ran. Four reversed `__main__`-guard mutations are excluded because they test harness startup rather than application behavior. Their exact IDs and reasons are in the matrix. None is presented as a successful application fault detection.

Every Python case has a nonempty detection list, but shared mutation kills do not prove that cases are nonredundant. The previous individual necessity review documents consolidation decisions for the earlier inventory. The new MER-11 malformed-actor and connection-reuse cases have separate assertions and separate fault witnesses. Repeated split offsets and Unicode classes remain separate because they exercise distinct input boundaries required by the decoder and text contracts.

## Remaining coverage limits

1. MER-11 repository tests use mocks. They do not call `app.notes_repository` against PostgreSQL or prove real connection-pool state reset. Database case F071 separately checks that the synthetic app role sees only its actor's rows; it does not exercise the Python repository.
2. There is no authentication route. The repository requires a UUID by contract but cannot establish who supplied it. Tests do not prove real signed-in identity.
3. The chosen MER-11 operation is list-only. No fetch-by-ID behavior exists, so guessed foreign-ID versus missing-ID response behavior is not implemented or tested.
4. MER-10 HTTP transport remains deferred. Decoder tests do not establish redirects, proxy behavior, deadlines, request cleanup, or transport isolation.
5. Current evidence is a local fresh CI-entry rehearsal over uncommitted code and documents. Hosted CI has not tested this exact combined revision.

No current failing test or surviving executable fault was found. The earlier per-fault attribution gap is closed for the current local snapshot. The fresh local CI-entry rehearsal now validates current MER-11 witnesses and retains all eight case/fault/migration evidence reports with SHA-256 checksums. Hosted CI has not tested this exact revision. Passing tests or fault injection do not prove all possible vulnerabilities are covered.
