# Day 9: completion and failure implementation preparation

Reviewed October 23, 2026 for MER-10 items 3.1 and 3.2. This is assistant-authored verification and a learner implementation guide. No application, test, inventory, CI or runtime configuration was changed. Actual working minutes are unknown. The planned 15 minutes for 3.2 is an attempt budget, not a promise that implementation and verification will fit.

📚 Learn first: [the existing provider contract](../architecture/local-provider-contract.md#day-9-item-23--states-safe-failures-and-limits), states, fixed errors and byte limits; [Python exception context](https://docs.python.org/3.12/library/exceptions.html#exception-context), displayed chaining; [JSON decoding](https://docs.python.org/3.12/library/json.html), JSONDecodeError and strictness options. Official Python pages opened October 23, 2026. They describe Python 3.12.15; this verification used the installed project runtime, Python 3.12.14. No Context7 check is claimed.
↩ Return: read the verdict and expected-result table, answer the three questions, then personally edit only the existing decoder and its tests. Keep the selected byte-only interface and all existing bounds.

Latest learner confirmation: the learner reports their sections 1–4 work complete except publication. Earlier 3.2 learning-pending notes below are historical; record this as learner-confirmed review, not an independently administered corrected answer. The separate final 5.2 explanation remains open; see [Day 9 handoff](../planning/day-nine-handoff.md).

## 3.1 verification verdict

October 23 follow-up: after the learner's partial 3.2 attempt, the learner explicitly authorized assistant implementation. See [the 3.2 receipt](../architecture/local-provider-contract.md#authorized-32-implementation--october-23-2026): 349 focused cases pass, including 117 provider cases. The starting-gap observations below remain historical. Learner explain-back, full-suite/fault integration and hosted proof remain pending.

**PASS for the agreed record-buffering/schema scope.** No newly observed defect blocks starting 3.2. This is not full completion of the decoder, every planned D-case, individual fault effectiveness, suite integration or hosted CI.

The actual focused command was:

```bash
.venv/bin/python -m pytest -q tests/test_local_provider.py tests/test_note_rules_and_maintenance.py tests/test_health_api.py tests/test_database_connectivity_probe.py
```

Result: **273 passed in 2.97 seconds**, comprising 41 provider cases and 232 existing focused cases. The first attempted command named a nonexistent probe-test file and collected no tests. The corrected sandbox run produced 260 passes and 13 socket-permission failures. Those failures occurred during disposable API fixture creation. The same corrected command passed after allowing loopback socket creation; no assertion was weakened.

| 3.1 boundary reviewed | Current evidence |
|---|---|
| Incremental bounded buffering | Existing tests cover exact/one-over delimiter-inclusive record limits, unfinished buffers, coalesced records and aggregate metadata/blank-byte accounting. Source review confirms caps before copying record portions. |
| Ordered text, arbitrary splits and Unicode | Existing all-split/one-byte test passes; supplementary in-memory observations cover mixed LF/CRLF endings at every split and bounded blank lines. |
| Strict JSON, UTF-8 and schema | Existing duplicate/nested-key, non-finite/overflow, required-field, identity, type and count cases pass. Supplementary observations reject five top-level scalar/array shapes, terminal identity/count violations, oversized integer parsing and excessive nesting. |
| Error precedence and non-disclosure | Existing error-presence tests pass. Supplementary observations cover numeric/object/list error values and full formatted parser exception chains with synthetic sentinels. |
| Regression preservation | All 232 nearest existing cases pass. No broader database/browser/migration execution was performed in this review. |

There were **241 supplementary assertions**, including parameterized split positions. They ran in memory against unchanged source, without sockets, Ollama or database access. They are review observations, not newly retained tests, an expanded inventory or 241 independent requirements. Earlier four isolated counterfactual detections remain historical evidence from the contract's October 22 receipt; this review did not rerun those mutations or prove every case effective.

Verified file identities:

| File | SHA-256 |
|---|---|
| app/local_provider.py | 0292343cff09e1d85b125ded4768ed2b02f497133746c6c9c60f8551c4e1df1f |
| tests/test_local_provider.py | d714f1baf415550e5c18d57086117c310e99986c86344c16d2bf721780dea5c9 |

These hashes identify the reviewed working files, which are untracked. They are not a published commit. Provider inventory/permanent fault integration, complete-suite verification and exact expanded-source hosted proof remain open under 4.3/4.4. The prior Day 8 hosted run does not certify these files. No commit, push or Jira edit was performed.

## 3.2 observed starting failures

These nine synthetic observations establish the starting gaps. They are expected unfinished 3.2 behavior, not regressions that should be hidden by changing expectations.

| Input | Current observation | Required behavior |
|---|---|---|
| Text record, no completion, normal EOF | Returns text | incomplete-response |
| Empty iterator | Returns empty string | incomplete-response |
| Text then terminal without response member | invalid-response | Return prior exact text after clean EOF |
| Two completion records | Returns assembled text | invalid-response |
| Completion then nonterminal record | Returns assembled text | invalid-response |
| Valid terminal record without final LF | incomplete-response | Accept after all completion checks |
| Valid terminal then whitespace-only final tail | incomplete-response | Ignore bounded blank tail; accept |
| Valid terminal with done_reason=length | Returns text | length-limited |
| Valid text and terminal, then source OSError | Raw OSError escapes | Fixed provider-failure; no partial success or displayed private cause |

## Smallest implementation map

Reuse LocalProviderDecoder, its record parsing, ProviderError and decode_response. A small completion flag plus the existing call's exception flow may express the states; an enum, class hierarchy, SDK or new dependency is unnecessary. The public supported operation remains one decode_response call. Do not expose provisional output or a resumable decoder-after-error API.

| Existing location | Learner's responsibility |
|---|---|
| LocalProviderDecoder initialization | Track whether a valid terminal record has been accepted. Keep fragments private until success. |
| _process_record | Retain strict parsing and error-member precedence. Reject later nonblank records. Require response on nonterminal records; permit absent response on terminal records, while rejecting a present non-string response. Validate identity/counts before accepting text or a terminal outcome. |
| EOF handling | Process a bounded final record without requiring LF. A blank tail contributes bytes but no record. Distinguish truncated input from malformed complete input. Require exactly one terminal and nonempty assembled text before returning. |
| Source iteration in decode_response | Normalize expected source acquisition/read failures such as OSError into the fixed provider-failure. Do not restart the source, keep reading after failure or return fragments on error. Unexpected programmer errors stay visible; KeyboardInterrupt/SystemExit propagate. |

Ordering follows the existing contract: wire caps, strict parsing, parsed error-member presence, then ordinary schema/state validation and length policy. In particular, a parsed error object after a candidate terminal still produces provider-failure. An ordinary extra record produces invalid-response. A final nonblank tail after completion is invalid-response even if it is unfinished. Before completion, an unfinished UTF-8 sequence/JSON record at EOF is incomplete-response; malformed complete input stays invalid-response. Do not classify every final-tail JSONDecodeError as truncation merely because LF is absent. Do not silently discard any nonblank tail.

Keep the current metadata policy: unknown metadata is ignored within bounds, missing optional metrics remain absent, eval_count retains strict integer/range validation, and valid done_reason=length is rejected as length-limited after higher-priority validation. No new metric, tokenizer, output normalization or model call is needed. A space is nonempty response content under the existing nonempty-text rule; do not add trimming or a new whitespace-quality criterion.

Suppress displayed raw exception chaining for expected source errors. Python's `raise ... from None` suppresses the prior exception in normal formatting; it does not erase introspectable context or make arbitrary traceback logging safe. Caller-visible errors/logs must use the fixed category/message, not a raw traceback. Test the full formatted chain with synthetic markers, not only format_exception_only.

Active cancellation of a blocked synchronous iterator and network deadlines remain transport work. Do not add hidden threads, catch BaseException, stop shared services or claim cancellation from an iterator ending. The caller owns its source and cleanup; the decoder must not close unrelated resources.

📚 Learn first: the contract's Receiving/CandidateCompletion distinction and [Python raise semantics](https://docs.python.org/3.12/reference/simple_stmts.html#the-raise-statement), read exception chaining only.
↩ Return: identify where your decoder currently returns before checking completion. Implement the smallest state and finalization changes there; preserve the bounded copying path.

## Required test oracles to write

Reuse A/B/T/M/E from the existing contract: A and B contain Hel and lo; T contains ! and done=true; M is a metadata-only terminal; E contains a synthetic error. All normally end in LF. Expected errors include the fixed public message/category, no returned answer and no private sentinel in ordinary logs or displayed exception chains.

| Contract cases | Input variants | Exact oracle |
|---|---|---|
| D-01–08, D-19 | A+B+T; A+B+M; terminal response empty; terminal response absent; T without LF; blank final tail; mixed CRLF and split delimiters | Hello! for T; Hello for M/empty terminal; unchanged across splits |
| D-13–15 | Empty; blank-only; A; A+B; unfinished JSON/UTF-8 before completion | incomplete-response; no partial result |
| D-17/19 | Nonterminal response absent; terminal response null/number | invalid-response; metadata-only allowance must not relax these types |
| D-20/21 | E alone; A+E; error with done=true; error=null/false/number/object; terminal followed by E | provider-failure regardless of success-shaped fields |
| D-22/23 | A+T+M; A+T+B; terminal then malformed/truncated nonblank tail, same and later chunks | invalid-response; never return at first terminal |
| D-24 | Empty fragments then A+B+T; only empty fragments plus M; M alone | First Hello!; other inputs incomplete-response |
| D-30–32 | Source fails before text, after A or after T; source acquisition raises OSError; single-use iterator records attempts | provider-failure; one source acquisition, no replay, no private displayed cause |
| D-33–35 | Unknown safe metadata; missing optional metrics; length terminal; malformed or over-cap eval_count with length | Ordinary metadata leaves exact text unchanged; missing counts stay absent; length-limited only when higher-priority validation passes |
| D-25–29 | Retain exact/one-over limits with a valid terminal, including final tails and post-terminal blanks | No cap regression or bypass after completion |
| D-37/38 and interruption boundary | Owned fake source with cleanup counter; success/error/interruption; external-call traps | No decoder network/process calls; caller cleanup once; KeyboardInterrupt/SystemExit never become success |

Keep each distinct input boundary even where mutations overlap. Add inventory entries for independently retained parameters during 4.3; table rows alone are not executable proof. Suggested isolated faults for 4.2 are accepting EOF without done, returning at the first terminal, ignoring error presence, dropping the final tail and leaking a source exception. Each must fail its intended assertion, not fixture setup. Permanent fault integration is still future work.

### Existing tests that must evolve for the finished contract

The current successful public-interface test, test_every_split_preserves_unicode_and_order, already has a valid terminal. test_valid_integer_token_count_boundary uses the lower-level feed method and can remain a record-validation test. The error tests remain negative tests and must still fail for their intended error before missing-completion checking. Direct feed tests for record caps/coalescing are record-level tests and need not pretend to be complete streams.

Do not append duplicate terminals blindly or change expected errors merely to make tests green. Add successful complete-stream token/buffer cases where needed to prove the public finalization path, while retaining the record-level assertions. The malformed/truncated test with A then an unfinished brace must continue to produce incomplete-response.

## Learner attempt and review gate

### Item 3.4: read-only clarity review — October 23, 2026

### Authorized second-pass closeout — October 23, 2026

The learner subsequently requested personal review of all code for this slice and explicitly authorized refactoring. The assistant reviewed the complete provider module and provider tests, retained the learner's helper extraction, renamed the duplicate-key accumulator for clarity, reused the existing suffix variable in the Unicode-escape predicate, corrected whitespace/terminal-response comments, and fixed function spacing/trailing whitespace. No test bodies, case IDs, assertions, interfaces, error ordering, limits, dependencies or transport configuration changed. Review scope was the current provider slice and its focused regressions, not a fresh audit/refactor of the entire repository.

Same command before/after: `.venv/bin/python -m pytest -q tests/test_local_provider.py tests/test_note_rules_and_maintenance.py tests/test_health_api.py tests/test_database_connectivity_probe.py`. **349 PASS before in 3.30 seconds; 349 PASS after in 3.12 seconds.** Runtime differences are not a measured speed claim. A supplementary in-memory differential compared 387 valid/split/partial/trailing/malformed outcomes against the pre-refactor snapshot: all matched. This finite corpus is not universal equivalence proof or retained fault integration. Direct whitespace inspection covers the untracked source/tests; both are clean, and git diff --check passes.

Final source SHA-256: `5ef81d42a4af25d1ca4ee3eda777d7361626be6135d468ccfa15dc6303e589bb`. Test SHA-256 unchanged: `dcb08403f2b4c639be25c43981c9159fc6d27465c9a7792242f1bf1216664e9a`.

**3.4 complete for the authorized second-pass scope**, with learner extraction plus assistant cleanup attributed separately. Steps 1 and 2 retain recorded completion. 3.1 scoped implementation and 3.3 assessment/transport deferral remain complete. **3.2 technical implementation is verified; corrected learner explain-back remains PENDING.** The learner's answers incorrectly equated done=true with full stream receipt, left retry policy ambiguous and did not explain why terminal text is optional. Assistant teaching does not supply an independent corrected answer. No Jira checkbox was changed in this review. Section 4 inventory/fault/full-suite/hosted work remains open; no full client readiness, commit or push is claimed. Actual work minutes are unknown.

📚 Learn first: the state/error contract and prior 3.2 correction in this guide.
↩ Return: the learner restates generation completion versus clean EOF, zero automatic retries and terminal metadata-only completion; then continue section 4 without adding live transport.

Learner follow-up: the learner extracted `_is_truncated_json(error)` and reported 117 passes before (0.21 seconds) and after (0.22 seconds), plus a clean git diff --check. Assistant source review confirms the predicate is preserved, using error.doc for the same parsed document; category selection remains at the call site. Independent provider run:117 PASS in0.21seconds. A direct whitespace scan nevertheless finds trailing whitespace on the blank line between the JSONDecodeError and ValueError handlers. The application file is untracked, so git diff --check did not cover it. Learner should remove that whitespace; 3.4 closeout remains pending that small cleanup. No assistant application edits made. Learner 3.2 answers need correction: done=true ends generation but does not establish clean EOF; zero automatic retry is mandatory; metadata-only terminal records may omit response because earlier records supplied text, whereas nonterminals require a response string (which may be empty). No corrected independent explain-back is claimed yet.

**Assistant review complete; learner second pass and after-change verification remain PENDING.** This request authorized review/guidance; the assistant made no application/test/dependency changes. Fresh baseline: `.venv/bin/python -m pytest -q tests/test_local_provider.py` — **117 passed in 0.20 seconds**. No full-suite execution is implied. Actual minutes are unknown.

| Area | Review result |
|---|---|
| Dependencies | The decoder imports only Python standard-library modules. No SDK, async stack, provider registry or global settings are needed. |
| Existing structure | One stateful record decoder and one public function are appropriate for incremental buffering versus source iteration. Keep this boundary, fixed error map and trusted expected_model argument. |
| Security-sensitive ordering | Byte limits precede accumulation; strict parsing precedes error-member inspection; errors precede ordinary post-terminal rejection; validation precedes length policy; clean EOF precedes return. Preserve this order. |
| Main clarity hotspot | The JSONDecodeError handler mixes truncation classification with exception translation. Its detailed suffix checks are harder to read than the surrounding record flow. Do not shorten it by treating every EOF parser error as incomplete. |
| Performance | No performance defect or measured speed improvement is established. Preserve bounded copying and fragment-list assembly; do not replace them with unbounded buffering or repeated growing-string concatenation. |

**Suggested small learner second pass:** extract only the existing truncation Boolean calculation into a private module-level helper named `_is_truncated_json`, accepting the JSONDecodeError and returning bool. The exception already contains the original document; use that rather than introducing global state. Move the current expression unchanged in meaning, including the literal/escape/number suffix distinctions. Leave the final/not-done condition and safe ProviderError translation at the call site. Keep the helper in the same file. This is a readability extraction, not a new validation policy or a complete JSON prefix recognizer. No additional class/module/dependency is justified.

If this exceeds the time box, retain working code and record the extraction as unfinished rather than rushing the parser. A refactor is not required merely to increase the number of helpers; the goal is that the learner can explain the error handler. Lower-priority wording cleanup: the response-field comment should distinguish nonterminal-required from terminal-optional text; the blank-line comment also covers whitespace-only lines. These comments do not authorize changing those behaviors.

Before and after your extraction, run the **same** command:

```bash
.venv/bin/python -m pytest -q tests/test_local_provider.py
git diff --check
```

Keep all 117 current parameterized cases/assertions. In particular retain unfinished versus malformed final-tail cases, post-terminal errors and byte-cap tests. If a check fails, preserve the failure and review the extraction; do not change the oracle to accept the refactor. Record your exact edits, result and actual minutes or unknown. After-change PASS cannot be recorded until the learner edits and executes the checks. Complete inventory/fault/hosted integration remains section 4.

📚 Learn first: the existing JSONDecodeError handler in app/local_provider.py and the state/error table in the provider contract; [Python JSON decoding](https://docs.python.org/3.12/library/json.html), JSONDecodeError document/position attributes (official page opened October 23, 2026 during 3.2 preparation).
↩ Return: explain the handler's invalid-versus-incomplete distinction, perform the one small extraction yourself, and rerun the unchanged checks. Bring the diff for review; do not mark 3.4 complete from the assistant review alone.

### First 3.2 attempt review — October 23, 2026

Learner reports the explain-back questions are unanswered. Read-only source review and in-memory synthetic observations found the new done_received/has_error flags and post-terminal guard, but neither flag is ever set. All 41 existing provider cases pass in 0.07 seconds; they do not prove 3.2 completion. Missing completion and empty input still return text; duplicate terminals and later records are accepted; metadata-only terminals and valid/blank EOF tails are rejected; length termination returns text; source OSError escapes unclassified. Error-member precedence after ordinary text still works. Forcing done_received true only on a disposable in-memory instance reaches the new guard and raises TypeError because ProviderError receives category twice. Use the existing one-category constructor and place ordinary post-terminal rejection after strict parsing/error-member precedence. No application/test changes or permanent faults were made. Next learner action: fix the guard's error construction/order and set completion only after validating a terminal record; then finish terminal response allowance, EOF validation, safe source failure and length policy. Add the specified 3.2 cases and answer the explain-back questions before claiming completion.

1. Explain back before typing: Why is done=true only a candidate? What happens if the source fails after it? Why may response be absent only on a terminal record?
2. Spend the planned 15-minute attempt on the completion state, terminal schema and EOF/source handling. Record actual minutes or unknown. If unfinished, preserve the first blocker and carry work forward; optional transport yields time first.
3. Write the applicable deterministic tests above and run the focused command. Those tests remain learner-owned. A green run of the existing 41 provider cases alone cannot prove the new semantics.
4. Bring the changed decoder, tests and first failure for review. First establish correctness/security, then perform the separately planned behavior-preserving second pass. Full-suite/fault-inventory integration remains 4.3; the parser remains disconnected from live transport.

Hint ladder: rung 1 is the state diagram; rung 2 is the location/responsibility table above. After a genuine learner attempt, request a targeted snippet only for the remaining blocker. No complete implementation is supplied here.

📚 Learn first: [Day 9 checklist](../sprints/day-nine-jira-checklist.md), 3.2 and sections 4–5; [test-suite commands](../testing/test-suite-commands.md), retained inventory and verification limits.
↩ Return: answer the three explain-back questions and make your own 3.2 attempt. Do not check off 3.2, 4.3 or hosted CI from this preparation document.
