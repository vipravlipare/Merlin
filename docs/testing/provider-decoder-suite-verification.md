# Day 9 items 4.2–4.4: decoder fault and retained-suite verification

Later pre-commit audit: [cumulative suite audit](precommit-suite-audit.md) supersedes the technical counts, source fingerprints and runtime evidence below. It repairs additional decoder/verification gaps and retains all earlier cases/faults. Earlier learning and publication states remain attributed as recorded; hosted proof is still pending.

Recorded October 23, 2026. The learner explicitly authorized assistant completion of 4.2–4.4, excluding commit authorization. **4.2 PASS; 4.3 PASS locally, including fresh synthetic CI-entry execution; 4.4 local results recorded, hosted proof PENDING publication.** No project commit, push, workflow dispatch, live model request or provider transport was performed. Learner explain-back remains separately pending. Actual work minutes are unknown; the 10/9/5-minute planned allocations are not measured effort and must not be reported as achieved time boxes.

📚 Learn first: [4.1 baseline and D-case map](provider-decoder-baseline-review.md); [complete-suite command and safety boundaries](test-suite-commands.md); [cumulative CI gate](../delivery/cumulative-ci-gate.md).
↩ Return: inspect the results below and representative intended failures, then complete the learner explanations and section 5. Publication and the exact hosted run require their separate authorization; retain every deferred transport obligation.

## Final observed results

| Required check | Actual outcome |
|---|---|
| Expanded provider baseline | All 459 retained cases pass; UTF-8 fixture strengthened without changing its expected invalid-response outcome |
| Entire Python/database baseline | 1,188 tests plus three subtests PASS in the complete suite |
| Quiz baseline | 40 cases PASS |
| Python effectiveness | All **808 case/subtest IDs** demonstrate fault detection; **284 canonical faults DETECTED**, zero unexpected survivors, invalid runs, timeouts or unapplied faults |
| New provider effectiveness | All **34 provider faults** DETECTED by their required case/assertion; every provider case demonstrates detection |
| Existing attribution categories | Three proven aliases and four explicitly excluded startup diagnostics preserved; exclusions are not successful detections |
| SQL/quiz/browser/lifecycle/migration gates | All retained stages and inventories PASS; no required stage skipped or assertion weakened |
| Runner and result validation | **120 controls PASS**, including provider attribution, scope fallback, unreviewed side-effect fault refusal, imported-parent refusal and contradictory-result rejection |
| Complete ten-stage run | **PASS in 74.937830 seconds**, measured from runner start/finish; first final failed stage: none |
| Source preservation / owned-copy cleanup | Both PASS for the full run |
| Actual CI entry point on fresh synthetic storage | **PASS in 123.009 seconds**: original-source Python checks, complete suite, separate committed migration roundtrip and cleanup |
| Fresh-target suite within that CI execution | PASS in 89.116166 seconds; independent run, not reused results |
| Separate committed migration rehearsal | All **383 rebuilt case IDs**, semantic checks, reconnect, source preservation and owned cleanup PASS |
| Hosted proof for expanded source | **PENDING**. The local CI receipt identifies base commit 235ee974a3a95628be7ae9cb5f84ae31463709b3 plus uncommitted inputs. It is not a hosted result for that old commit or a future commit. |

Runtime differences reflect different runs, preparation and host load; no speed improvement is claimed. The ten-stage wall time includes guarded preparation/preflight, baselines and faults. The fresh CI-entry wall time also includes fresh provisioning and the separate committed rehearsal, but excludes the earlier pinned-image build/browser installation. Test runtimes are not learner or assistant work minutes.

Durable evidence:

- [Allowlisted summary, source hashes, stage outcomes, controls and initial failures](provider-decoder-verification-results.json).
- [Compressed provider case/fault matrix and synthetic intended-failure witnesses](provider-decoder-effectiveness-evidence.json.gz). Expanded contents were inspected before compression and rechecked after decompression. All 459 provider case IDs and all 34 fault outcomes remain available.
- [Earlier 4.1 receipt](provider-decoder-baseline-results.json) remains historical and is not relabeled with the later strengthened test-file hash.

Raw local run directories are `/tmp/merlin-provider-complete-suite` and `/tmp/merlin-provider-fresh-ci`. They may disappear after restarts and are not automatic publication artifacts. Durable evidence omits private environments, connection values, arbitrary logs, infrastructure access details and full raw audit reports. The compressed artifact retains bounded synthetic assertion excerpts rather than private runtime traces. A finite pattern/local-value scan does not guarantee universal confidentiality or production security.

## Implemented fault catalogue and necessity

The new tools/provider_faults.py is a catalogue for the existing audit, not a second runner. Each faulty source executes only in fresh isolated child memory or disposable files. No faulty application or database implementation was installed. The existing Python audit retains baseline-first execution, source hashes, exact selected-case manifests, timeouts and fresh workers.

| Provider faults | Requirement protected / intended observation |
|---|---|
| accept-unvalidated-answer | Known-invalid top-level input must not become any returned answer; expected exception assertion fails against a fail-open stub. This broad fault also witnesses negative-case effectiveness; it does not replace the narrower faults below. |
| wrong-fragment; no-fragment | Exact ordered text and accepted fragment retention, including direct record-level tests |
| drop-split-tail | Incomplete buffers survive arbitrary reads; one-byte fragmentation must preserve output |
| utf8-replacement | Invalid UTF-8 must be rejected rather than silently replaced |
| source-replay | One source traversal, no automatic retry after a source failure |
| record-cap; total-cap; character-count | Unfinished/complete record cap, all-response cap and wire-byte rather than character accounting |
| duplicate-key; nonfinite-constant; overflow-float | Strict JSON including nested names, named non-finite constants and overflowing exponents |
| error-truthiness; error-after-terminal | Error-member presence and precedence over success/state, including malformed values |
| model-identity; done-type | Trusted model identity and genuine Boolean completion |
| token-type; token-cap | Genuine nonnegative integer metadata and output-token ceiling |
| require-terminal-text; terminal-response-type | Metadata-only terminals allowed; a present response must remain a string |
| post-terminal; early-success | One completion and no early return before clean source termination |
| length-limit; trust-eof; empty-answer | Length-limit category, required completion and nonempty smoke answer |
| discard-tail; all-tail-incomplete; all-tail-invalid | Valid final record without LF, malformed-versus-unfinished distinction |
| source-raw-error; source-leak; parser-leak | Fixed source/parser failures, safe ordinary diagnostics and displayed exception-chain suppression |
| caller-close | Decoder respects caller-owned source cleanup |
| network-side-effect; process-side-effect | Guarded tests detect attempted network/process work before any external operation occurs |

All faults require a named case and a matching observed failure category. Provider attribution is independently recomputed by the suite validator from actual failed-call evidence; a DETECTED label, another failing test, a missing collection or a setup error cannot substitute. Representative cases are pinned to exact parameterized node IDs. The case-level matrix preserves all relevant detections, not only the representative witness. Related cases remain necessary because they exercise distinct D-case inputs, offsets or privilege/ownership boundaries; a shared mutation kill is not used to remove coverage.

The network/process mutants are special: the audit requires the exact reviewed provider-test hash and runs them only in the three retained side-effect-trap cases. Those cases intercept the relevant standard-library operations before invoking mutated code. A changed test source refuses these dangerous fault experiments. Ordinary provider faults use the reviewed dependency graph, with conservative all-Python fallback for changed/unknown tests, opaque imports or shared fixtures. The pristine fork parent now explicitly refuses an imported provider module.

## Suite integration and preservation of earlier work

Changed the existing audit, dependency scoping, result validator and control fixtures to recognize provider faults and their intended assertions. Explicitly appended **459 provider case IDs and 34 fault IDs** to the reviewed inventory; earlier case/fault prefixes, alias mappings and every SQL/JavaScript/browser/lifecycle/migration inventory remain intact. Inventory is never regenerated at runtime to excuse missing coverage. The ordinary discovery baseline and the fault baseline now validate against the same expanded required set.

The existing workflow already invokes tools/run_ci.py, which invokes the complete suite and separate migration rehearsal. **No workflow change was needed.** The local fresh-target execution used the same pinned CI PostgreSQL image recipe, independently generated synthetic storage and the wrapper's explicit include-untracked option. It did not rely on the personal database for CI provisioning. The ordinary local suite still checked/preserved its established guarded source before using independent copies.

Application source and applied migrations were unchanged in this task. The only provider-test behavior change strengthened an invalid-UTF8 fixture. No model/runtime upgrade, new project dependency, SDK, async stack or global configuration was introduced. Restored test-only temporary browser dependencies remain outside versioned application inputs.

## Initial failures and why they do not count as detections

The first 31-fault trial produced 25 intended detections, four SURVIVED and two INVALID. These outcomes remain in the receipt. The byte-accounting mutant initially altered the scanning length rather than isolating accounting; it was corrected to mutate cumulative counting only. The duplicate-key representative initially failed for wrong model identity instead of duplicate-key rejection; the required witness was changed to the valid duplicate-completion case. The Boolean-type mutation produced a missing-exception failure, so its assertion attribution was corrected to that actual expected failure. The parser-chain mutation did not expose a sentinel through JSONDecodeError's message, so it was attributed to the existing explicit chain-suppression assertion. None of these repairs loosened an application oracle.

The two side-effect experiments were INVALID because their selected function-level selector did not match the independently computed exact node manifest, despite trap assertions firing. Explicitly selecting the three parameterized node IDs repaired manifest accounting without skipping the traps or broadening execution.

Adding split-tail, UTF-8 and replay faults expanded the catalogue to 34. The UTF-8 replacement fault then SURVIVED its intended case: the fixture lacked mandatory model/done fields, so schema validation masked replacement decoding. The fixture now contains otherwise-valid model/response/done JSON and a valid terminal. Strict decoding still must reject it; replacement decoding now wrongly succeeds and fails the intended missing-exception assertion. The original failure and survivor are retained; a fixture-only rejection was not counted as successful UTF-8 proof. Final full-suite and fresh-CI executions detected all 34 faults with the repaired fixture.

The first prerequisite attempt also failed because Docker's WSL integration was temporarily unavailable. The learner stated it should already be enabled; a retry reached the daemon without altering its settings or replacing its connection. The pinned temporary browser installation was missing. Its initial installer rejected the host's Ubuntu 26.04 target; the project's documented Ubuntu 24.04 compatibility override plus temporary browser/library paths restored the required pinned Chromium launch. Missing runtime libraries were downloaded from the configured Ubuntu repository and extracted only into `/tmp`, not installed globally. No timeout, identity check, browser pin or required stage was relaxed. All failures consumed real effort; actual effort minutes remain unknown.

## Remaining ownership and next step

4.2 and 4.3 technical work is assistant-authored under this task's explicit authorization. The learner still reviews representative faults and completes the corrected 3.2 explanation. The learner's earlier 3.4 extraction remains attributed separately from the assistant cleanup.

4.4 is complete for local recording and remains **open only for publication and exact hosted verification**. No commit/push authorization was requested or inferred, and none was performed. A later approved publication must include the reviewed implementation, tests, catalogue, inventory, validators and evidence; observe every required hosted step for that exact revision. New evidence-document additions after these executions require their own documentation checks; they do not retroactively change the tested source hashes.

Day 9 remains parser-only. Actual HTTP status/media handling, deadlines, proxy/redirect/fallback guards, network cleanup and in-flight cancellation remain deferred transport work. Learner explanation, section 5 review/handoff and actual-time attribution retain their own states. Do not close MER-10 or start Day 10 from local PASS alone.

📚 Learn first: [Day 9 checklist](../sprints/day-nine-jira-checklist.md), sections 4–5; [transport carryover](../architecture/local-provider-transport-assessment.md), LP-16–22/24.
↩ Return: review one framing fault, one validation fault and the UTF-8 fixture repair; finish the learner explain-back and section 5. Keep 4.4 hosted proof pending until separately authorized publication has actually passed.
