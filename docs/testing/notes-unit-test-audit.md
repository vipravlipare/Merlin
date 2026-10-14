# Manual review of the notes/maintenance tests

Latest evidence: [deep review of each current case](notes-unit-test-deep-audit.md),82PASS/8FAIL; this file retains the original-case audit history.

Reviewed October 10, 2026. This is a case-by-case review of the original 74 collected cases against the current helper code, worker code and [written rules](../architecture/users-notes-design.md). Case numbers below identify the original collection order, not permanent pytest IDs. They include each parametrized input, not just each function.

For every case, I checked the rule, actual function call, expected answer, assertion, unrelated ways it could pass, and whether another case already supplied the same evidence. Test quantity was not the acceptance condition.

## Findings and changes

The original suite contained useful tests, but its count overstated distinct coverage. Aggregate blank/email checks repeated later cases; separate target-helper checks were weaker than exercising the full worker. Integer10 repeated integer1 rejection. A list repeated the same non-string branch without adding meaningful evidence. These were consolidated. Interior NUL rejection and absent-email behavior were retained in the consolidated groups.

Wrong-target tests now exercise run_once for both wrong database and preserved cluster. They check that the identity query is the only SQL call. Valid fingerprints are literal observed values rather than derived from the worker's own EXPECTED_CLUSTER constant: a wrong constant must not make the test silently pass.

Worker assertions now check the exact expiry/purge function names, order, bound batch values, pre-cleanup timeouts and error-free transaction-context exit. Previously, matching only the last two argument tuples could pass even when the wrong function was called. This is control-flow evidence, not actual database transaction evidence.

Expected rejection messages are now specific. No acceptance case computes its expected answer by calling the function under test. Added useful missing cases: blank title with real body, and combining-character text accepted at each exact limit. The latter catches a validator that wrongly uses code-point length even when the counting helper itself is correct.

Two additional cases expose a real worker input gap: booleans and fractions must not be forwarded as an SQL INTEGER batch argument. The worker currently checks only the numeric range. True and1.5 therefore reach the connector. Tests intentionally make any such connection attempt fail, before touching a database. These failures are not marked xfail or hidden. No application code was changed during this review.

## Original cases: individual verdicts

| Original case | Exact input/check | Rule and independently expected answer | Review decision |
|---|---|---|---|
| 01 | abc plus space/exclamation | Ordinary letters/space/punctuation count1 each; total5 | Keep; valid arithmetic oracle. |
| 02 | One smiling emoji | Emoji weighs4 | Keep; catches weight1. |
| 03 | Family ZWJ sequence | One displayed emoji weighs4 | Keep; catches component/byte counting. |
| 04 | Thumb with skin tone | Complete emoji sequence weighs4 | Keep; distinct sequence form. |
| 05 | US flag | Paired regional indicators form one emoji;4 | Keep. |
| 06 | Keycap1 | Full keycap sequence weighs4 | Keep. |
| 07 | e plus combining accent | One non-emoji grapheme weighs1 | Keep; catches code-point counting. |
| 08 | Newline | One non-emoji grapheme weighs1 | Keep; whitespace cannot be a free unlimited input channel. |
| 09 |43family emoji +3letters, then +4letters |175 accepted unchanged;176 rejected | Keep; sharpened message matching. Both checks reach validate_note. |
| 10 |1750smiling emoji, then1751 |7000 accepted unchanged;7004 rejected | Keep; validates public helper, not only counting. |
| 11 | Combined blank-save/draft/body/title checks | Blank saved requests deletion; draft stays; actual body survives; title-only stays | Consolidate; all covered more precisely in39–49. |
| 12 | Combined trimmed/blank/absent email checks | Preserve casing; empty/absent becomesNone | Consolidate into61–64 plus explicit None case. No uniqueness claim. |
| 13 | hello followed by NUL | Reject PostgreSQL-incompatible text | Move into consolidated invalid-text group; interior NUL is worth retaining. |
| 14 | Counting integer10 | Reject non-string | Remove duplicate;51already exercises integer rejection; field-specific tests still check forwarding. |
| 15 | Wrong database but valid cluster | Refuse maintenance | Replace helper-only case with stronger full-worker wrong-database case. |
| 16 | Correct database but preserved cluster | Refuse maintenance | Merge into full-worker wrong-cluster check. |
| 17 | Preserved cluster through run_once | Only fingerprint query; no cleanup | Keep and parameterize with wrong database; require refusal message. |
| 18 | Valid target, batch25, mocked counts2/3 | Return respective counts; call intended functions safely/in order | Keep; strengthen exact names/order/context exit. Does not prove actual changed rows. |
| 19 | Empty string | Weight0 | Keep; tests empty text independently of None. |
| 20 | Three special characters | Weight3 | Keep; confirms non-emoji punctuation. |
| 21 | Two Chinese characters | Weight2 | Keep; non-ASCII text must not become bytes or emojis. |
| 22 | Tab followed by CRLF | Tab1 plus CRLF grapheme1 =2 | Keep; correct under current grapheme rule, not byte/code-point rule. |
| 23 | a, emoji, b |1+4+1=6 | Keep; mixed content cannot use one uniform weight. |
| 24 | Family plus smile |4+4=8 | Keep; each sequence counted independently. |
| 25 | Copyright with emoji selector | Recognized sequence weighs4 | Keep; presentation-selector edge. |
| 26 | Skin-tone emoji plus punctuation |4+1=5 | Keep; mixed sequence edge. |
| 27 |174ordinary title characters | Accepted exactly as supplied | Keep; lower neighbor. |
| 28 |175ordinary title characters | Accepted exactly as supplied | Keep; catches >=instead of> defect. |
| 29 |176ordinary title characters | Title-specific ValueError | Keep; catches relaxed bound. |
| 30 |6999ordinary body characters | Accepted unchanged | Keep; lower neighbor. |
| 31 |7000ordinary body characters | Accepted unchanged | Keep; catches >=defect. |
| 32 |7001ordinary body characters | Body-specific ValueError | Keep; catches relaxed bound. |
| 33 | Draft title44smiles | Weighted176 rejected | Keep; draft does not bypass limits. |
| 34 | Draft title43smiles +4letters | Weighted176 rejected | Keep; mixed draft limit; sharpened message. |
| 35 | Draft title176accented graphemes | Weighted176 rejected | Keep, but alone cannot prove proper grapheme use; added accepted175case. |
| 36 | Draft body1751family sequences | Weighted7004 rejected | Keep; complete-sequence draft bound. |
| 37 | Draft body1750smiles +letter | Weighted7001 rejected | Keep; first weighted excess. |
| 38 | Draft body7001spaces | Rejected before blank decision | Keep; blank body is not an unlimited storage exemption. |
| 39 | Saved note: title/bodyNone | TitleNone, bodyempty, deletion requested | Keep; absent input normalization. |
| 40 | Saved note: two empty strings | Same stored result/deletion decision | Keep; distinguishes missing from explicit empty input. |
| 41 | Saved whitespace title/body | TitleNone; original body whitespace; deletion requested | Keep; whitespace classification and preservation. |
| 42 | Saved non-breaking-space title/body | Recognized blank; body preserved; deletion requested | Keep as Python whitespace behavior; does not prove SQL whitespace parity. |
| 43 | Draft title/bodyNone | Normalize input; no deletion | Keep; draft differs from saved input. |
| 44 | Draft empty strings | No deletion | Keep; explicit draft empty form. |
| 45 | Draft whitespace title/body | Normalize title, preserve body, no deletion | Keep; drafting must not discard blank text. |
| 46 | Draft non-breaking-space title/body | No deletion | Keep; Python edge only. |
| 47 | Real title, empty body | Exactly preserved; no immediate deletion | Keep; does not prove24hour SQL lifecycle. |
| 48 | Absent title, real body | Exactly preserved; no deletion | Keep; body-only note. |
| 49 | Padded emoji title, actual body with spaces/newlines | Both unchanged; no deletion | Keep; catches stripping real content. |
| 50 | CountingNone | Reject: counting requires a string | Keep; note normalization handlesNone separately. |
| 51 | Counting integer1 | Reject wrong text type | Keep; precise error message. |
| 52 | Counting bytes | Reject bytes rather than silently decoding | Keep; different caller mistake. |
| 53 | Counting list | Same non-string branch as51/52 | Remove duplicate; not distinct product evidence. |
| 54 | Counting NUL | Reject PostgreSQL-incompatible character | Keep; consolidated group also retains interior NUL13. |
| 55 | Title integer10 | Reject through public validator | Keep; helper rejection alone does not prove title path calls it. |
| 56 | Body integer10 | Reject through public validator | Keep; independent body path. |
| 57 | Title bytes | Reject through title path | Keep. |
| 58 | Body bytes | Reject through body path | Keep. |
| 59 | Title NUL | Reject through title path | Keep; PostgreSQL compatibility. |
| 60 | Body NUL | Reject through body path | Keep; separate field. |
| 61 | Empty email | None | Keep. |
| 62 | Tabs/newline-only email | None | Keep; cannot store a blank identifier. |
| 63 | Padded mixed-case email | Trim edges; preserve casing | Keep and include tabs/newline edges; no ownership/format/uniqueness claim. |
| 64 | Non-breaking-space-padded email | Trim edges; retain address | Keep as Python behavior; SQL whitespace consistency still unproved. |
| 65 | Integer email | Reject wrong text type | Keep; normalize_email must not silently stringify. |
| 66 | Bytes email | Reject wrong text type | Keep. |
| 67 | Email with interior NUL | Reject PostgreSQL-incompatible text | Keep. |
| 68 | Batch-1 | ValueError before connection | Keep; lower invalid value. |
| 69 | Batch0 | ValueError before connection | Keep; exact invalid boundary. |
| 70 | Batch1001 | ValueError before connection | Keep; first invalid upper value. |
| 71 | Batch1 and mocked no work | Fixed disposable endpoint; two bounded calls; counts0/0 | Keep; strengthen exact queries and timeouts. SQL batching is not proved. |
| 72 | Batch1000 and mocked no work | Same protections at maximum batch | Keep; tests accepted upper boundary. |
| 73 | Expiry operation raises simulated database error | Error escapes transaction context; purge never called | Keep; Python error propagation only, not database rollback. |
| 74 | Purge raises after expiry | Error escapes transaction context | Keep; checks failure after first operation. Actual rollback remains unproved. |

## Additional checks justified by the review

| New check | Missing evidence it supplies | Result |
|---|---|---|
| Blank title plus real body: empty and whitespace title | Normalizing title cannot erase a valid body or request deletion | PASS |
| Accented title175/body7000 | Valid displayed-character limits accepted despite larger code-point counts | PASS |
| BatchTrue | SQL INTEGER contract rejects booleans before connection | FAIL; connector reached |
| Batch1.5 | SQL INTEGER contract rejects fractions before connection | FAIL; connector reached |

The revised collection happens to contain76cases:74PASS and2FAIL. This count is a runner result, not a claim of76rules or complete coverage. Failures were left visible; no application fix was authorized or performed as part of this test review.

## Do the assertions detect broken behavior?

After reviewing the assertions, I tried seven deliberate defects in temporary copies under /tmp. The repository application files were not edited; the tests made no real database connections. A defect counted as detected only when pytest failed assertions, not when collection crashed.

| Temporary defect | Failing cases detecting it |
|---|---:|
| Emoji weight changed from4to1 |15|
| Title176 wrongly allowed |5|
| Body7001 wrongly allowed |3|
| Body whitespace stripped |9|
| Email display casing lowercased |1|
| Target identity verification skipped |5|
| Purge called instead of expiry |4|

All seven were detected. This checks meaningful failure sensitivity for these faults; it does not prove that every possible defect is detectable.

## What these tests still cannot prove

No executable SQL integration test exists in this file. UUID generation/immutability, username/email uniqueness, foreign keys, SQL weighted CHECKs, timestamps, trash/restore14day boundary, expiry24hour transitions, database row locks, view filtering, roles/grants, RLS, actual batching, reconnect, rollback and down/reapply remain PENDING. See the precise [database verification matrix](users-notes-database-verification.md). The last read-only server check found no available PL/Python and no Users/Notes tables. Do not reinterpret mocked counts or a raised Python error as proof of these rules.

Scheduler main() behavior (repeated timing, --once, Ctrl+C and sanitized terminal error output) also lacks direct executable tests; run_once tests cannot prove the CLI loop. That gap is recorded rather than filled with passing placeholders. Tests do not currently validate every possible input type, resource exhaustion or new emoji outside the pinned dataset. No new product behavior was invented to make the review look complete.

Exact next action: review/fix the worker's integer-only batch validation without changing the accepted1–1000range, then rerun the two failing tests and the full focused suite. This review itself did not change application code. Database verification remains blocked on PL/Python prerequisites. The39minute verification block and360minute day cap remain; actual minutes are unknown.

📚 Learn first: [Reviewed test file](../../tests/test_note_rules_and_maintenance.py), [helper](../../app/note_rules.py), [worker](../../app/notes_maintenance.py).
↩ Return: explain which two inputs reach the connector unexpectedly, then address that failure before claiming the suite passes.
