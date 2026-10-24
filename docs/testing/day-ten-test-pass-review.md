# Day 10 test pass review

Review date: October 24, 2026. Scope: the assistant-authored Day 10 read-only notes-list slice and the guarded full-suite failure/recovery. This is a code and evidence review, not proof of learner authorship or production security.

## Finding

The final pass was not produced by weakening application behavior or hiding failed tests. In the initial and final runs, the ordinary Python baseline passed. The first full-suite failure came from stale fault mutation text; after that was corrected, a second run exposed stale inventory IDs. Those failures were retained and fixed at their source in the test harness. No app behavior, test assertion, expected result, skip, or permission was changed during that diagnosis.

The implementation itself had been added earlier at the learner’s task-specific request. It is exercised by four new unit tests and eleven targeted faults. These use mocked PostgreSQL connections, so they check the repository’s SQL and transaction instructions, not PostgreSQL’s actual enforcement of them.

## What failed, and what changed

| Attempt | Observed failure | Cause | Repair |
|---|---|---|---|
| First guarded run | `Incomplete or duplicate python-case-faults inventory`; six `UNAPPLIED` faults | Six existing mutation definitions searched for literal limits `175`/`7000` and literal draft predicates. The implementation now uses named constants `MAX_TITLE_WEIGHTED_LENGTH` and `MAX_BODY_WEIGHTED_LENGTH`, so the mutations no longer applied. | Updated only the mutation source patterns in `tools/check_mutations.py` to target the current named-constant expressions. Their behavior still changes the boundary or incorrectly exempts drafts. |
| Second guarded run | Same inventory error | The test inventory retained eight old AST fault IDs after `app/note_rules.py` had been refactored. The actual source generated twelve current IDs. It also listed a misspelled test node ID: `test_active_note_list_uses_owner_and_uses_read_only_active_query`; pytest collected `test_active_note_list_sets_owner_and_uses_read_only_active_query`. | Replaced the stale AST IDs with the twelve IDs generated from the current source and corrected the node ID to the collected test name. No test case was removed. |
| Third guarded run | PASS | Fault definitions, test inventory and collected cases matched. | No test or implementation change was needed to obtain this pass. |

The first two failures were harness failures, not failing application tests. Both stopped later stages in the respective runs. Final run: all seven stages passed. The Python baseline reported 1,199 passed and 3 subtests passed. The final Python effectiveness result reported 819/819 cases demonstrated and 312 detected faults, with zero survivors, invalid mutations or unapplied mutations. Three duplicate-AST faults were classified as aliases to canonical faults; four known import-guard reversals were explicitly classified as invalid harness mutations. The validator checks the exact alias and exclusion inventories. SQL case/fault shards, lifecycle checks, migration/cleanup checks, documentation audit and whitespace audit passed. Documentation audit had zero errors, one expected missing-Day warning, and 27 verification items.

One intermediate direct audit command, run inside the sandbox, failed before mutation work because the sandbox denied loopback socket creation used by existing health API tests (`PermissionError`). This was an execution restriction, not a product/test failure. The final guarded suite was run outside that restriction and passed.

The final run took 60 seconds wall time; reported stage times sum to 90.515 seconds because database and Python lanes overlap. This was a local working-tree run, not hosted CI. The report does not claim an exact committed SHA or remote verification.

## New test review

| Test | Requirement checked | Evidence and limitation |
|---|---|---|
| `test_weighted_prefix_keeps_complete_display_units` | Weighted cap, emoji/grapheme integrity, zero limit, and rejecting bool/negative limits | Uses concrete ASCII, emoji, flag, family emoji and combining-accent examples. Detected `weighted-prefix-limit-ignored` and `weighted-prefix-codepoint-split`. |
| `test_active_note_list_uses_body_prefix_when_title_is_missing` | Untitled preview stops at 175 weighted units; stored title wins; selected fields and order are specified | 171 ASCII units plus a family emoji (four weighted units) is retained as an intact 175-unit prefix; trailing text is excluded. Detected preview-not-truncated, stored-title-discarded, and ordering mutations. |
| `test_active_note_list_sets_owner_and_uses_read_only_active_query` | Read-only transaction, transaction-local actor, explicit owner parameter, active-notes view and deterministic ordering | Compares the complete normalized SQL and bound parameters. Detected owner-filter removal, trash-view bypass, reversed ordering, session-wide actor setting and read-write transaction mutations. It does not execute SQL against PostgreSQL. |
| `test_active_note_list_rejects_missing_actor_and_busy_connection_before_query` | Reject missing actor and caller-owned transaction before database work | Checks no transaction/query starts for either condition. Detected both corresponding mutations. The connection state is mocked. |

The full audit also rechecked existing title/body boundaries, including exact limits and over-limit drafts. The six repaired mutations were all detected: relaxed/too-strict title and body bounds, and draft title/body limit bypass. Representative detecting cases are listed below.

| Fault | Detecting case examples |
|---|---|
| `title-bound-relaxed` | `test_plain_title_limit[176-False]`, `test_over_limit_title_rejected_even_for_drafts[emoji176]` |
| `title-bound-too-strict` | `test_plain_title_limit[175-True]`, `test_combining_characters_accepted_at_display_limit[title-175]` |
| `body-bound-relaxed` | `test_plain_body_limit[7001-False]`, `test_over_limit_body_rejected_even_for_drafts[spaces7001]` |
| `body-bound-too-strict` | `test_plain_body_limit[7000-True]`, `test_combining_characters_accepted_at_display_limit[body-7000]` |
| `draft-title-bypasses-limit` | `test_over_limit_title_rejected_even_for_drafts[emoji176]` |
| `draft-body-bypasses-limit` | `test_over_limit_body_rejected_even_for_drafts[family7004]` |

The audit verifies that every baseline case passed, every case detected at least one injected fault, every injected test failure was attributed to a collected case, and the complete case/fault inventories matched. A shared mutation kill proves effectiveness for that tested change; it does not alone prove two cases are nonredundant. The new tests have distinct direct-helper, repository-output and SQL-scope assertions.

## 4.2 follow-up — October 24, 2026

At the learner's explicit request, two repository tests and two isolated faults were added. No application code or existing assertion was changed.

| Added case | What it protects | Fault proof |
|---|---|---|
| `test_active_note_list_rejects_malformed_actor_before_query` | A string that looks like a UUID is not accepted as the typed trusted actor; rejection occurs before a transaction or SQL call. | `notes-malformed-actor-accepted` was detected by this exact case. |
| `test_active_note_list_binds_each_actor_when_connection_is_reused` | Two sequential list calls on one idle mocked connection each set a transaction-local actor and bind that same call's UUID in the owner predicate. | `notes-owner-parameter-hardcoded` was detected by this case and the existing owner-SQL case. |

The connection-reuse case confirms the repository's issued SQL and transaction API calls. It does **not** emulate PostgreSQL session state or prove a real pool returned the connection safely. Existing database case F071 independently checks that the synthetic application role sees only its current actor's records; it still does not invoke this Python repository. Since the selected feature is list-only, no foreign-ID lookup exists. Fetched-note concealment remains deferred until a fetch-by-ID slice is selected.

The focused repository module passed: 6 tests in 0.35 seconds. An earlier guarded run took 59.365 seconds; it was superseded by the later 58.477-second run and fresh CI-entry rehearsal recorded below. The earlier run also passed its stages, database shards, cleanup and source-preservation gates. It was local evidence, not hosted CI.

## Final CI-entry verification — October 24, 2026

The first copied-source rehearsal stopped in `verify_suite_execution.py`: the CI identity substitution changed `tests/test_note_rules_and_maintenance.py`, while its copied witness manifest retained the original source hash. `copy_inputs` now updates that copied hash and records the adapted source in `source-inputs.json`; the original checkout remains hash-verified and unchanged. A CI self-check covers this adaptation.

The next copied run detected all 314 executable Python faults but exceeded the 60-second cap by 0.562s. The fault worker ceiling increased from 16 to 20. A code review then found that the sandbox was snapshotting an unchanged source container into a new image, costing about four seconds. When the verified runtime has no persistent file changes, the sandbox now reuses the exact immutable base image and verifies it again inside each clone. The first control run found Docker may omit `Config.Labels`; the runtime adapter now treats absent labels as an empty set, and its self-check covers that shape.

Final local CI-entry rehearsal `/tmp/merlin-day10-ci-entry-20261024-r8/ci-summary.json`: PASS, 91.826s overall, `--include-untracked`, all three CI steps passed, cleanup passed. Nested full suite: 59.125s/60.0s, 20 workers, all 821 cases and 314 executable faults demonstrated, 11/11 MER-11 faults detected at their intended witnesses, all eight retained evidence reports present and checksummed. This rehearsal is not hosted exact-revision CI.

## Application changes reviewed

- `app/note_rules.py` centralizes the existing UTF-8/NUL/grapheme validation in `_validated_graphemes`, names the existing weighted title/body caps, and adds `truncate_weighted`. `weighted_length` still applies the same emoji weight to each grapheme. Existing validators still use the same 175/7000 limits and error strings.
- `app/notes_repository.py` accepts a UUID supplied by its caller, rejects an absent/wrong type and a non-idle connection, owns one transaction, marks it read-only, sets `merlin.actor_id` transaction-locally, filters the active view by the same bound owner UUID, and orders by update time then ID. It formats titles after reading rows and returns an immutable list item. It does not authenticate or expose a route.
- Diagnostic repairs changed only `tools/check_mutations.py` anchors and `tests/suite-inventory.json` IDs/list entries. They did not change the application code or loosen test assertions.

## Limits still open

1. The repository tests use `MagicMock`; they do not prove RLS isolation, actual PostgreSQL transaction reset, or behavior on a reused real connection. Existing database tests exercise schema/RLS rules separately, but do not call this repository. Add a guarded disposable-database integration test before treating repository/database ownership as integration-tested.
2. There is no login/authentication layer or notes route. The UUID argument is trusted only by contract. Do not pass request-supplied `user_id`; do not expose this function publicly until trusted authentication supplies the actor.
3. There is no route-level generic database error handling or response/log non-disclosure test. Database errors propagate from this repository. A future route must map them to a safe generic response and prove private sentinels/details do not escape.
4. The selected operation is list-only. Foreign-ID behavior is not implemented or tested because there is no fetch-by-ID operation.
5. The preview cap is interpreted as the existing **175 weighted display units** (emoji count as four; other graphemes count as one), not 175 Python code points. Confirm that interpretation if “characters” was intended to mean a different measure.
6. Hosted exact-revision CI is pending. The current local green run does not satisfy the next-day cumulative hosted-CI gate.

## Next learner review

Read the repository and tests, confirm the weighted-unit interpretation, and explain the transaction/identity boundary. Review actual PostgreSQL isolation/error handling before any route is added. Do not mark 4.1 complete from this assistant-authored code or local passing tests alone.

## Assistant-run 4.1–4.2 validation — October 24, 2026

Commands run:

```text
.venv/bin/python -m pytest -q tests/test_notes_repository.py tests/test_note_rules_and_maintenance.py
MERLIN_RUN_DB_TESTS=1 .venv/bin/python -m pytest -q tests/test_users_notes_database.py
```

Results: the focused repository/rules run passed **208 tests in 0.39 seconds**. The opt-in PostgreSQL suite passed **383 tests in 143.40 seconds** against the guarded disposable database, using synthetic records and transaction rollback. The database suite covers schema, constraints, roles, and RLS behavior; it does not call `app.notes_repository`.

The latest complete guarded suite is `/tmp/merlin-day10-ci-entry-20261024-r8/suite/summary.json`; all seven stages passed in 59.125 seconds under the hard 60-second gate (20 Python-fault workers). The fresh CI-entry rehearsal also passed in 91.826 seconds overall, including source tests, the complete suite and separate migration roundtrip. It used the uncommitted working tree. The suite reported 1,201 Python tests plus 3 subtests, 821/821 cases and 314 executable faults detected at pinned checks. Cleanup and source preservation passed. Hosted CI remains pending.

These runs complete the test-execution portion of 4.2. They do not complete the learner review/explain-back in 4.1 or the learner review of assistant-authored tests in 4.2. They also do not prove real PostgreSQL execution or connection-pool reuse by `app.notes_repository`; that integration test remains open. Foreign-ID behavior is not applicable to the selected list-only operation.
