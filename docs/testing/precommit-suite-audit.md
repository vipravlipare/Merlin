# Pre-commit cumulative suite audit

Later scope change: [application-only verification](application-test-scope.md) removes personal quiz tests/faults under explicit learner instruction. Quiz-inclusive counts and source receipts below are historical; use the new receipt for the retained application gates.

Recorded October 23, 2026. The learner authorized a thorough pre-commit review, new missing tests/faults and measured runtime improvements. This is assistant-authored work. Actual effort minutes are unknown. No commit, push, workflow dispatch, live model request or transport integration is authorized or performed.

📚 Learn first: [retained suite commands](test-suite-commands.md), [earlier individual necessity reviews](test-suite-second-review.md), [decoder D-01–D-38 map](provider-decoder-baseline-review.md#complete-decoder-requirement-map) and [health API contract](../architecture/health-api-contract.md).
↩ Return: inspect the new findings and final evidence below before separately deciding publication; keep exact hosted verification pending.

## Scope and findings

The review covers implemented Sprint 0 and Days 6–9, including the work represented by MER-1, MER-8, MER-9 and MER-10. “MER0–MER10” is interpreted as the cumulative implemented foundation, not a claim that eleven numbered Jira stories or future planned features exist. Planning/account/learning checks remain separately attributed. Day 9 remains parser-only: HTTP transport, deadlines, redirects/proxies/fallback and actual network cancellation are deferred.

The original full baseline passed, but that did not establish that its effectiveness reporting was sound. This audit found and repaired the following gaps:

1. An incomplete literal suffix could hide an earlier JSON syntax error. The decoder now considers a partial literal only when the JSON parser was expecting a value. Two new cases distinguish extra data and a missing comma from genuine truncation. A further numeric-suffix review found the same risk for unfinished decimals/exponents. Six additional cases cover earlier missing commas, a number where a delimiter was required, leading zeroes and an invalid decimal/exponent combination. The numeric classifier now requires the parser to stop at the actual unfinished numeric suffix.
2. The duplicate-model fixture also changed the model identity. It now repeats the valid identity in an otherwise valid terminal record, so last-key-wins parsing cannot be rejected for an unrelated reason.
3. Twenty-five provider cases depended only on a broad fail-open mutant. Thirteen narrower faults now exercise missing/wrong fields, invalid chunks, generic error objects, empty source, malformed/top-level data, private diagnostics and the literal/numeric-prefix regressions. Every provider case has at least one detection beyond the broad stub.
4. A selected Python case could be skipped, unexecuted or omitted while another failure certified detection. Producers now require completed selected calls; the parent validator independently reconstructs the exact selected ordinary-case set from the baseline and rejects missing rows and setup/teardown errors.
5. Assertion words in a traceback source line could certify an unrelated exception. Attribution now requires a real pytest assertion or the anchored expected exception type. Counterfactuals include misleading exception messages containing assertion/type names.
6. Standalone Python audit evidence previously fingerprinted sources only after execution. It now pins application/test/tool hashes before baseline and checks them before faults and after execution. A synthetic source-drift control proves rejection.
7. Quiz worker exit status could substitute for a failed assertion. The TAP classifier requires a complete unique sequence, exact plan/totals, no skipped/cancelled/TODO cases and an actual failed case. The parent independently rejects missing or contradictory fault outcomes.
8. Browser navigation/setup/timeouts/cleanup could count as mutation detections. Only explicit behavior assertions during the check phase count; script startup errors have their own assertion before locator work. The parent checks phase and assertion metadata.
9. Database lifecycle fixture failures could count as behavior failures. Setup SQL/assertion failures are invalid; behavior assertions and the deliberately induced lock timeout remain distinct valid detections. Synthetic controls run without a database to prove classification.
10. A nested CLI process could outlive its timed-out owner. Linux child processes now register a parent-death signal and check the registration race. A real bounded nested-timeout control fails when the signal is disabled and reaps its owned synthetic child.

These are targeted repairs to behavior and verification. No expected application outcome was weakened. All 808 original Python case/subtest IDs and 291 original fault catalogue entries remain; eight cases and thirteen fault entries were added. SQL, quiz, browser, lifecycle and migration inventories remain unchanged. No retained case/fault was removed to improve speed. Faulty implementations run only in isolated processes/copies or guarded disposable database transactions.

## Necessity and evidence interpretation

The [individual historical index](test-necessity-review/complete-case-index.csv) and its linked reviews provide earlier per-case rationales and dispositions. The current SQL review still matches all 382 SQL scripts and 607 case/fault applications; the current quiz review matches the HTML/JavaScript inputs for all 37 logic faults. Historical manifests are not relabeled as current: the changed probe and infrastructure receive fresh execution/source evidence. Day 7's API mapping and Day 9's D-case map supplement that index. Parameterized byte offsets and different privilege/state/Unicode boundaries remain separate even when their current kill sets coincide.

The new [complete evidence matrix](precommit-suite-audit-evidence.json.gz) records each retained Python baseline outcome, selected fault execution outcome, detection matrix, SQL case/fault outcome, quiz outcome, browser/lifecycle outcome, migration control and new runner control. It links necessity to the existing reviewed sources and named contracts. Raw private environments, connection values, arbitrary runtime logs and database access paths are excluded. Compressed evidence is reviewed after expansion.

A demonstrated fault kill proves sensitivity to that specific change. It does not prove all assertions indispensable, all possible defects absent, model quality or safe future transport. Three proven aliases and four excluded startup diagnostics remain explicit; exclusions are not detections.

## Performance

The safe second pass changes reporting only: compact JSON preserves the complete data, and one reverse detection index replaces repeated case-by-fault scans. Worker limits, fresh baselines, inventories, fault scopes, deadlines, database isolation and cleanup remain intact. No SDK, new dependency, async stack or global configuration was added.

For the same 18,951,459-byte decoded report, five serial samples measured median JSON serialization of 0.5475 seconds with indentation and 0.0974 seconds compactly. Compact size was 15,001,380 bytes, about 20.8% smaller. Round-trip decoding produced the identical object. These are reporting measurements, not a promise of equivalent end-to-end acceleration.

The complete correctness baseline took 56.504894 seconds. The first optimized complete run took 60.218757 seconds; a short concurrent serialization benchmark makes it unsuitable for a clean speed comparison. All individual baseline/fault outcomes, selected scopes and detection sets matched exactly. Final clean run and fresh CI-entry results are recorded in the [results receipt](precommit-suite-audit-results.json). Host load, process startup and database/browser scheduling vary; no globally fastest or statistically established total-suite speedup is claimed.

## Latest complete local result

All ten stages passed in 57.370795 seconds. The baseline passed 1,196 Python/database tests plus three subtests and 40 quiz cases. All 816 Python case/subtest IDs demonstrate detection; all 297 canonical faults were detected, including 47 provider faults. All 467 provider cases have a narrower witness beyond the fail-open stub. The unchanged SQL, browser, lifecycle and migration inventories passed; preservation and owned cleanup passed. The 149 runner controls and five Python-isolation controls passed. No unexpected survivor, invalid experiment, timeout or unapplied fault remains in the final complete run.

The actual CI entry point also passed on fresh synthetic storage in 99.341 seconds, including original-source Python checks, the complete suite, a separate committed migration roundtrip, source preservation and owned cleanup. This remains local CI execution for unpublished inputs; it is not hosted proof. Final evidence-only documentation edits were checked after execution.

## Publication boundary

Final local results and source fingerprints are recorded in the receipt. Hosted verification remains PENDING for uncommitted inputs. The earlier 4.1/4.2–4.4 receipts and pre-commit review are historical snapshots superseded by this audit for changed technical sources. Learner-guided explanation remains complete as recorded; the assistant's repairs do not establish independent learner authorship.

📚 Learn first: [cumulative exact-commit CI gate](../delivery/cumulative-ci-gate.md) and [Day 9 handoff](../planning/day-nine-handoff.md).
↩ Return: review the final diff and evidence; commit/push only after separate authorization, then observe every required hosted job for that exact revision before closing 4.4 or beginning Day 10.
