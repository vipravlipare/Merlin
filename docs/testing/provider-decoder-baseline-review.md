# Day 9 item 4.1: retained decoder baseline review

Recorded October 23, 2026. The learner explicitly authorized the assistant to complete 4.1, including test changes, and inspect the division of work for 4.2–4.4. **4.1 PASS for the implemented byte-only decoder.** The assistant extended tests/test_local_provider.py; application code, fault harness, suite inventory, CI, services and databases were not changed. Actual working minutes are unknown; the planned 12 minutes is not an observed effort total.

📚 Learn first: [D-01–D-38 input/oracle contract](../architecture/local-provider-contract.md#day-9-item-22--decoder-inputs-and-expected-results); [existing complete-suite requirements](test-suite-commands.md), retained checks and isolation.
↩ Return: inspect the map below alongside the retained test functions, then review the ownership table before starting 4.2. This baseline is protocol verification, not a model-quality golden set or a working HTTP transport.

Later October 23 update: [4.2–4.4 technical execution](provider-decoder-suite-verification.md) supersedes the later-step planning statuses below. A masked UTF-8 fixture was strengthened during effectiveness work; the original 4.1 file hash/receipt remains historical.

## Observed results and changes

| Check | Actual result |
|---|---|
| Starting retained provider baseline | 117 PASS in 0.22 seconds |
| Expanded provider baseline | **459 PASS in 0.71 seconds**, zero failed/skipped cases; outcome-only pytest plugin recorded every collected node and setup/call/teardown outcome |
| Baseline capture wall time | 0.760712278 seconds including pytest invocation/reporting overhead; distinct from pytest's rounded duration |
| Final provider plus nearest regressions | **691 PASS in 3.56 seconds**: 459 provider cases plus 232 existing note/maintenance/API/probe cases |
| Whitespace and documentation | Direct checks include untracked source/test files; documentation lint/whitespace results recorded at final validation, not inferred from pytest |
| Application source | SHA-256 unchanged: 5ef81d42a4af25d1ca4ee3eda777d7361626be6135d468ccfa15dc6303e589bb |
| Expanded test source | SHA-256: 8cf3a6855baa46baaf150ae33f2ae34aff1f1677940beb088165d068a457b976 |
| Fault effectiveness / full suite / hosted CI | Not performed by this baseline; remain 4.2–4.4 |

Durable synthetic evidence: [case-level outcomes and file identities](provider-decoder-baseline-results.json). It stores no private payloads, credentials, raw traceback logs or environment dumps. Every retained node must pass, including setup and teardown; a green summary alone is insufficient. Finite coverage does not prove that all possible defects are absent.

Provider command: `.venv/bin/python -m pytest -q tests/test_local_provider.py`. The case receipt invokes the same arguments through pytest.main with a plugin that records only outcomes. Combined regression command: `.venv/bin/python -m pytest -q tests/test_local_provider.py tests/test_note_rules_and_maintenance.py tests/test_health_api.py tests/test_database_connectivity_probe.py`. Disposable loopback API fixtures required execution outside the socket-restricted sandbox; provider-only checks need no sockets, GPU, downloaded model or personal service.

Added missing retained cases for canonical ASCII assembly/splits, individually named multibyte splits, line-ending boundaries, top-level shapes, duplicate identity/text keys, corruption after partial output, terminal identity/token limits, complete-stream byte boundaries, ignored Unicode metadata, blank floods, safe diagnostics and external-call traps. The padded-record fixture now builds exact ASCII or Unicode wire sizes and terminal/nonterminal records while retaining original assertions. No application expectation was weakened.

The two earlier delimiter-free-tail cases previously looped over offsets internally; the same assertions are now individually parameterized. New IDs are deliberate and must be reconciled in 4.3 rather than silently regenerated at runtime. Existing Unicode all-split/one-byte checks remain, protecting their original input boundaries. Raw case count is not a count of independent product requirements: many nodes are distinct offsets/variants of the same requirement.

## Complete decoder requirement map

All named functions below are in tests/test_local_provider.py. PASS refers to baseline behavior, not demonstrated fault effectiveness. Parameter values and exact node IDs are in the linked receipt. Some related existing checks also cover a row; the table names the primary retained oracles rather than duplicating every overlapping assertion.

| Contract | Primary retained test function(s) | Boundary / actual status |
|---|---|---|
| D-01 | test_contract_ordered_ascii_assembly | Separate A/B/T records return exact Hello!; PASS |
| D-02 | test_contract_each_two_piece_split | Every internal canonical byte offset independently collected; exact Hello!; PASS |
| D-03 | test_contract_one_byte_chunks_with_interleaved_empty_chunks | Successive one-byte fragments with empties before/between/after; PASS |
| D-04 | test_contract_ordered_ascii_assembly | Coalesced A/B/T consumes every record; PASS |
| D-05 | test_contract_each_multibyte_split; test_every_split_preserves_unicode_and_order | Named splits inside é and emoji encodings plus original whole-wire splits; PASS |
| D-06 | test_contract_record_endings_with_split_crlf | LF, CRLF and mixed endings, split CR/LF where present; PASS |
| D-07 | test_contract_blank_records_before_between_and_after_text | Bounded whitespace records at all three positions; PASS |
| D-08 | test_final_record_without_newline_accepts_every_split | Terminal text and metadata-only terminal, every final-wire split independently collected; PASS |
| D-09 | test_contract_corruption_after_partial_text | Malformed LF-terminated JSON after accepted text fails invalid-response; PASS |
| D-10 | test_duplicate_keys_are_rejected_at_every_object_level; test_contract_duplicate_identity_and_text_keys | Duplicate done/model/response plus nested keys; PASS |
| D-11 | test_nonfinite_numbers_are_rejected_even_in_nested_metadata | NaN, ±Infinity and exponent overflow in metadata; PASS |
| D-12 | test_contract_corruption_after_partial_text | Invalid UTF-8 in a complete line fails invalid-response; PASS |
| D-13 | test_truncated_record_does_not_return_preceding_text; test_unfinished_final_record_is_incomplete | Unfinished JSON at EOF cannot return prior text; PASS |
| D-14 | test_contract_corruption_after_partial_text | Incomplete multibyte EOF tail fails incomplete-response; PASS |
| D-15 | test_missing_completion_or_empty_answer_is_incomplete; test_contract_additional_state_and_schema_boundaries | Empty, blanks, one/multiple text records without terminal; PASS |
| D-16 | test_contract_top_level_shapes | Array/string/null/Boolean/number rejected independently; PASS |
| D-17 | test_schema_rejects_wrong_identity_types_and_token_metadata; test_required_nonterminal_fields_cannot_be_missing; test_contract_additional_state_and_schema_boundaries | Mandatory Boolean done and response string, including object response; PASS |
| D-18 | test_required_nonterminal_fields_cannot_be_missing; test_schema_rejects_wrong_identity_types_and_token_metadata; test_contract_additional_state_and_schema_boundaries | Missing/non-string/wrong first model and terminal-only identity change; PASS |
| D-19 | test_metadata_completion_waits_for_clean_eof | Absent/empty terminal response after text; PASS |
| D-20 | test_contract_bare_error_object; test_error_precedence_including_after_terminal | Bare error before/after text and error plus success-shaped fields; PASS; HTTP status handling deferred |
| D-21 | test_error_precedence_including_after_terminal | Null/false/number/object error values cannot become success; PASS |
| D-22 | test_nonblank_data_after_completion_is_invalid | Duplicate terminal rejected in same/later chunk; PASS |
| D-23 | test_nonblank_data_after_completion_is_invalid | Ordinary record, malformed/unfinished/non-UTF8 data after terminal; PASS |
| D-24 | test_contract_empty_fragment_before_real_answer; test_missing_completion_or_empty_answer_is_incomplete | Empty fragments allowed before real text; wholly empty terminal outcome rejected; PASS |
| D-25 | test_contract_complete_stream_record_byte_boundary; test_record_cap_accepts_exact_boundary_and_rejects_one_over_before_copy | 65,536 accepted, 65,537 rejected before copying, delimiter accounting and complete-stream use; PASS |
| D-26 | test_contract_small_chunks_enforce_unfinished_buffer_cap_immediately | Incremental 1 KiB unfinished input crosses cap; no wait for LF/EOF; PASS |
| D-27 | test_contract_total_cap_counts_ignored_metadata_bytes; test_complete_stream_keeps_total_and_post_terminal_byte_limits | Valid records/terminal total exactly 262,144; one extra blank byte rejected; PASS |
| D-28 | test_contract_blank_only_flood_cannot_bypass_aggregate_limit | Individually tiny blank records cumulatively exceed total cap; PASS |
| D-29 | test_contract_complete_stream_record_byte_boundary; test_contract_total_cap_counts_ignored_metadata_bytes | Unicode metadata tests wire bytes rather than decoded character counts at both caps; PASS |
| D-30 | test_contract_private_markers_absent_from_all_public_diagnostics; test_source_failure_is_safe_and_never_replayed; test_source_acquisition_failure_is_safe | Synthetic provider/JSON/UTF8/source markers absent from public error, formatted chain, stdout/stderr and ordinary logs; PASS |
| D-31 | test_source_failure_is_safe_and_never_replayed; test_failure_does_not_consume_more_source_or_close_caller_resource | One source iteration, no replay or accepted partial answer; stop on selected failure; PASS |
| D-32 | test_source_failure_is_safe_and_never_replayed | Source failure after terminal remains provider-failure; PASS |
| D-33 | test_unknown_metadata_and_mixed_line_endings_preserve_text; test_contract_ordered_ascii_assembly | Safe unknown metadata and absent optional metrics preserve exact text; public result remains str, no metric fabrication; PASS |
| D-34 | test_length_policy_respects_validation_precedence | Valid length termination distinct from normal success; PASS |
| D-35 | test_contract_terminal_token_metadata; test_length_policy_respects_validation_precedence | Terminal count64 allowed,65 rejected, wrong-type/negative counts rejected, higher-priority validation preserved; PASS |
| D-36 | test_invalid_chunk_type_has_safe_error; one-byte empty-chunk cases | str/None/bytearray/integer rejected; empty bytes allowed; PASS |
| D-37 | test_contract_decoder_has_zero_external_side_effects | Success, provider error and malformed JSON execute with traps for socket creation/connection, standard HTTP/URL entry points, subprocesses, shell calls and process kills; zero calls; PASS |
| D-38 | test_caller_keeps_source_cleanup_ownership | Decoder never closes caller-owned source; caller closes once on success/error; PASS for fake source ownership only |

D-37 intercepts the named standard-library entry points; it is not universal proof against arbitrary future libraries or every possible operating-system interface. There is no decoder model-management API, and the subprocess/HTTP/process traps protect the expected paths by which such management might be attempted. New external dependencies would require revisiting these traps.

HTTP-200/non-2xx/media-type handling, real response/connection cleanup, cancellation, blocked reads, idle/absolute deadlines and redirect/proxy/hosted routing stay **PENDING transport**. The decoder sees supplied bytes, not an HTTP status. No HTTP 200 was invented for synthetic records. D-38 proves caller-owned fake-source cleanup, not network cleanup or a new safe cleanup-error API. See [3.3 transport deferral](../architecture/local-provider-transport-assessment.md).

## What 4.2–4.4 require from assistant and learner

This turn completes 4.1 and performs read-only planning for later steps. It does not grant blanket permission for new application/harness/CI edits or publication. The learner can explicitly delegate the technical tasks below; independent understanding remains learner work.

| Step | Technical work the assistant can do when delegated | What remains with the learner | Current state |
|---|---|---|---|
| 4.2 effectiveness | Build/reuse isolated source faults for every required decoder boundary; run retained cases; require intended assertion failures; record every case/fault outcome, surviving/invalid/unexecuted experiments and necessity rationale. Prove trap/ownership tests detect relevant faults too. | Review representative original failures and explain what each test detects. No requirement to manually type every fault if assistance is explicitly authorized. | Not completed. Earlier four 3.2 observations are historical and do not certify this expanded 459-case set. |
| 4.3 retained verification | Extend the existing Python audit's provider fault catalogue/attribution, dependency scoping and conservative fallbacks; explicitly review and add the new case/fault inventory; update result-validator/control fixtures; run the complete guarded suite with prior SQL/browser/lifecycle/migration checks retained. Verify clean-runner compatibility without Ollama. | Review scope/authorship and supplied evidence; authorize those particular test/harness changes if delegating. No new manual application feature is inherently needed for this verification. | Not started. Ordinary test discovery finds provider tests, but the reviewed inventory/fault gates do not yet include them. |
| 4.4 results/publication | Record exact local PASS/FAIL/PENDING, first failure and complete-suite duration. After separately authorized commit/push, inspect required hosted jobs/steps for the exact new commit and record their evidence. | Confirm any remembered actual minutes, otherwise leave unknown; decide whether to authorize publication. No credentials or account-security details need to be pasted. | Local 4.1 results recorded; complete-suite and expanded-source hosted proof PENDING. |

Specific 4.3 integration points inspected: tools/audit_python_cases.py currently has health-API-specific intended detections and a general baseline; tools/test_dependencies.py has reviewed source targets without the provider module; tests/suite-inventory.json has no provider case/fault IDs; tools/run_test_suite.py requires exact inventory equality and relevant fault detection for every retained Python case. tools/verify_suite_execution.py supplies validator/control fixtures that must evolve consistently. tools/run_ci.py already wraps the suite and migration rehearsal; inspect compatibility before deciding whether it needs an edit. Do not assume a workflow change is required, or regenerate the inventory automatically to hide mismatches.

The full runner is deliberately not run merely to obtain a green label before provider fault/inventory integration: its exact inventory requirements are known to be unfinished. That is recorded carryover, not a reason to skip required stages or weaken result validation. Missing prerequisites or harness failures must be repaired within the existing time allocation or carried forward explicitly.

The earlier 3.2 corrected explain-back remains open. Completing assistant-authored tests does not substitute for it. There is no requirement to answer those questions before these finite synthetic tests can run, but the learning/story closeout must not falsely mark that proof complete.

📚 Learn first: [Day 9 sections 4–5](../sprints/day-nine-jira-checklist.md), exact obligations and stop rule; [effectiveness review principles](case-effectiveness-audit.md), distinguish intended assertion failures from fixture failures.
↩ Return: review this baseline receipt, then choose learner implementation or explicit delegation for 4.2/4.3. Keep MER-10 open, transport deferred and publication pending its own authorization. Actual effort beyond the 12-minute plan displaces optional work; no extra hours are invented.
