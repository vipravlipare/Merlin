# Strict testing policy and 150 defect scenarios

Reviewed October 10, 2026. This is a test specification, not new executable tests or a deployment guarantee. The learner writes code and tests under the current repository instructions. No application, SQL, configuration or test files were changed in this review.

## Current evidence

Read every function and parameter row in `tests/test_note_rules_and_maintenance.py` again against `app/note_rules.py` and `app/notes_maintenance.py`. The existing [individual 90-case ledger](notes-unit-test-deep-audit.md) identifies each input and result. Reran the unchanged suite:

```bash
.venv/bin/python -m pytest tests/test_note_rules_and_maintenance.py -q
```

Observed: **82 passed, 8 failed**. Five batch-type failures and three draft-type failures remain unfixed. Earlier evidence detected 21 deliberate mutations in temporary copies; this turn did not execute additional mutations. The 150 scenarios below are proposed faults to challenge, not 150 bugs found, tests executed, or mutations detected.

There is one executable test file. It tests input helpers and simulated maintenance behavior. The probe has no executable tests here. Migration behavior, real transactions, concurrency, role permissions and cleanup remain unproved. The last database inspection found missing PL/Python and absent users/notes tables. Do not infer real database behavior from MagicMock.

## Policy going forward

Each implemented rule needs a named contract, realistic input or transition, independently specified expected result, and the right proof layer. Include valid cases as well as rejection cases so an implementation that rejects everything cannot pass. Prefer meaningful boundaries and distinct risks over a numerical test target.

A failure regression must fail against the broken behavior, then pass against the corrected code with unchanged expectations. Record both results. Do not remove a failing assertion, widen accepted exceptions, add xfail, skip a required case, or calculate expected results using the implementation under test to create a green result.

For each input rule, consider absent values, wrong types, empty values, whitespace, normal values, below/at/above boundaries, Unicode and persistence. For lifecycle rules, test before/at/after deadlines, repeated operations, forbidden transitions and concurrent actors. Not every combination is necessary: explain what distinct fault each retained case detects.

Use exact outputs and exact exception classes where they form the contract. Verify refusal occurs before forbidden side effects. Check the complete ordered command list when extra writes are dangerous. Avoid brittle assertions on irrelevant private implementation details or whole error messages that users never depend on.

Mutation experiments change one behavior at a time in isolated copies. First establish a passing baseline for the selected tests. Existing failures cannot count as mutant detection. Report detected, survived, equivalent, invalid and timed-out mutations separately. A syntax error or import failure is not evidence that a rule assertion caught a behavioral defect. Investigate survivors rather than adding assertions that merely match source text.

Mocks prove Python decisions and calls. Real PostgreSQL tests prove constraints, commits, rollback, locks, grants and row policies. Real limited-role connections are required for authorization evidence. Administrative connections cannot establish ordinary-user denial. Deployment checks must match the actual deployed versions and configuration; unit counts are not a release gate by themselves.

Only synthetic disposable storage may be modified. Before database tests, verify project, network, host/port, volume and cluster against the preserved Sprint 0 target. Do not migrate, reset or delete `merlin_postgres_data` or cluster `7691749973399031842`.

No suite can establish that nothing will ever break. The policy is to make defined behaviors falsifiable, keep unresolved failures visible, and expand coverage when new behavior is implemented. Authentication, sharing, rate limiting and cloud deployment have no implemented boundary to verify here; do not invent passing tests for them.

## Second review: every test function

All parameter cases in each row were reread. Keep the existing individual case ledger as the detailed mapping; this table records the new assessment and specific improvements.

| Function | Assessment / precise improvement |
|---|---|
| test_display_character_weights | Independent counts cover plain text, emoji families, tones, flags, keycaps, accents and newline. Keep all distinct forms. |
| test_title_boundary_with_emoji_sequence | Correct mixed 175/176 boundary. Also assert body and deletion decision on accepted output so correct title alone cannot hide a corrupted result. |
| test_body_boundary | Correct emoji 7000/7004 boundary. Add a mixed 7001 saved-note case; current mixed rejection is draft-only. |
| test_wrong_target_never_calls_cleanup | Correct wrong database and preserved cluster. Replace fingerprint substring check with the exact sole identity query. Add both-wrong and failed/missing identity reads; no cleanup may follow. |
| test_worker_cycle_verifies_then_uses_bounded_functions | Correct bound calls, counts and clean context exit. Last-two-call comparison permits extra earlier SQL: assert the complete five-call sequence, exact connector settings and exactly three fetches. |
| test_more_display_sequences | Correct independent empty/control/CJK/mixed counts. CRLF is one grapheme here; retain the expected two for tab plus CRLF. Add other Unicode forms only with pinned independent expectations. |
| test_plain_title_limit | Good below/at/above boundaries. Assert complete accepted result, not title alone. |
| test_plain_body_limit | Good below/at/above boundaries. Assert complete accepted result, not body alone. |
| test_over_limit_title_rejected_even_for_drafts | Specific title error proves drafts cannot bypass limits. All three Unicode forms are useful. |
| test_over_limit_body_rejected_even_for_drafts | Specific body error covers emoji, mixed text and oversized whitespace. Keep all three. |
| test_empty_note_decision | Correct exact normalized title/body and Boolean decision across eight cases. Keep saved and draft paths. |
| test_nonblank_note_is_preserved | Good complete result tuple including whitespace preservation. Add valid draft content to challenge accidental draft deletion. |
| test_count_rejects_invalid_text | Specific type/NUL errors are useful. Add surrogate handling only after deciding the PostgreSQL-compatible text contract. |
| test_note_fields_reject_invalid_text | Correct public-path tests for both fields. Add Boolean/container inputs and interior NUL through both fields. |
| test_email_edge_whitespace | Good optional/blank/trim/display-case expectations. Add already-normalized input and idempotence with a literal expected address. No claim of syntax or ownership validation. |
| test_email_rejects_invalid_database_text | Useful type/NUL rejection. Add Boolean/container inputs and NUL at distinct positions if behavior changes. |
| test_invalid_batch_never_connects | Useful range errors and forbidden connection. Keep negative, zero and upper overflow. |
| test_allowed_batch_boundaries_and_fixed_target | Useful minimum/maximum, target and timeout assertions. Check user/connect_timeout too and full ordered SQL sequence rather than slices. |
| test_cleanup_failure_leaves_transaction_as_error | Useful expiry/purge failure propagation and stop-before-purge. Assert the same error object reaches exit, no later commands, and no successful return. Real rollback remains pending. |
| test_blank_title_with_real_body | Good complete output; prevents accidental deletion when title disappears. |
| test_combining_characters_accepted_at_display_limit | Good public acceptance of multi-code-point graphemes. Assert untouched companion field and false deletion flag. |
| test_noninteger_batch_rejected_before_connecting | Both cases fail correctly against the current missing guard. Keep ValueError plus no-connection requirements. |
| test_more_wrong_batch_types_rejected | All three cases expose missing guard/accidental TypeError. Keep deliberate ValueError contract. |
| test_draft_flag_requires_boolean | Three useful failing regressions. Could match a stable draft-field message after the learner defines it; do not accept TypeError or silent coercion. |
| test_cli_once_runs_one_cycle_without_sleep | Good bounded fixture, exact cycle arguments, no sleep and secret exclusion. Prefer exact success line over substring to catch duplicate/misleading output. |
| test_cli_repeats_at_chosen_interval_and_stops_on_interrupt | Good default/custom timing and bounded interrupt. Check exact cycle arguments every time and both result lines, not only stop message. |
| test_cli_rejects_bad_interval_before_password_or_work | Good exit2 and no prompt/work. Add negative interval, unknown flag, help and sleep-not-called. |
| test_cli_error_hides_credentials_and_stops | Good sanitized errors and no retry/sleep. Assert no success line after failure; test errors at connection/identity/cleanup separately through run_once. |

Additional decision needed: oversized whitespace-only titles are normalized to None before the title bound check, unlike oversized bodies. Do not invent an expected result: decide whether discarded blank input must obey the title limit. Python strip and PostgreSQL POSIX whitespace may also disagree for Unicode; compare them in real database tests.

## 150 realistic defect challenges

Each row describes a deliberate faulty behavior and the evidence that should distinguish it from correct behavior. These are **all proposed**, even where the current suite already covers a similar fault. U means Python unit proof; D means disposable PostgreSQL integration; C means concurrent database sessions; P means probe/runtime. D/C scenarios remain blocked until database prerequisites pass. Rows marked contract decision must not become passing tests without that decision.

### Text counting and compatibility

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F001 | Emoji counts as one | One smiley returns four | U |
| F002 | Plain character counts as four | Plain a returns one | U |
| F003 | Family counted by components | One family grapheme returns four | U |
| F004 | Skin tone counted separately | One toned emoji returns four | U |
| F005 | Flag counted by regional indicators | One complete flag returns four | U |
| F006 | Keycap split into parts | Complete keycap returns four | U |
| F007 | Combining accent counted separately | Decomposed accented letter returns one | U |
| F008 | Empty text given nonzero weight | Empty text returns zero | U |
| F009 | Spaces ignored in limits | Three spaces return three | U |
| F010 | Mixed text loses ordinary characters | a + smiley + b returns six | U |
| F011 | Newline stripped before counting | Single newline returns one | U |
| F012 | CRLF treated as two graphemes | Tab plus CRLF returns two | U |
| F013 | CJK counted as UTF-8 bytes | Two CJK graphemes return two | U |
| F014 | NUL accepted inside text | Interior NUL raises the text validation error | U |
| F015 | Server Unicode packages differ from helper | Same independent corpus returns identical Python/SQL counts; mismatched pins block migration | D |

### Title and body limits

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F016 | Title limit relaxed to 176 | Plain 176 rejects | U/D |
| F017 | Title limit tightened to 174 | Plain 175 accepts unchanged | U/D |
| F018 | Body limit relaxed to 7001 | Plain 7001 rejects | U/D |
| F019 | Body limit tightened to 6999 | Plain 7000 accepts unchanged | U/D |
| F020 | Title uses code-point count | 175 decomposed accented graphemes accept | U/D |
| F021 | Body uses code-point count | 7000 decomposed accented graphemes accept | U/D |
| F022 | Title counts emojis as one | 44 smileys reject as weighted 176 | U/D |
| F023 | Body counts emojis as one | 1751 smileys reject as weighted 7004 | U/D |
| F024 | Draft bypasses title limit | Weighted 176 draft title rejects | U/D |
| F025 | Draft bypasses body limit | Weighted 7001 draft body rejects | U/D |
| F026 | Title truncates silently | Accepted 175 unchanged; 176 rejects instead of shortening | U/D |
| F027 | Body truncates silently | Accepted 7000 unchanged; 7001 rejects instead of shortening | U/D |
| F028 | Limit applies only on insert | Updating an existing note above each limit rejects | D |
| F029 | Title and body errors swapped | Each invalid field produces its own expected rejection | U/D |
| F030 | Oversized blank title bypass is unintended | Decide discarded-blank-title contract, then test 175/176 spaces | U/D |

### Blank, type and normalization behavior

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F031 | Blank title retained as empty text | Empty title normalizes to None | U/D |
| F032 | Whitespace title retained | Spaces/tabs/lines normalize to None | U/D |
| F033 | Real title stripped | Padded real title remains exactly unchanged | U/D |
| F034 | Body stripped | Leading/trailing spaces and lines survive | U/D |
| F035 | None body remains None | Helper returns empty text | U |
| F036 | Fully blank saved note preserved | delete_on_save is exactly True | U |
| F037 | Fully blank draft marked for deletion | delete_on_save is exactly False | U |
| F038 | Title-only saved note deleted immediately | Helper preserves legitimate title | U |
| F039 | Body-only saved note deleted | Real body preserved without title | U |
| F040 | Whitespace body mistaken for content | Saved note without real title requests deletion | U/D |
| F041 | Text draft flag coerced to True | "false" raises ValueError | U |
| F042 | Integer draft flag accepted | 1 raises ValueError | U |
| F043 | None draft flag accepted | None raises ValueError | U |
| F044 | Text fields coerced from containers | List/dict/Boolean title/body rejected | U |
| F045 | Python and SQL disagree about blank Unicode | Same whitespace corpus normalizes/rejects consistently; resolve differences explicitly | U/D |

### Users and email integrity

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F046 | Email display casing lowercased | Mixed-case display address preserved | U |
| F047 | Email padding retained by helper | Edge whitespace trimmed | U |
| F048 | Empty email stored as empty text | Blank helper input becomes None | U |
| F049 | Optional email rejected | User with NULL email inserts | D |
| F050 | Multiple NULL emails treated as duplicates | Two distinct users without email insert | D |
| F051 | Lowercase email uniqueness removed | Case-variant duplicate rejects; original row unchanged | D |
| F052 | Same email allowed on update | Updating another account to duplicate rejects | D |
| F053 | Direct padded email bypasses helper | SQL CHECK rejects stored padded address | D |
| F054 | Direct blank email bypasses helper | SQL CHECK rejects blank address | D |
| F055 | Invalid email text coerced | Non-string/NUL helper input rejected | U |
| F056 | Required username nullable | NULL username rejects | D |
| F057 | Uppercase username accepted directly | Nonlowercase username rejects | D |
| F058 | Username boundary off by one | Valid 20 accepts; 21 rejects; empty rejects | D |
| F059 | Canonical username manually overridden | Generated canonical value cannot be independently supplied/updated | D |
| F060 | Concurrent duplicate registration succeeds twice | Two sessions yield one committed account, one uniqueness rejection | C |

### IDs, ownership and permissions

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F061 | Default ID missing | Insert without ID produces non-NULL UUIDv4 | D |
| F062 | Wrong UUID version accepted | Valid UUIDv7 input rejects under current v4 contract | D |
| F063 | Wrong UUID variant accepted | Nonstandard variant rejects | D |
| F064 | Duplicate primary key accepted | Second same-ID insert rejects | D |
| F065 | Missing owner accepted | NULL note owner rejects | D |
| F066 | Nonexistent owner accepted | Unknown UUID owner rejects | D |
| F067 | User deletion leaves orphan notes | Delete synthetic account; its notes disappear | D |
| F068 | Note owner mutable | Direct owner transfer rejects; original owner retained | D |
| F069 | User ID mutable | ID update rejects; dependent rows remain valid | D |
| F070 | Note ID mutable | ID update rejects | D |
| F071 | App can read another user's note | Limited app role with actor A cannot read B's row | D |
| F072 | App can edit another user's note | Limited app role update affects no B row | D |
| F073 | App can insert as another user | Actor A insert for B rejects | D |
| F074 | Missing actor exposes rows | App role without actor sees no protected rows | D |
| F075 | App bypasses roles or privileged functions | Inspect actual login membership; protected operations denied; actor source remains trusted-backend prerequisite | D |

### Server and device timestamps

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F076 | Device sets server creation clock | Forged insert clock overridden/rejected; server creation verified | D |
| F077 | Initial server edit differs from creation | New row created_at equals updated_at | D |
| F078 | User creation time mutable | User created_at update rejects | D |
| F079 | Note creation time mutable | Note created_at update rejects | D |
| F080 | Device creation time mutable | device_created_at update rejects | D |
| F081 | Real text edit leaves server edit unchanged | Changed title/body advances updated_at | D |
| F082 | No-op update advances last edited | Same text leaves updated_at unchanged | D |
| F083 | Hiding note advances last edited | deleted_at changes; updated_at preserved | D |
| F084 | Restoring note advances last edited | Restore alone preserves updated_at | D |
| F085 | Manual updated_at bypass succeeds | Direct protected clock change denied/overridden as specified | D |
| F086 | Initial device edit differs from device creation | Initial device timestamps satisfy implemented initialization rule | D |
| F087 | Device clock controls expiry | Extreme device time does not move server deadline | D |
| F088 | Device clock controls purge | Extreme device time does not move trash retention | D |
| F089 | Timezone display changes the stored instant | Equivalent timezone-offset inputs preserve instant | D |
| F090 | Device-only metadata update acts as text edit | Test existing trigger contract separately from real content edit | D |

### Title-only expiry lifecycle

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F091 | New title-only note lacks expiry | First saved title-only row has server-based 24-hour deadline | D |
| F092 | Draft starts saved-note expiry | Blank/title-only draft deadline remains NULL | D |
| F093 | Filled note retains expiry | Real body clears deadline | D |
| F094 | Clearing body loses timer | Filled-to-empty body starts fresh 24-hour timer | D |
| F095 | Repeated blank save extends expiry | Existing blank deadline remains unchanged | D |
| F096 | Title edit resets blank-body timer | Title-only edit retains original deadline | D |
| F097 | Manual deadline extension succeeds | Direct override denied/normalized to lifecycle result | D |
| F098 | Manual deadline removal succeeds | Saved title-only row cannot cancel required deadline | D |
| F099 | Saved note converted back to draft | Transition rejects rather than canceling timer | D |
| F100 | Expiry worker deletes before deadline | Row just before deadline stays active | D |
| F101 | Exact deadline ignored | Due row at deadline moves to trash under implemented comparison | D |
| F102 | Expiry causes immediate permanent deletion | Due row remains in trash with server deletion time | D |
| F103 | Filled rows selected for expiry | Expiry job leaves real-body note untouched | D |
| F104 | Already trashed row gets fresh expiry deletion time | Repeated worker run preserves first deleted_at | D |
| F105 | Concurrent body fill ignored by cleanup | Locked competing transitions settle with lifecycle-consistent body/deadline/trash state | C |

### Trash, restore and purge

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F106 | New note inserted directly into trash | Non-NULL deleted_at insert rejects | D |
| F107 | User forges deletion clock | First hide uses server time | D |
| F108 | Repeated hide extends retention | deleted_at remains first-hide time | D |
| F109 | Trashed note stays in active view | active_notes excludes it | D |
| F110 | Restore before 14 days fails | Eligible restore becomes active | D |
| F111 | Restore at 14 days succeeds | Exact retention boundary rejects | D |
| F112 | Restore after 14 days succeeds | Expired restore rejects even before worker purge | D |
| F113 | Purge removes fresh trash | Just-before-14-day row remains | D |
| F114 | Purge ignores exact due boundary | Due-at-14-day row removed | D |
| F115 | Purge deletes active notes | NULL deleted_at rows remain | D |
| F116 | Body edited while still trashed | Prohibited text edit rejects | D |
| F117 | Draft status edited while still trashed | Prohibited draft transition rejects | D |
| F118 | Title-only restore reuses expired deadline | Eligible restore starts fresh 24-hour deadline | D |
| F119 | App permanently deletes a saved note | Direct saved-note DELETE denied | D |
| F120 | Worker purges restored row concurrently | Competing restore/purge honors locks and final retention eligibility | C |

### Maintenance target, batching and transaction behavior

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F121 | Target check removed | Wrong target stops before any maintenance command | U |
| F122 | Database/cluster checks joined with AND | Either mismatch independently refuses | U |
| F123 | Both identity values wrong still accepted | Both-wrong identity refuses with only identity read | U |
| F124 | Target port switched to preserved database | Exact connector port remains 55432 | U |
| F125 | Target user/host/timeout altered | Exact connector values merlin_d6/127.0.0.1/3 | U |
| F126 | Identity query fails but cleanup continues | Raised read error prevents timeouts and writes | U |
| F127 | Boolean/floats accepted as batch | True/1.0/1.5 reject before connector | U |
| F128 | Missing/string batch incidental error | None/"100" produce deliberate ValueError before connector | U |
| F129 | Batch boundaries changed | 1/1000 accept; 0/1001 reject | U/D |
| F130 | Batch interpolated into query | Exact parameterized call passes separate tuple | U |
| F131 | Worker skips or swaps cleanup functions | Complete ordered command list matches contract | U |
| F132 | Lock/statement timeout omitted | Both exact local timeouts occur before cleanup | U |
| F133 | Expiry failure still calls purge | No purge after expiry error; same error escapes | U |
| F134 | Purge failure commits expiry changes | Real second-stage failure rolls back first-stage writes | D |
| F135 | Concurrent workers process overlapping batches | SKIP LOCKED/batch caps verified with two sessions, no duplicate transitions | C |

### CLI, probe and migration readiness

| ID | Fault to introduce or challenge | Required evidence | Layer |
|---|---|---|---|
| F136 | --once runs twice | Exactly one cycle; no sleep | U |
| F137 | Custom interval ignored | Every sleep uses requested accepted interval | U |
| F138 | Invalid interval prompts for secret | Invalid/negative/unknown argument exits before prompt/work | U |
| F139 | Worker error printed with password | No secret in stdout/stderr/SystemExit; no success/retry | U |
| F140 | Counts swapped in output | Exact displayed expiry/purge counts match distinct values | U |
| F141 | Interrupt causes another cleanup cycle | Interrupt stops without later work | U |
| F142 | Probe opens writable transaction | read_only set before SELECT; real probe cannot write | P |
| F143 | Probe queries wrong target | Exact disposable connector and expected identity reported | P |
| F144 | Probe connection error reports success | Failure exits nonzero, no success line/credential disclosure | P |
| F145 | Probe or worker hides real database failures | Connection/permission/query errors have deliberate nonzero failure behavior | P |
| F146 | Migration ignores absent PL/Python | Missing dependency fails before creating users/notes | D |
| F147 | Migration accepts wrong server package pins | Missing/mismatched package versions fail before schema creation | D |
| F148 | Migration failure leaves partial schema | Decide atomic migration execution; injected later failure leaves no partial objects under that contract | D |
| F149 | Committed insert disappears on reconnect | Separate real connection sees committed synthetic row; rollback row absent | D |
| F150 | Undo/reapply loses required protections | Disposable undo/reapply restores all constraints, triggers, grants and indexes; down migration currently absent | D |

## Evidence record and next action

For each implemented test, record scenario ID, test node ID, independently expected result, actual result, layer, target fingerprint for database tests, and any matching mutation result. A proposed case has status PENDING, never PASS. Mutation survival is a coverage finding, not automatically a product bug. Contract decisions remain OPEN until resolved.

First action: write the two strict type guards described in [input-validation-fixes.md](../learning/input-type-validation-fixes.md), then rerun the unchanged 90-case suite. Next strengthen full worker call sequences, accepted result tuples and CLI output as listed above. Add probe unit specifications to executable tests only when learner writes them. Resolve whitespace-title/Unicode contracts before asserting an answer.

Do not start 150 experiments inside an invisible extra block. Day 6 remains 360 minutes with a 39-minute verification allocation; actual elapsed learning time is unknown. This expanded catalogue is a reusable backlog. Unfinished verification stays visible and displaces later feature time. AWS and DSA remain deferred.

📚 Learn first: Python unittest.mock documentation, https://docs.python.org/3/library/unittest.mock.html ; pytest parametrization guide, https://docs.pytest.org/en/stable/how-to/parametrize.html ; PostgreSQL transaction tutorial, https://www.postgresql.org/docs/17/tutorial-transactions.html . Reference links; not reverified online this turn.

↩ Return: explain which failures are Python decisions, which require real PostgreSQL, and why an existing failing test cannot count as detecting a new mutation.
