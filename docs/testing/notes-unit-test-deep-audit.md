# Deep review of every current unit case

This review follows the earlier [original-case audit](notes-unit-test-audit.md). Each current test function and each parameter input was read against the helper/worker contract. The table includes an actual pytest result for every collected case; there are no skipped or expected-failure placeholders. The conclusions below were written manually; pytest metadata only supplied case labels, inputs and observed outcomes.

## What changed after the second review

The original useful boundary/normalization/target cases remain. Added direct scheduler tests cover --once, repeated default/custom intervals, invalid intervals, Ctrl+C and sanitized failure messages. Their time and database operations are replaced so no real waiting or connection occurs. A whole-file guard refuses accidental real connections. The --once fixture raises on any second cycle, so a broken loop cannot hang the audit and cannot appear to pass.

Added type-edge cases exposed genuine missing validation. These are helper-boundary tests, not claims that an existing API accepts these values: no API exists. Draft BOOLEAN and SQL INTEGER are the declared data contracts. A helper annotation alone does not enforce either contract at runtime.

### Confirmed findings

1. True,1.5and1.0 batches pass the numeric range check and reach the connector. They should be rejected as noninteger batch values.
2. None and text batches stop before a connection, but raise incidental TypeError rather than a deliberate validation ValueError. This is inconsistent error handling, not a demonstrated database write.
3. Draft flags text "false", integer1andNone are silently accepted. Text "false" is truthy and prevents blank-note deletion, so coercion can produce the wrong decision.

The two previously failing checks remain failing. No application code was changed to hide failures. Current run:82PASS/8FAIL. These are runner outcomes, not82distinct rules or complete backend coverage.

## Rules used for this review

COUNT: pinned displayed-character/emoji weighting. TITLE/BODY:175/7000 weighted limits. BLANK/TEXT: blank-title normalization, draft preservation, saved-blank deletion decision and real-text preservation. EMAIL: optional normalized input with original display casing. TARGET: known disposable database/cluster only. BATCH: integer1–1000 and bound query values. WORKER: bounded-cycle call sequence and exception propagation. SCHEDULER: foreground CLI behavior and safe terminal messages. Type checks are boundary hardening for the declared field/argument types.

A mock case is retained only when it checks Python refusal, control flow, parameters or output. It is never counted as SQL deletion, commit, rollback, locks, grants or ownership evidence.

## Current cases, individually

Input previews abbreviate very long text; the test source retains the complete input. The displayed code-point length in an abbreviated preview identifies the input, not its weighted expected count. Each row's purpose corresponds to a manually reviewed assertion and a declared rule.

| Case | Function | Input | Rule / required evidence | Actual |
|---|---|---|---|---|
| C001 | test_display_character_weights | text='abc !', count=5 | COUNT: Exact independent count supplied by each row; covers a distinct displayed-character form. | PASSED |
| C002 | test_display_character_weights | text='😀', count=4 | COUNT: Exact independent count supplied by each row; covers a distinct displayed-character form. | PASSED |
| C003 | test_display_character_weights | text='👨\u200d👩\u200d👧\u200d👦', count=4 | COUNT: Exact independent count supplied by each row; covers a distinct displayed-character form. | PASSED |
| C004 | test_display_character_weights | text='👍🏽', count=4 | COUNT: Exact independent count supplied by each row; covers a distinct displayed-character form. | PASSED |
| C005 | test_display_character_weights | text='🇺🇸', count=4 | COUNT: Exact independent count supplied by each row; covers a distinct displayed-character form. | PASSED |
| C006 | test_display_character_weights | text='1️⃣', count=4 | COUNT: Exact independent count supplied by each row; covers a distinct displayed-character form. | PASSED |
| C007 | test_display_character_weights | text='é', count=1 | COUNT: Exact independent count supplied by each row; covers a distinct displayed-character form. | PASSED |
| C008 | test_display_character_weights | text='\n', count=1 | COUNT: Exact independent count supplied by each row; covers a distinct displayed-character form. | PASSED |
| C009 | test_title_boundary_with_emoji_sequence | fixed fixture in function | TITLE: Mixed weighted175 accepted unchanged;176 rejected specifically as a title error. | PASSED |
| C010 | test_body_boundary | fixed fixture in function | BODY: 1750emoji accepted unchanged;1751 rejected specifically as a body error. | PASSED |
| C011 | test_wrong_target_never_calls_cleanup | database='merlin', cluster=7694311451826794534 | TARGET: Reject wrong database or preserved cluster; identity read is the only SQL call. | PASSED |
| C012 | test_wrong_target_never_calls_cleanup | database='merlin_d6', cluster=7691749973399031842 | TARGET: Reject wrong database or preserved cluster; identity read is the only SQL call. | PASSED |
| C013 | test_worker_cycle_verifies_then_uses_bounded_functions | fixed fixture in function | WORKER: Verify target; call correct expiry/purge functions in order with batch25; return2/3; clean context exit. | PASSED |
| C014 | test_more_display_sequences | text='', expected=0 | COUNT: Exact independent count supplied by row; empty/special/non-ASCII/control/mixed sequences have distinct purposes. | PASSED |
| C015 | test_more_display_sequences | text='!@#', expected=3 | COUNT: Exact independent count supplied by row; empty/special/non-ASCII/control/mixed sequences have distinct purposes. | PASSED |
| C016 | test_more_display_sequences | text='中文', expected=2 | COUNT: Exact independent count supplied by row; empty/special/non-ASCII/control/mixed sequences have distinct purposes. | PASSED |
| C017 | test_more_display_sequences | text='\t\r\n', expected=2 | COUNT: Exact independent count supplied by row; empty/special/non-ASCII/control/mixed sequences have distinct purposes. | PASSED |
| C018 | test_more_display_sequences | text='a😀b', expected=6 | COUNT: Exact independent count supplied by row; empty/special/non-ASCII/control/mixed sequences have distinct purposes. | PASSED |
| C019 | test_more_display_sequences | text='👨\u200d👩\u200d👧\u200d👦😀', expected=8 | COUNT: Exact independent count supplied by row; empty/special/non-ASCII/control/mixed sequences have distinct purposes. | PASSED |
| C020 | test_more_display_sequences | text='©️', expected=4 | COUNT: Exact independent count supplied by row; empty/special/non-ASCII/control/mixed sequences have distinct purposes. | PASSED |
| C021 | test_more_display_sequences | text='👍🏽!', expected=5 | COUNT: Exact independent count supplied by row; empty/special/non-ASCII/control/mixed sequences have distinct purposes. | PASSED |
| C022 | test_plain_title_limit | size=174, accepted=True | TITLE: 174/175 accepted unchanged;176 rejected as title limit. Both sides of boundary matter. | PASSED |
| C023 | test_plain_title_limit | size=175, accepted=True | TITLE: 174/175 accepted unchanged;176 rejected as title limit. Both sides of boundary matter. | PASSED |
| C024 | test_plain_title_limit | size=176, accepted=False | TITLE: 174/175 accepted unchanged;176 rejected as title limit. Both sides of boundary matter. | PASSED |
| C025 | test_plain_body_limit | size=6999, accepted=True | BODY: 6999/7000 accepted unchanged;7001 rejected as body limit. | PASSED |
| C026 | test_plain_body_limit | size=7000, accepted=True | BODY: 6999/7000 accepted unchanged;7001 rejected as body limit. | PASSED |
| C027 | test_plain_body_limit | size=7001, accepted=False | BODY: 6999/7000 accepted unchanged;7001 rejected as body limit. | PASSED |
| C028 | test_over_limit_title_rejected_even_for_drafts | title='😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀' | TITLE/DRAFT: Named weighted176 input must reject; draft must not bypass title validation. | PASSED |
| C029 | test_over_limit_title_rejected_even_for_drafts | title='😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀abcd' | TITLE/DRAFT: Named weighted176 input must reject; draft must not bypass title validation. | PASSED |
| C030 | test_over_limit_title_rejected_even_for_drafts | title='ééééééééééééééééééééééée... (352 code points) | TITLE/DRAFT: Named weighted176 input must reject; draft must not bypass title validation. | PASSED |
| C031 | test_over_limit_body_rejected_even_for_drafts | body='👨\u200d👩\u200d👧\u200d👦👨\u200d👩\u200d👧\u200d👦👨\u... (12257 code points) | BODY/DRAFT: Named weighted7001/7004 input must reject; whitespace/draft must not bypass body validation. | PASSED |
| C032 | test_over_limit_body_rejected_even_for_drafts | body='😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀😀... (1751 code points) | BODY/DRAFT: Named weighted7001/7004 input must reject; whitespace/draft must not bypass body validation. | PASSED |
| C033 | test_over_limit_body_rejected_even_for_drafts | body='                                               ... (7001 code points) | BODY/DRAFT: Named weighted7001/7004 input must reject; whitespace/draft must not bypass body validation. | PASSED |
| C034 | test_empty_note_decision | draft=False, title=None, body=None | BLANK: Normalize absent title/body; preserve body whitespace; deletion decision must equal not draft. | PASSED |
| C035 | test_empty_note_decision | draft=False, title='', body='' | BLANK: Normalize absent title/body; preserve body whitespace; deletion decision must equal not draft. | PASSED |
| C036 | test_empty_note_decision | draft=False, title=' \t\n', body=' \r\n' | BLANK: Normalize absent title/body; preserve body whitespace; deletion decision must equal not draft. | PASSED |
| C037 | test_empty_note_decision | draft=False, title='\xa0', body='\xa0' | BLANK: Normalize absent title/body; preserve body whitespace; deletion decision must equal not draft. | PASSED |
| C038 | test_empty_note_decision | draft=True, title=None, body=None | BLANK: Normalize absent title/body; preserve body whitespace; deletion decision must equal not draft. | PASSED |
| C039 | test_empty_note_decision | draft=True, title='', body='' | BLANK: Normalize absent title/body; preserve body whitespace; deletion decision must equal not draft. | PASSED |
| C040 | test_empty_note_decision | draft=True, title=' \t\n', body=' \r\n' | BLANK: Normalize absent title/body; preserve body whitespace; deletion decision must equal not draft. | PASSED |
| C041 | test_empty_note_decision | draft=True, title='\xa0', body='\xa0' | BLANK: Normalize absent title/body; preserve body whitespace; deletion decision must equal not draft. | PASSED |
| C042 | test_nonblank_note_is_preserved | title='Title', body='' | TEXT: Keep exact title/body and return delete_on_save=False; legitimate text survives. | PASSED |
| C043 | test_nonblank_note_is_preserved | title=None, body='body' | TEXT: Keep exact title/body and return delete_on_save=False; legitimate text survives. | PASSED |
| C044 | test_nonblank_note_is_preserved | title=' 😀 ', body=' \nbody\n ' | TEXT: Keep exact title/body and return delete_on_save=False; legitimate text survives. | PASSED |
| C045 | test_count_rejects_invalid_text | value=None | TEXT-TYPE: Non-string raises specific text-type ValueError; NUL raises specific database-text ValueError. | PASSED |
| C046 | test_count_rejects_invalid_text | value=1 | TEXT-TYPE: Non-string raises specific text-type ValueError; NUL raises specific database-text ValueError. | PASSED |
| C047 | test_count_rejects_invalid_text | value=b'text' | TEXT-TYPE: Non-string raises specific text-type ValueError; NUL raises specific database-text ValueError. | PASSED |
| C048 | test_count_rejects_invalid_text | value='\x00' | TEXT-TYPE: Non-string raises specific text-type ValueError; NUL raises specific database-text ValueError. | PASSED |
| C049 | test_count_rejects_invalid_text | value='hello\x00' | TEXT-TYPE: Non-string raises specific text-type ValueError; NUL raises specific database-text ValueError. | PASSED |
| C050 | test_note_fields_reject_invalid_text | value=10, field='title' | TEXT-TYPE: Public title/body path must reject the named invalid type or NUL, not rely only on standalone counter tests. | PASSED |
| C051 | test_note_fields_reject_invalid_text | value=10, field='body' | TEXT-TYPE: Public title/body path must reject the named invalid type or NUL, not rely only on standalone counter tests. | PASSED |
| C052 | test_note_fields_reject_invalid_text | value=b'text', field='title' | TEXT-TYPE: Public title/body path must reject the named invalid type or NUL, not rely only on standalone counter tests. | PASSED |
| C053 | test_note_fields_reject_invalid_text | value=b'text', field='body' | TEXT-TYPE: Public title/body path must reject the named invalid type or NUL, not rely only on standalone counter tests. | PASSED |
| C054 | test_note_fields_reject_invalid_text | value='\x00', field='title' | TEXT-TYPE: Public title/body path must reject the named invalid type or NUL, not rely only on standalone counter tests. | PASSED |
| C055 | test_note_fields_reject_invalid_text | value='\x00', field='body' | TEXT-TYPE: Public title/body path must reject the named invalid type or NUL, not rely only on standalone counter tests. | PASSED |
| C056 | test_email_edge_whitespace | raw=None, expected=None | EMAIL: Exact row expected result: None for absent/blank; trimmed address retains casing. | PASSED |
| C057 | test_email_edge_whitespace | raw='', expected=None | EMAIL: Exact row expected result: None for absent/blank; trimmed address retains casing. | PASSED |
| C058 | test_email_edge_whitespace | raw='\t\n', expected=None | EMAIL: Exact row expected result: None for absent/blank; trimmed address retains casing. | PASSED |
| C059 | test_email_edge_whitespace | raw=' \tMixed@Example.COM\n ', expected='Mixed@Example.COM' | EMAIL: Exact row expected result: None for absent/blank; trimmed address retains casing. | PASSED |
| C060 | test_email_edge_whitespace | raw='\xa0a@b.test\xa0', expected='a@b.test' | EMAIL: Exact row expected result: None for absent/blank; trimmed address retains casing. | PASSED |
| C061 | test_email_rejects_invalid_database_text | value=10 | EMAIL: Named invalid type/NUL rejected with appropriate ValueError; no claim of verified email ownership. | PASSED |
| C062 | test_email_rejects_invalid_database_text | value=b'email' | EMAIL: Named invalid type/NUL rejected with appropriate ValueError; no claim of verified email ownership. | PASSED |
| C063 | test_email_rejects_invalid_database_text | value='a\x00@b.test' | EMAIL: Named invalid type/NUL rejected with appropriate ValueError; no claim of verified email ownership. | PASSED |
| C064 | test_invalid_batch_never_connects | size=-1 | BATCH: -1/0/1001 rejected as range errors before any connection. | PASSED |
| C065 | test_invalid_batch_never_connects | size=0 | BATCH: -1/0/1001 rejected as range errors before any connection. | PASSED |
| C066 | test_invalid_batch_never_connects | size=1001 | BATCH: -1/0/1001 rejected as range errors before any connection. | PASSED |
| C067 | test_allowed_batch_boundaries_and_fixed_target | size=1 | BATCH/TARGET: 1/1000 accepted; fixed loopback55432/merlin_d6; correct timeouts/function order/bindings; no-work result0/0. | PASSED |
| C068 | test_allowed_batch_boundaries_and_fixed_target | size=1000 | BATCH/TARGET: 1/1000 accepted; fixed loopback55432/merlin_d6; correct timeouts/function order/bindings; no-work result0/0. | PASSED |
| C069 | test_cleanup_failure_leaves_transaction_as_error | failure_stage='expiry' | WORKER-ERROR: Chosen operation failure reaches context exit as error; expiry failure also prevents purge. Actual rollback unproved. | PASSED |
| C070 | test_cleanup_failure_leaves_transaction_as_error | failure_stage='purge' | WORKER-ERROR: Chosen operation failure reaches context exit as error; expiry failure also prevents purge. Actual rollback unproved. | PASSED |
| C071 | test_blank_title_with_real_body | title='' | BLANK/TEXT: Empty/whitespace title becomesNone; actual body is preserved; no deletion requested. | PASSED |
| C072 | test_blank_title_with_real_body | title=' \t\n' | BLANK/TEXT: Empty/whitespace title becomesNone; actual body is preserved; no deletion requested. | PASSED |
| C073 | test_combining_characters_accepted_at_display_limit | field='title', size=175 | COUNT/LIMIT: 175accented title/7000accented body accepted unchanged; rejects a code-point-only validator. | PASSED |
| C074 | test_combining_characters_accepted_at_display_limit | field='body', size=7000 | COUNT/LIMIT: 175accented title/7000accented body accepted unchanged; rejects a code-point-only validator. | PASSED |
| C075 | test_noninteger_batch_rejected_before_connecting | size=True | BATCH-TYPE: Boolean/fraction should raise batch ValueError before connection; current worker instead attempts connection. | FAILED |
| C076 | test_noninteger_batch_rejected_before_connecting | size=1.5 | BATCH-TYPE: Boolean/fraction should raise batch ValueError before connection; current worker instead attempts connection. | FAILED |
| C077 | test_more_wrong_batch_types_rejected | size=1.0 | BATCH-TYPE: Whole float must not reach connector; None/string should give batch validation error, not incidental TypeError. | FAILED |
| C078 | test_more_wrong_batch_types_rejected | size=None | BATCH-TYPE: Whole float must not reach connector; None/string should give batch validation error, not incidental TypeError. | FAILED |
| C079 | test_more_wrong_batch_types_rejected | size='100' | BATCH-TYPE: Whole float must not reach connector; None/string should give batch validation error, not incidental TypeError. | FAILED |
| C080 | test_draft_flag_requires_boolean | draft='false' | DRAFT-TYPE: Draft flag is BOOLEAN; do not silently treat text/integer/None as a valid flag. Current helper lacks runtime enforcement. | FAILED |
| C081 | test_draft_flag_requires_boolean | draft=1 | DRAFT-TYPE: Draft flag is BOOLEAN; do not silently treat text/integer/None as a valid flag. Current helper lacks runtime enforcement. | FAILED |
| C082 | test_draft_flag_requires_boolean | draft=None | DRAFT-TYPE: Draft flag is BOOLEAN; do not silently treat text/integer/None as a valid flag. Current helper lacks runtime enforcement. | FAILED |
| C083 | test_cli_once_runs_one_cycle_without_sleep | fixed fixture in function | SCHEDULER: One prompt, one cycle, no sleep/second cycle; correct counts printed without password. | PASSED |
| C084 | test_cli_repeats_at_chosen_interval_and_stops_on_interrupt | args=[], interval=60 | SCHEDULER: Two cycles/sleeps at60or10seconds, then stop cleanly on interrupt; no real waiting. | PASSED |
| C085 | test_cli_repeats_at_chosen_interval_and_stops_on_interrupt | args=['--interval', '10'], interval=10 | SCHEDULER: Two cycles/sleeps at60or10seconds, then stop cleanly on interrupt; no real waiting. | PASSED |
| C086 | test_cli_rejects_bad_interval_before_password_or_work | interval='0' | SCHEDULER: 0/9/nonnumeric rejected by argument parser with exit2 before prompt/work. | PASSED |
| C087 | test_cli_rejects_bad_interval_before_password_or_work | interval='9' | SCHEDULER: 0/9/nonnumeric rejected by argument parser with exit2 before prompt/work. | PASSED |
| C088 | test_cli_rejects_bad_interval_before_password_or_work | interval='abc' | SCHEDULER: 0/9/nonnumeric rejected by argument parser with exit2 before prompt/work. | PASSED |
| C089 | test_cli_error_hides_credentials_and_stops | failure='connection' | SCHEDULER-ERROR: Database/identity error ends process with safe message, no secret, no retry/sleep. | PASSED |
| C090 | test_cli_error_hides_credentials_and_stops | failure='identity' | SCHEDULER-ERROR: Database/identity error ends process with safe message, no secret, no retry/sleep. | PASSED |

## Deliberate defects: do tests really fail for bad behavior?

Each experiment changed one source expression in a temporary copy under /tmp. Already-failing type cases were excluded: a pre-existing failure cannot falsely count as detection of a new defect. The unmodified selected set passes; mutants must produce new assertion failures, not collection errors. No repository application code or database was modified.

| Temporary defect | New failing cases | Detected |
|---|---:|---|
| emoji-weight-one | 15 | Yes |
| codepoint-instead-of-grapheme | 12 | Yes |
| title-bound-relaxed | 5 | Yes |
| title-bound-too-strict | 3 | Yes |
| body-bound-relaxed | 3 | Yes |
| body-bound-too-strict | 3 | Yes |
| body-stripped | 9 | Yes |
| real-title-stripped | 2 | Yes |
| email-lowercased | 1 | Yes |
| blank-title-stored-empty | 8 | Yes |
| draft-delete-protection-removed | 4 | Yes |
| nul-check-removed | 5 | Yes |
| target-check-skipped | 5 | Yes |
| identity-or-changed-to-and | 2 | Yes |
| target-port-original-db | 2 | Yes |
| batch1001-allowed | 1 | Yes |
| lock-timeout-removed | 2 | Yes |
| wrong-expiry-function | 4 | Yes |
| once-flag-ignored | 1 | Yes |
| custom-interval-ignored | 1 | Yes |
| cli-error-secret-leaked | 2 | Yes |

All21deliberate faults were detected. This includes both relaxed and overly strict bounds, lost whitespace, lost draft protection, wrong cluster/port logic, omitted timeout, wrong cleanup function, ignored one-cycle mode, ignored interval and leaked error credentials. That supports these assertions' usefulness; it does not guarantee discovery of every possible defect.

## Remaining limits and next action

SQL integration is still blocked by absent PL/Python and absent tables. Direct SQL limits, uniqueness, foreign keys, timestamps, trash/restore boundaries, concurrent locks, role restrictions, committed reconnect, actual rollback and undo/reapplication remain PENDING. These unit results cannot substitute for the [database verification matrix](users-notes-database-verification.md). Scheduler tests prove CLI sequencing with simulated work, not continuous real database operation or production deployment.

No claim is made that every input type, corrupted database response, Unicode version upgrade, memory-exhaustion scenario or concurrent schedule is covered. Those require their own concrete contracts and evidence; do not create passing filler tests.

Exact next action: fix integer-only batch validation and strict Boolean draft validation, preserving the existing text/limit/lifecycle rules; decide a consistent validation error for invalid batch types. Rerun the focused failing cases and then this entire suite. No application fixes were made during this review. Keep the39minute verification/360minute day caps; actual time remains unknown and unfinished work displaces later feature time.

📚 Learn first: [Current test file](../../tests/test_note_rules_and_maintenance.py), [input helper](../../app/note_rules.py), [maintenance worker](../../app/notes_maintenance.py).
↩ Return: explain the failing type cases before editing the two guards. Missing database tests are not passes.
