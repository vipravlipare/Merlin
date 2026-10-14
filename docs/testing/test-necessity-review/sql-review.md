# SQL case and fault necessity review

Reviewed 2026-10-12. Read-only source and supplied evidence review. No database commands or new tests ran. Application, tests, tools, migrations and evidence remain unchanged.

The JSON companion contains the complete concrete SQL, assertions, observed diagnostics and individual decision for every baseline and pair. This document is the human-readable decision index.

## Counts and interpretation

- 389 baselines: 388 CASES and one genuine reconnect rollback case.
- 653 pair rows: 652 stored-SQL recipe applications plus one reconnect patch.
- 70 distinct stored-SQL bodies plus reconnect: 71 total implementations. Requested “71 SQL faults plus reconnect” overcounts supplied evidence by one.
- Reported results: 550 assertion detections, 53 behavior errors, 50 survivals. These are historical report classifications, not newly executed results.
- Five lifecycle baseline/fault rows; 36 migration checks: two roundtrip branches, 14 gates, three concurrency checks, 17 repairs.

Baseline decisions: {'KEEP': 339, 'IMPROVE': 45, 'MERGE': 5}. Pair decisions: {'KEEP': 522, 'IMPROVE': 81, 'REMOVE': 50}. No test was removed. MERGE/REMOVE are review recommendations only.

## Findings

1. Merge five historical Unicode cases into named parity successors. Only unicode-blank-title and parity-U+00A0-title are exact normalized scripts. Four others are equivalent or weaker same-input checks; stronger successor assertions stay.
2. Keep every distinct Unicode input and SQL/Python layer. Each code point can differ under a realistic faulty implementation. Constant-helper kill sets cannot prove semantic redundancy.
3. Remove 50 unrelated mutation pairings from mandatory proof, preserving baselines and fault implementations in relevant tests. These expected survivals do not justify weakening product assertions.
4. Twenty-nine maintenance whitespace mutations fail fixture preparation at notes_deadline_matches_body before role/worker assertions. Improve injection placement and target worker/policy definitions. F049-F050 also fails its shared seed before its own assertion.
5. Whole weighted-length overcount fails the unchanged body constraint in three title-limit cases. Use a realistic title boundary/counting regression. Keep ASCII below/at/above and combining/emoji/draft paths separately.
6. F069 detects an exact error mismatch from a secondary FK, not successful forbidden user-ID change. Use an unreferenced user to isolate trigger behavior. App immutable-column grant mutants also hit secondary triggers, but expected 42501 remains a valid permission boundary oracle.
7. Worker RETURN 0/1 stubs prove gross count/state oracle responsiveness. They do not prove deadline inclusivity, retention eligibility, actor filtering, oldest-first ordering or batch arguments. Keep a smoke mutant and add localized source faults.
8. Reconnect FK-removal mutation fails before reconnect observation; baseline genuinely reconnects. Keep baseline, add premature-commit mutation to isolate persistence check. Lifecycle premature-commit fault already demonstrates cleanup/purge atomicity.
9. F104 needs a first-effect assertion; F118 needs exact restored 24-hour deadline. Legal batch argument cases currently operate on no eligible rows. Index LIKE checks need semantic/validity checks.
10. Keep two-session expiry/purge lock tests, committed cascade/reconnect layer, both migration permission branches and all negative migration gates. valid-gate can reuse false-branch successful down completion.
11. Migration guard-removal extra-index experiment has a concrete counterfactual. In contrast, injected postcheck changes mainly prove oracle checks reject selected damage; they do not simulate every naturally occurring undo defect.
12. No new runtime correctness or comprehensive security claim follows from this review. Historical PUBLIC CREATE baseline remains unknown.

## Exact duplicate normalization

Normalization changes only unquoted layout. Literal spaces, Unicode code points, roles, placeholders, commands and assertions stay significant. It does not equate INSERT with UPDATE, privileged with app/worker roles, or transaction-only with committed/reconnected execution.

- unicode-blank-title, parity-U+00A0-title

## Every SQL baseline decision

| Case | Decision | Concrete property | Rationale and exact overlaps |
|---|---|---|---|
| F015-plain | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F015-emoji | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F015-family | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F015-skin | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F015-flag | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F015-keycap | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F015-accent | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F015-cjk | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F015-empty | KEEP | Database uses the pinned grapheme-weighting rule | Database uses the pinned grapheme-weighting rule is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| limit-title-174 | KEEP | Weighted text limit also applies to updates | Weighted text limit also applies to updates is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| limit-title-175 | KEEP | Weighted text limit also applies to updates | Weighted text limit also applies to updates is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| limit-title-176 | KEEP | Weighted text limit also applies to updates | Weighted text limit also applies to updates is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F020 | KEEP | Combining graphemes fit at the limit | Combining graphemes fit at the limit is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| draft-title-overflow | KEEP | Drafts cannot bypass text limits | Drafts cannot bypass text limits is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| emoji-title-overflow | KEEP | Emoji weigh four in direct SQL | Emoji weigh four in direct SQL is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| limit-body-6999 | KEEP | Weighted text limit also applies to updates | Weighted text limit also applies to updates is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| limit-body-7000 | KEEP | Weighted text limit also applies to updates | Weighted text limit also applies to updates is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| limit-body-7001 | KEEP | Weighted text limit also applies to updates | Weighted text limit also applies to updates is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F021 | KEEP | Combining graphemes fit at the limit | Combining graphemes fit at the limit is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| draft-body-overflow | KEEP | Drafts cannot bypass text limits | Drafts cannot bypass text limits is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| emoji-body-overflow | KEEP | Emoji weigh four in direct SQL | Emoji weigh four in direct SQL is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F031 | KEEP | Blank titles normalize to NULL and preserve body | Blank titles normalize to NULL and preserve body is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F033 | KEEP | Nonblank title whitespace is preserved | Nonblank title whitespace is preserved is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F034 | KEEP | Body whitespace is preserved | Body whitespace is preserved is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F036 | KEEP | Fully blank saved rows reject | Fully blank saved rows reject is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F037 | KEEP | Fully blank drafts are permitted without countdown | Fully blank drafts are permitted without countdown is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F038 | KEEP | Title-only notes persist with a one-day deadline | Title-only notes persist with a one-day deadline is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F087, F091, note-body-default |
| F039 | KEEP | Body-only notes persist | Body-only notes persist is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F040 | KEEP | Spaces and blank lines do not make saved content | Spaces and blank lines do not make saved content is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F049-F050 | IMPROVE | Multiple users can omit email | Retain required behavior; add direct two-row inserts in the case body so the before_seed mutant proves the case oracle rather than failing common fixture creation. |
| F051 | KEEP | Case variants of an email are duplicates | Case variants of an email are duplicates is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| email-insert-duplicate | KEEP | Email uniqueness also rejects a new user | Email uniqueness also rejects a new user is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| email-blank | KEEP | Direct SQL email must be nonblank and unpadded | Direct SQL email must be nonblank and unpadded is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| email-spaces | KEEP | Direct SQL email must be nonblank and unpadded | Direct SQL email must be nonblank and unpadded is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| email-leading | KEEP | Direct SQL email must be nonblank and unpadded | Direct SQL email must be nonblank and unpadded is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| email-trailing | KEEP | Direct SQL email must be nonblank and unpadded | Direct SQL email must be nonblank and unpadded is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| username-null | KEEP | Username is required lowercase ASCII with a 20-character cap | Username is required lowercase ASCII with a 20-character cap is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| username-upper | KEEP | Username is required lowercase ASCII with a 20-character cap | Username is required lowercase ASCII with a 20-character cap is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| username-empty | KEEP | Username is required lowercase ASCII with a 20-character cap | Username is required lowercase ASCII with a 20-character cap is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| username-twenty-one | KEEP | Username is required lowercase ASCII with a 20-character cap | Username is required lowercase ASCII with a 20-character cap is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| username-punctuation | KEEP | Username is required lowercase ASCII with a 20-character cap | Username is required lowercase ASCII with a 20-character cap is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| username-twenty | KEEP | Twenty-character username accepts and canonical lookup agrees | Twenty-character username accepts and canonical lookup agrees is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| username-duplicate | KEEP | Duplicate username is rejected | Duplicate username is rejected is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F059 | KEEP | Canonical username cannot be supplied independently | Canonical username cannot be supplied independently is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F061-user | KEEP | User default ID is a UUIDv4 | User default ID is a UUIDv4 is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F061-note | IMPROVE | Note default ID is independent UUIDv4 | Check the UUID RFC variant explicitly, matching F061-user, and prove two generated note IDs differ. |
| uuid-users-version | KEEP | Explicit IDs must have UUIDv4 version and variant | Explicit IDs must have UUIDv4 version and variant is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| uuid-users-variant | KEEP | Explicit IDs must have UUIDv4 version and variant | Explicit IDs must have UUIDv4 version and variant is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| uuid-notes-version | KEEP | Explicit IDs must have UUIDv4 version and variant | Explicit IDs must have UUIDv4 version and variant is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| uuid-notes-variant | KEEP | Explicit IDs must have UUIDv4 version and variant | Explicit IDs must have UUIDv4 version and variant is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F064 | KEEP | Duplicate note ID rejects | Duplicate note ID rejects is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F065 | KEEP | Owner is required | Owner is required is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F066 | KEEP | Owner must exist | Owner must exist is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F067 | KEEP | Deleting one user cascades only their notes | Deleting one user cascades only their notes is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: app-delete-account-cascade, committed-reconnect-cascade |
| F068 | KEEP | Immutable identity/creation fields cannot be changed | Immutable identity/creation fields cannot be changed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F069 | IMPROVE | Immutable identity/creation fields cannot be changed | Use a user without referencing notes for the identity-trigger check, while preserving a separate foreign-key safety case. Current injected trigger removal fails from FK before the expected trigger diagnostic. |
| F070 | KEEP | Immutable identity/creation fields cannot be changed | Immutable identity/creation fields cannot be changed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F078 | KEEP | Immutable identity/creation fields cannot be changed | Immutable identity/creation fields cannot be changed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F079 | KEEP | Immutable identity/creation fields cannot be changed | Immutable identity/creation fields cannot be changed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F080 | KEEP | Immutable identity/creation fields cannot be changed | Immutable identity/creation fields cannot be changed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F071 | KEEP | App role sees only its actor's rows | App role sees only its actor's rows is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F072 | KEEP | App cannot edit another actor's note | App cannot edit another actor's note is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F073 | KEEP | App cannot insert for another actor | App cannot insert for another actor is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F074 | KEEP | Missing actor sees no protected rows | Missing actor sees no protected rows is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: app-unset-actor |
| F075-role | KEEP | App cannot escalate to object owner | App cannot escalate to object owner is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-column-id | KEEP | Column grants forbid app changes to protected fields | Column grants forbid app changes to protected fields is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-column-user_id | KEEP | Column grants forbid app changes to protected fields | Column grants forbid app changes to protected fields is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-column-created_at | KEEP | Column grants forbid app changes to protected fields | Column grants forbid app changes to protected fields is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-column-updated_at | KEEP | Column grants forbid app changes to protected fields | Column grants forbid app changes to protected fields is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-column-blank_body_expires_at | KEEP | Column grants forbid app changes to protected fields | Column grants forbid app changes to protected fields is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-own-edit | KEEP | App can edit its own content | App can edit its own content is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-saved-delete | KEEP | App cannot permanently delete a saved note | App cannot permanently delete a saved note is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-blank-draft-delete | KEEP | App can delete its own blank draft | App can delete its own blank draft is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F076 | KEEP | Device cannot forge server-created time | Device cannot forge server-created time is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F077, user-clock-forged |
| F077 | KEEP | Initial server times are equal | Initial server times are equal is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F076, user-clock-forged |
| F081 | KEEP | Content edits advance server edit time | Content edits advance server edit time is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F082 | KEEP | No-op save keeps Last Edited | No-op save keeps Last Edited is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F083 | KEEP | Hiding a note keeps Last Edited | Hiding a note keeps Last Edited is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F084 | KEEP | Restoring a note keeps Last Edited | Restoring a note keeps Last Edited is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F110 |
| F085 | KEEP | Manual server edit time is overridden for no-op | Manual server edit time is overridden for no-op is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F086 | KEEP | Initial device edit time equals device creation | Initial device edit time equals device creation is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F087 | KEEP | Device time cannot control expiry | Device time cannot control expiry is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F038 |
| F088 | KEEP | Device time cannot control retention | Device time cannot control retention is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F089 | KEEP | Different timezone offsets preserve an instant | Different timezone offsets preserve an instant is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F090 | KEEP | Device-only metadata update does not fake a text edit | Device-only metadata update does not fake a text edit is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F092 | KEEP | Title-only draft has no countdown | Title-only draft has no countdown is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F093 | KEEP | Adding real body clears countdown | Adding real body clears countdown is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F094 | KEEP | Returning to blank starts a new countdown | Returning to blank starts a new countdown is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F095 | KEEP | A saved blank-body deadline cannot be extended or removed | A saved blank-body deadline cannot be extended or removed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F096 | KEEP | A saved blank-body deadline cannot be extended or removed | A saved blank-body deadline cannot be extended or removed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F097 | KEEP | A saved blank-body deadline cannot be extended or removed | A saved blank-body deadline cannot be extended or removed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F098 | KEEP | A saved blank-body deadline cannot be extended or removed | A saved blank-body deadline cannot be extended or removed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F099 | KEEP | Saved notes cannot become drafts | Saved notes cannot become drafts is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F100 | KEEP | Worker cannot expire a future title-only note | Worker cannot expire a future title-only note is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F102 | KEEP | Overdue title-only notes enter trash instead of disappearing | Overdue title-only notes enter trash instead of disappearing is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: expiry-batch-one, maintenance-expiry |
| F103 | KEEP | Worker leaves filled notes alone | Worker leaves filled notes alone is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F104 | IMPROVE | Repeated expiry keeps first trash time | Assert the first expiry really trashes the row and establishes a non-NULL first_time before testing a repeat. Constant-return mutation currently fails the repeated count without proving the first side effect. |
| F106 | KEEP | New notes cannot be inserted into trash | New notes cannot be inserted into trash is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F107 | KEEP | Caller cannot forge deletion time | Caller cannot forge deletion time is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F108 | KEEP | Repeated hiding preserves first deletion time | Repeated hiding preserves first deletion time is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F109 | KEEP | Active view excludes trash | Active view excludes trash is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F110 | IMPROVE | Fresh trash can be restored | Keep successful restore/view observation, but add restore-trigger-specific mutation; current false-view fault only proves view observation. Overlap: F084 |
| F112 | KEEP | Restore after retention is rejected | Restore after retention is rejected is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F113 | KEEP | Fresh trash survives purge | Fresh trash survives purge is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F115 | KEEP | Active rows survive purge | Active rows survive purge is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| purge-overdue | KEEP | Overdue trash is removed | Overdue trash is removed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: maintenance-overdue-purge, purge-batch-one |
| F116 | KEEP | Trashed body cannot be edited | Trashed body cannot be edited is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F117 | KEEP | Trashed draft cannot be published | Trashed draft cannot be published is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F118 | IMPROVE | Restored title-only note gets a new countdown | Assert exact restored deadline equals server statement time plus 24 hours; current >now()+23 hours accepts 48 hours or longer. |
| sql-batch-cleanup_expired_blank_notes-NULL | KEEP | SQL cleanup refuses invalid batch sizes | SQL cleanup refuses invalid batch sizes is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| sql-batch-cleanup_expired_blank_notes-0 | KEEP | SQL cleanup refuses invalid batch sizes | SQL cleanup refuses invalid batch sizes is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| sql-batch-cleanup_expired_blank_notes-1001 | KEEP | SQL cleanup refuses invalid batch sizes | SQL cleanup refuses invalid batch sizes is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| sql-batch-purge_deleted_notes-NULL | KEEP | SQL cleanup refuses invalid batch sizes | SQL cleanup refuses invalid batch sizes is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| sql-batch-purge_deleted_notes-0 | KEEP | SQL cleanup refuses invalid batch sizes | SQL cleanup refuses invalid batch sizes is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| sql-batch-purge_deleted_notes-1001 | KEEP | SQL cleanup refuses invalid batch sizes | SQL cleanup refuses invalid batch sizes is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| maintenance-fresh-delete | KEEP | Maintenance cannot delete recent trash | Maintenance cannot delete recent trash is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| maintenance-active-read | KEEP | Maintenance cannot read non-due active content | Maintenance cannot read non-due active content is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| maintenance-overdue-purge | KEEP | Maintenance can purge only due trash | Maintenance can purge only due trash is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: purge-overdue |
| maintenance-expiry | KEEP | Maintenance can expire due rows | Maintenance can expire due rows is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F102 |
| F045-nbsp | KEEP | Python and SQL agree that nonbreaking-space-only body is blank | Python and SQL agree that nonbreaking-space-only body is blank is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F053-nbsp | KEEP | Direct SQL rejects nonbreaking-space padding on email | Direct SQL rejects nonbreaking-space padding on email is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F091 | KEEP | New title-only note starts exactly one day after server creation | New title-only note starts exactly one day after server creation is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F038, note-body-default |
| F101 | KEEP | Expiry includes the exact server-statement deadline | Expiry includes the exact server-statement deadline is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| F114 | KEEP | Purge includes the exact retention boundary | Purge includes the exact retention boundary is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-own-insert | KEEP | App can insert for its own actor | App can insert for its own actor is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-crossuser-delete | KEEP | App cannot delete another user's account or note | App cannot delete another user's account or note is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-unset-actor | KEEP | Unset actor fails closed | Unset actor fails closed is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F074 |
| app-active-view | KEEP | Active view preserves the actor boundary | Active view preserves the actor boundary is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| required-body | KEEP | Required note data cannot be NULL | Required note data cannot be NULL is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| required-device_created_at | KEEP | Required note data cannot be NULL | Required note data cannot be NULL is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| required-is_draft | KEEP | Required note data cannot be NULL | Required note data cannot be NULL is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| permission-groups | KEEP | All permission groups lack administrative or login powers | All permission groups lack administrative or login powers is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| rls-forced | KEEP | Both tables have forced row policies | Both tables have forced row policies is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| app-no-cleanup-grant | IMPROVE | App cannot execute maintenance functions | Keep cleanup denial and add independently named purge permission denial. Current case covers only one of two maintenance functions. |
| app-no-schema-create | KEEP | App cannot create public schema objects | App cannot create public schema objects is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| index-created | IMPROVE | Timeline index has the intended owner/order keys | Keep structural index requirement; inspect catalog key order/directions/predicate semantically and check validity. Text LIKE can reject equivalent formatting and does not prove index validity or planner use. |
| index-edited | IMPROVE | Timeline index has the intended owner/order keys | Keep structural index requirement; inspect catalog key order/directions/predicate semantically and check validity. Text LIKE can reject equivalent formatting and does not prove index validity or planner use. |
| index-device | IMPROVE | Timeline index has the intended owner/order keys | Keep structural index requirement; inspect catalog key order/directions/predicate semantically and check validity. Text LIKE can reject equivalent formatting and does not prove index validity or planner use. |
| index-draft | IMPROVE | Timeline index has the intended owner/order keys | Keep structural index requirement; inspect catalog key order/directions/predicate semantically and check validity. Text LIKE can reject equivalent formatting and does not prove index validity or planner use. |
| app-delete-account-cascade | KEEP | Deleting one's own account removes saved notes too | Deleting one's own account removes saved notes too is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. Overlap: F067, committed-reconnect-cascade |
| sql-valid-batch-cleanup_expired_blank_notes-1 | IMPROVE | SQL accepts both valid batch boundaries | Keep exact legal argument boundary, but add eligible-row side effects and source-local validation mutant. Empty eligible set with RETURN 0 also accepts ignored arguments. |
| sql-valid-batch-cleanup_expired_blank_notes-1000 | IMPROVE | SQL accepts both valid batch boundaries | Keep exact legal argument boundary, but add eligible-row side effects and source-local validation mutant. Empty eligible set with RETURN 0 also accepts ignored arguments. |
| sql-valid-batch-purge_deleted_notes-1 | IMPROVE | SQL accepts both valid batch boundaries | Keep exact legal argument boundary, but add eligible-row side effects and source-local validation mutant. Empty eligible set with RETURN 0 also accepts ignored arguments. |
| sql-valid-batch-purge_deleted_notes-1000 | IMPROVE | SQL accepts both valid batch boundaries | Keep exact legal argument boundary, but add eligible-row side effects and source-local validation mutant. Empty eligible set with RETURN 0 also accepts ignored arguments. |
| expiry-batch-one | KEEP | Expiry processes the oldest due row and respects batch one | Expiry processes the oldest due row and respects batch one is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| purge-batch-one | KEEP | Purge processes the oldest trash and respects batch one | Purge processes the oldest trash and respects batch one is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| note-body-default | KEEP | Omitted body defaults to empty text and gets a saved countdown | Omitted body defaults to empty text and gets a saved countdown is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| user-id-duplicate | KEEP | A duplicate user ID rejects even with a different username | A duplicate user ID rejects even with a different username is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| user-clock-forged | KEEP | User server clocks also override device-forged insert values | User server clocks also override device-forged insert values is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| unicode-blank-title | MERGE | Nonbreaking-space-only titles normalize to NULL | Exact same statement, role, fixture and assertion. Retain target case and independent Python coverage. Overlap: parity-U+00A0-title |
| unicode-blank-countdown | MERGE | Nonbreaking-space-only body starts a title-only countdown | Same NBSP transition/deadline; target also verifies exact stored body. Retain target case and independent Python coverage. Overlap: parity-U+00A0-countdown |
| unicode-email-padding-leading | MERGE | Each Unicode-padding edge is rejected independently | Equivalent single NBSP leading padding, same SQLSTATE and constraint. Target expresses identical text by concatenation. Retain target case and independent Python coverage. Overlap: parity-U+00A0-email-leading |
| unicode-email-padding-trailing | MERGE | Each Unicode-padding edge is rejected independently | Equivalent single NBSP trailing padding, same SQLSTATE and constraint. Target expresses identical text by concatenation. Retain target case and independent Python coverage. Overlap: parity-U+00A0-email-trailing |
| unicode-blank-draft-delete | MERGE | App can delete a draft that Python considers fully blank | Same NBSP blank owner draft deletion; target additionally preserves other owner row. Retain target case and independent Python coverage. Overlap: parity-U+00A0-draft-delete |
| blank-body-U+0009 | KEEP | Unicode whitespace alone cannot be saved as note content | U+0009 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+000A | KEEP | Unicode whitespace alone cannot be saved as note content | U+000A is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+000B | KEEP | Unicode whitespace alone cannot be saved as note content | U+000B is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+000C | KEEP | Unicode whitespace alone cannot be saved as note content | U+000C is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+000D | KEEP | Unicode whitespace alone cannot be saved as note content | U+000D is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+001C | KEEP | Unicode whitespace alone cannot be saved as note content | U+001C is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+001D | KEEP | Unicode whitespace alone cannot be saved as note content | U+001D is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+001E | KEEP | Unicode whitespace alone cannot be saved as note content | U+001E is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+001F | KEEP | Unicode whitespace alone cannot be saved as note content | U+001F is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+0020 | KEEP | Unicode whitespace alone cannot be saved as note content | U+0020 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+0085 | KEEP | Unicode whitespace alone cannot be saved as note content | U+0085 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+1680 | KEEP | Unicode whitespace alone cannot be saved as note content | U+1680 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2000 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2000 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2001 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2001 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2002 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2002 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2003 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2003 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2004 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2004 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2005 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2005 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2006 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2006 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2007 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2007 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2008 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2008 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2009 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2009 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+200A | KEEP | Unicode whitespace alone cannot be saved as note content | U+200A is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2028 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2028 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+2029 | KEEP | Unicode whitespace alone cannot be saved as note content | U+2029 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+202F | KEEP | Unicode whitespace alone cannot be saved as note content | U+202F is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+205F | KEEP | Unicode whitespace alone cannot be saved as note content | U+205F is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| blank-body-U+3000 | KEEP | Unicode whitespace alone cannot be saved as note content | U+3000 is an independently valid Python whitespace input. Saved-content rejection has a separate constraint oracle; keep SQL and Python checks independently. |
| parity-U+0009-title | KEEP | All blank titles normalize to NULL | U+0009 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0009-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+0009 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0009-email-leading | KEEP | SQL rejects every blank/padded stored email | U+0009 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0009-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+0009 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0009-email-blank | KEEP | SQL rejects every blank/padded stored email | U+0009 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0009-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+0009 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0009-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+000A-title | KEEP | All blank titles normalize to NULL | U+000A independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000A-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+000A independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000A-email-leading | KEEP | SQL rejects every blank/padded stored email | U+000A independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000A-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+000A independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000A-email-blank | KEEP | SQL rejects every blank/padded stored email | U+000A independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000A-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+000A independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000A-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+000B-title | KEEP | All blank titles normalize to NULL | U+000B independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000B-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+000B independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000B-email-leading | KEEP | SQL rejects every blank/padded stored email | U+000B independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000B-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+000B independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000B-email-blank | KEEP | SQL rejects every blank/padded stored email | U+000B independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000B-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+000B independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000B-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+000C-title | KEEP | All blank titles normalize to NULL | U+000C independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000C-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+000C independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000C-email-leading | KEEP | SQL rejects every blank/padded stored email | U+000C independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000C-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+000C independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000C-email-blank | KEEP | SQL rejects every blank/padded stored email | U+000C independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000C-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+000C independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000C-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+000D-title | KEEP | All blank titles normalize to NULL | U+000D independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000D-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+000D independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000D-email-leading | KEEP | SQL rejects every blank/padded stored email | U+000D independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000D-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+000D independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000D-email-blank | KEEP | SQL rejects every blank/padded stored email | U+000D independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000D-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+000D independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+000D-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+001C-title | KEEP | All blank titles normalize to NULL | U+001C independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001C-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+001C independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001C-email-leading | KEEP | SQL rejects every blank/padded stored email | U+001C independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001C-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+001C independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001C-email-blank | KEEP | SQL rejects every blank/padded stored email | U+001C independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001C-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+001C independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001C-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+001D-title | KEEP | All blank titles normalize to NULL | U+001D independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001D-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+001D independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001D-email-leading | KEEP | SQL rejects every blank/padded stored email | U+001D independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001D-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+001D independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001D-email-blank | KEEP | SQL rejects every blank/padded stored email | U+001D independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001D-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+001D independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001D-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+001E-title | KEEP | All blank titles normalize to NULL | U+001E independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001E-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+001E independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001E-email-leading | KEEP | SQL rejects every blank/padded stored email | U+001E independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001E-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+001E independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001E-email-blank | KEEP | SQL rejects every blank/padded stored email | U+001E independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001E-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+001E independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001E-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+001F-title | KEEP | All blank titles normalize to NULL | U+001F independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001F-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+001F independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001F-email-leading | KEEP | SQL rejects every blank/padded stored email | U+001F independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001F-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+001F independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001F-email-blank | KEEP | SQL rejects every blank/padded stored email | U+001F independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001F-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+001F independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+001F-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+0020-title | KEEP | All blank titles normalize to NULL | U+0020 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0020-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+0020 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0020-email-leading | KEEP | SQL rejects every blank/padded stored email | U+0020 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0020-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+0020 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0020-email-blank | KEEP | SQL rejects every blank/padded stored email | U+0020 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0020-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+0020 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0020-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+0085-title | KEEP | All blank titles normalize to NULL | U+0085 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0085-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+0085 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0085-email-leading | KEEP | SQL rejects every blank/padded stored email | U+0085 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0085-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+0085 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0085-email-blank | KEEP | SQL rejects every blank/padded stored email | U+0085 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0085-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+0085 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+0085-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+00A0-title | KEEP | All blank titles normalize to NULL | U+00A0 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+00A0-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+00A0 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+00A0-email-leading | KEEP | SQL rejects every blank/padded stored email | U+00A0 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+00A0-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+00A0 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+00A0-email-blank | KEEP | SQL rejects every blank/padded stored email | U+00A0 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+00A0-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+00A0 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+00A0-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+1680-title | KEEP | All blank titles normalize to NULL | U+1680 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+1680-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+1680 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+1680-email-leading | KEEP | SQL rejects every blank/padded stored email | U+1680 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+1680-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+1680 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+1680-email-blank | KEEP | SQL rejects every blank/padded stored email | U+1680 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+1680-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+1680 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+1680-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2000-title | KEEP | All blank titles normalize to NULL | U+2000 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2000-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2000 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2000-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2000 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2000-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2000 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2000-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2000 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2000-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2000 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2000-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2001-title | KEEP | All blank titles normalize to NULL | U+2001 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2001-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2001 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2001-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2001 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2001-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2001 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2001-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2001 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2001-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2001 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2001-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2002-title | KEEP | All blank titles normalize to NULL | U+2002 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2002-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2002 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2002-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2002 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2002-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2002 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2002-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2002 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2002-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2002 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2002-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2003-title | KEEP | All blank titles normalize to NULL | U+2003 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2003-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2003 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2003-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2003 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2003-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2003 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2003-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2003 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2003-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2003 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2003-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2004-title | KEEP | All blank titles normalize to NULL | U+2004 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2004-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2004 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2004-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2004 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2004-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2004 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2004-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2004 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2004-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2004 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2004-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2005-title | KEEP | All blank titles normalize to NULL | U+2005 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2005-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2005 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2005-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2005 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2005-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2005 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2005-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2005 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2005-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2005 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2005-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2006-title | KEEP | All blank titles normalize to NULL | U+2006 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2006-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2006 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2006-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2006 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2006-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2006 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2006-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2006 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2006-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2006 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2006-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2007-title | KEEP | All blank titles normalize to NULL | U+2007 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2007-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2007 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2007-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2007 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2007-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2007 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2007-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2007 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2007-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2007 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2007-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2008-title | KEEP | All blank titles normalize to NULL | U+2008 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2008-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2008 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2008-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2008 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2008-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2008 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2008-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2008 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2008-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2008 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2008-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2009-title | KEEP | All blank titles normalize to NULL | U+2009 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2009-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2009 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2009-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2009 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2009-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2009 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2009-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2009 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2009-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2009 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2009-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+200A-title | KEEP | All blank titles normalize to NULL | U+200A independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+200A-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+200A independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+200A-email-leading | KEEP | SQL rejects every blank/padded stored email | U+200A independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+200A-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+200A independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+200A-email-blank | KEEP | SQL rejects every blank/padded stored email | U+200A independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+200A-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+200A independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+200A-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2028-title | KEEP | All blank titles normalize to NULL | U+2028 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2028-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2028 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2028-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2028 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2028-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2028 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2028-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2028 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2028-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2028 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2028-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+2029-title | KEEP | All blank titles normalize to NULL | U+2029 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2029-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+2029 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2029-email-leading | KEEP | SQL rejects every blank/padded stored email | U+2029 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2029-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+2029 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2029-email-blank | KEEP | SQL rejects every blank/padded stored email | U+2029 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2029-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+2029 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+2029-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+202F-title | KEEP | All blank titles normalize to NULL | U+202F independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+202F-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+202F independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+202F-email-leading | KEEP | SQL rejects every blank/padded stored email | U+202F independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+202F-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+202F independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+202F-email-blank | KEEP | SQL rejects every blank/padded stored email | U+202F independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+202F-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+202F independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+202F-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+205F-title | KEEP | All blank titles normalize to NULL | U+205F independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+205F-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+205F independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+205F-email-leading | KEEP | SQL rejects every blank/padded stored email | U+205F independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+205F-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+205F independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+205F-email-blank | KEEP | SQL rejects every blank/padded stored email | U+205F independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+205F-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+205F independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+205F-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-U+3000-title | KEEP | All blank titles normalize to NULL | U+3000 independently exercises title. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+3000-countdown | KEEP | All blank saved bodies start the 24-hour countdown | U+3000 independently exercises countdown. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+3000-email-leading | KEEP | SQL rejects every blank/padded stored email | U+3000 independently exercises email-leading. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+3000-email-trailing | KEEP | SQL rejects every blank/padded stored email | U+3000 independently exercises email-trailing. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+3000-email-blank | KEEP | SQL rejects every blank/padded stored email | U+3000 independently exercises email-blank. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+3000-draft-delete | KEEP | Owner can delete every whitespace-only draft | U+3000 independently exercises draft-delete. Different Unicode inputs can regress separately; identical kill sets from constant helper faults do not establish redundant inputs. |
| parity-U+3000-maintenance | IMPROVE | Limited worker sees and expires every due blank body | Keep independent code point and maintenance-role safety boundary. Install worker/policy-specific fault after historical fixture is valid; current blank-helper mutant fails before worker assertions. |
| parity-nonwhitespace-U+200B | KEEP | Invisible nonwhitespace remains real SQL content | Invisible nonwhitespace remains real SQL content is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| parity-nonwhitespace-U+FEFF | KEEP | Invisible nonwhitespace remains real SQL content | Invisible nonwhitespace remains real SQL content is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| parity-nonwhitespace-U+2060 | KEEP | Invisible nonwhitespace remains real SQL content | Invisible nonwhitespace remains real SQL content is a distinct direct-SQL input, transition or privilege boundary. Python validation cannot substitute for stored SQL enforcement. |
| test_failed_second_write_rolls_back_first_write_after_reconnect | IMPROVE | Failed second write rolls back first after reconnect | Keep real reconnect transaction atomicity baseline; current missing-FK mutation fails at the expected error assertion before reconnect absence is checked. Add a disposable premature-commit fault to prove the rollback observation independently. Overlap: F066, second-operation-failure-rolls-back-cleanup |

## Every distinct fault implementation

Complete SQL and per-pair observed diagnostics are in sql-review.json. IDs identify exact SQL plus before-seed placement; names are descriptive aliases.

| Fault | Names | Decision | Cases | Rationale |
|---|---|---|---|---|
| SQL-F001 | incorrect-weighted-count | IMPROVE | F015-accent, F015-cjk, F015-emoji, F015-family, F015-flag, F015-keycap, F015-plain, F015-skin | Constant helper replacement proves integration calls the helper, but erases all input distinctions. Add realistic regex/strip/grapheme or one-codepoint regressions; do not infer that repeated identical kills prove every Unicode branch. |
| SQL-F002 | incorrect-weighted-count | IMPROVE | F015-empty | Constant helper replacement proves integration calls the helper, but erases all input distinctions. Add realistic regex/strip/grapheme or one-codepoint regressions; do not infer that repeated identical kills prove every Unicode branch. |
| SQL-F003 | valid-text-overcounted | IMPROVE | F020, F021, limit-body-6999, limit-body-7000, limit-title-174, limit-title-175 | Synthetic blanket over-restriction predictably rejects valid input. Keep only a smoke pairing and prefer a localized existing limit/predicate regression. Blanket overcount affects other field constraints, obscuring tested title boundary. |
| SQL-F004 | constraint-removed-notes_title_limit | KEEP | draft-title-overflow, emoji-title-overflow, limit-title-176 | Removing notes_title_limit permits title weighted overflow through both UPDATE and draft INSERT; these are distinct enforcement paths. |
| SQL-F005 | constraint-removed-notes_body_limit | KEEP | draft-body-overflow, emoji-body-overflow, limit-body-7001 | Removing notes_body_limit permits body weighted overflow through both UPDATE and draft INSERT; preserve positive legal boundaries separately. |
| SQL-F006 | whitespace-misclassified-content | IMPROVE | F031, F036, F040, F045-nbsp, blank-body-U+0009, blank-body-U+000A, blank-body-U+000B, blank-body-U+000C, blank-body-U+000D, blank-body-U+001C, blank-body-U+001D, blank-body-U+001E, blank-body-U+001F, blank-body-U+0020, blank-body-U+0085, blank-body-U+1680, blank-body-U+2000, blank-body-U+2001, blank-body-U+2002, blank-body-U+2003, blank-body-U+2004, blank-body-U+2005, blank-body-U+2006, blank-body-U+2007, blank-body-U+2008, blank-body-U+2009, blank-body-U+200A, blank-body-U+2028, blank-body-U+2029, blank-body-U+202F, blank-body-U+205F, blank-body-U+3000, parity-U+0009-countdown, parity-U+0009-draft-delete, parity-U+0009-maintenance, parity-U+0009-title, parity-U+000A-countdown, parity-U+000A-draft-delete, parity-U+000A-maintenance, parity-U+000A-title, parity-U+000B-countdown, parity-U+000B-draft-delete, parity-U+000B-maintenance, parity-U+000B-title, parity-U+000C-countdown, parity-U+000C-draft-delete, parity-U+000C-maintenance, parity-U+000C-title, parity-U+000D-countdown, parity-U+000D-draft-delete, parity-U+000D-maintenance, parity-U+000D-title, parity-U+001C-countdown, parity-U+001C-draft-delete, parity-U+001C-maintenance, parity-U+001C-title, parity-U+001D-countdown, parity-U+001D-draft-delete, parity-U+001D-maintenance, parity-U+001D-title, parity-U+001E-countdown, parity-U+001E-draft-delete, parity-U+001E-maintenance, parity-U+001E-title, parity-U+001F-countdown, parity-U+001F-draft-delete, parity-U+001F-maintenance, parity-U+001F-title, parity-U+0020-countdown, parity-U+0020-draft-delete, parity-U+0020-maintenance, parity-U+0020-title, parity-U+0085-countdown, parity-U+0085-draft-delete, parity-U+0085-maintenance, parity-U+0085-title, parity-U+00A0-countdown, parity-U+00A0-draft-delete, parity-U+00A0-maintenance, parity-U+00A0-title, parity-U+1680-countdown, parity-U+1680-draft-delete, parity-U+1680-maintenance, parity-U+1680-title, parity-U+2000-countdown, parity-U+2000-draft-delete, parity-U+2000-maintenance, parity-U+2000-title, parity-U+2001-countdown, parity-U+2001-draft-delete, parity-U+2001-maintenance, parity-U+2001-title, parity-U+2002-countdown, parity-U+2002-draft-delete, parity-U+2002-maintenance, parity-U+2002-title, parity-U+2003-countdown, parity-U+2003-draft-delete, parity-U+2003-maintenance, parity-U+2003-title, parity-U+2004-countdown, parity-U+2004-draft-delete, parity-U+2004-maintenance, parity-U+2004-title, parity-U+2005-countdown, parity-U+2005-draft-delete, parity-U+2005-maintenance, parity-U+2005-title, parity-U+2006-countdown, parity-U+2006-draft-delete, parity-U+2006-maintenance, parity-U+2006-title, parity-U+2007-countdown, parity-U+2007-draft-delete, parity-U+2007-maintenance, parity-U+2007-title, parity-U+2008-countdown, parity-U+2008-draft-delete, parity-U+2008-maintenance, parity-U+2008-title, parity-U+2009-countdown, parity-U+2009-draft-delete, parity-U+2009-maintenance, parity-U+2009-title, parity-U+200A-countdown, parity-U+200A-draft-delete, parity-U+200A-maintenance, parity-U+200A-title, parity-U+2028-countdown, parity-U+2028-draft-delete, parity-U+2028-maintenance, parity-U+2028-title, parity-U+2029-countdown, parity-U+2029-draft-delete, parity-U+2029-maintenance, parity-U+2029-title, parity-U+202F-countdown, parity-U+202F-draft-delete, parity-U+202F-maintenance, parity-U+202F-title, parity-U+205F-countdown, parity-U+205F-draft-delete, parity-U+205F-maintenance, parity-U+205F-title, parity-U+3000-countdown, parity-U+3000-draft-delete, parity-U+3000-maintenance, parity-U+3000-title, unicode-blank-countdown, unicode-blank-draft-delete, unicode-blank-title | Constant helper replacement proves integration calls the helper, but erases all input distinctions. Add realistic regex/strip/grapheme or one-codepoint regressions; do not infer that repeated identical kills prove every Unicode branch. |
| SQL-F007 | real-content-trimmed | KEEP | F033 | Trimming nonblank title damages exact preserved user text; title preservation is independent of body preservation. |
| SQL-F008 | real-content-trimmed | KEEP | F034 | Trimming body damages exact preserved body whitespace; distinct field path from title trimming. |
| SQL-F009 | constraint-removed-notes_has_content | KEEP | F036, F040, F045-nbsp, blank-body-U+0009, blank-body-U+000A, blank-body-U+000B, blank-body-U+000C, blank-body-U+000D, blank-body-U+001C, blank-body-U+001D, blank-body-U+001E, blank-body-U+001F, blank-body-U+0020, blank-body-U+0085, blank-body-U+1680, blank-body-U+2000, blank-body-U+2001, blank-body-U+2002, blank-body-U+2003, blank-body-U+2004, blank-body-U+2005, blank-body-U+2006, blank-body-U+2007, blank-body-U+2008, blank-body-U+2009, blank-body-U+200A, blank-body-U+2028, blank-body-U+2029, blank-body-U+202F, blank-body-U+205F, blank-body-U+3000 | Removing notes_has_content admits fully blank saved content when countdown constraint remains satisfied; essential independent stored-content barrier. |
| SQL-F010 | drafts-now-forbidden | IMPROVE | F037, F092 | Synthetic blanket over-restriction predictably rejects valid input. Keep only a smoke pairing and prefer a localized existing limit/predicate regression. Blanket overcount affects other field constraints, obscuring tested title boundary. |
| SQL-F011 | countdown-too-short | KEEP | F038, F087, F091, F093, F094, F095, F096, F097, F098, F118, note-body-default, parity-U+0009-countdown, parity-U+000A-countdown, parity-U+000B-countdown, parity-U+000C-countdown, parity-U+000D-countdown, parity-U+001C-countdown, parity-U+001D-countdown, parity-U+001E-countdown, parity-U+001F-countdown, parity-U+0020-countdown, parity-U+0085-countdown, parity-U+00A0-countdown, parity-U+1680-countdown, parity-U+2000-countdown, parity-U+2001-countdown, parity-U+2002-countdown, parity-U+2003-countdown, parity-U+2004-countdown, parity-U+2005-countdown, parity-U+2006-countdown, parity-U+2007-countdown, parity-U+2008-countdown, parity-U+2009-countdown, parity-U+200A-countdown, parity-U+2028-countdown, parity-U+2029-countdown, parity-U+202F-countdown, parity-U+205F-countdown, parity-U+3000-countdown, unicode-blank-countdown | Changing existing 24-hour intervals to one hour exercises actual deadline assignment branches. Keep start/restart/restore pairings; preservation-only survivors are not relevant. |
| SQL-F012 | countdown-not-preserved | KEEP | F038, F087, F091, F093, F094, F095, F096, F097, F098, F118, note-body-default, parity-U+0009-countdown, parity-U+000A-countdown, parity-U+000B-countdown, parity-U+000C-countdown, parity-U+000D-countdown, parity-U+001C-countdown, parity-U+001D-countdown, parity-U+001E-countdown, parity-U+001F-countdown, parity-U+0020-countdown, parity-U+0085-countdown, parity-U+00A0-countdown, parity-U+1680-countdown, parity-U+2000-countdown, parity-U+2001-countdown, parity-U+2002-countdown, parity-U+2003-countdown, parity-U+2004-countdown, parity-U+2005-countdown, parity-U+2006-countdown, parity-U+2007-countdown, parity-U+2008-countdown, parity-U+2009-countdown, parity-U+200A-countdown, parity-U+2028-countdown, parity-U+2029-countdown, parity-U+202F-countdown, parity-U+205F-countdown, parity-U+3000-countdown, unicode-blank-countdown | Changing existing preserved deadline assignment to fresh 48-hour value targets forbidden extension. Keep F095-F098; initial/restarted deadlines do not execute this branch. |
| SQL-F013 | optional-title-now-required | KEEP | F039 | Making optional title NOT NULL rejects a legitimate body-only row; protects optional-field contract independently of blank-title normalization. |
| SQL-F014 | null-emails-now-unique | IMPROVE | F049-F050 | Realistic NULL uniqueness regression, but current application before shared seed fails setup. Retain implementation; make the tested optional-email insert an explicit case operation. |
| SQL-F015 | email-uniqueness-removed | KEEP | F051, email-insert-duplicate | Dropping lowercase email unique index admits case-variant duplicates. UPDATE and INSERT enforcement must both stay. |
| SQL-F016 | email-cleanliness-always-accepts, stored-email-validation-removed | IMPROVE | F053-nbsp, email-blank, email-insert-duplicate, email-leading, email-spaces, email-trailing, parity-U+0009-email-blank, parity-U+0009-email-leading, parity-U+0009-email-trailing, parity-U+000A-email-blank, parity-U+000A-email-leading, parity-U+000A-email-trailing, parity-U+000B-email-blank, parity-U+000B-email-leading, parity-U+000B-email-trailing, parity-U+000C-email-blank, parity-U+000C-email-leading, parity-U+000C-email-trailing, parity-U+000D-email-blank, parity-U+000D-email-leading, parity-U+000D-email-trailing, parity-U+001C-email-blank, parity-U+001C-email-leading, parity-U+001C-email-trailing, parity-U+001D-email-blank, parity-U+001D-email-leading, parity-U+001D-email-trailing, parity-U+001E-email-blank, parity-U+001E-email-leading, parity-U+001E-email-trailing, parity-U+001F-email-blank, parity-U+001F-email-leading, parity-U+001F-email-trailing, parity-U+0020-email-blank, parity-U+0020-email-leading, parity-U+0020-email-trailing, parity-U+0085-email-blank, parity-U+0085-email-leading, parity-U+0085-email-trailing, parity-U+00A0-email-blank, parity-U+00A0-email-leading, parity-U+00A0-email-trailing, parity-U+1680-email-blank, parity-U+1680-email-leading, parity-U+1680-email-trailing, parity-U+2000-email-blank, parity-U+2000-email-leading, parity-U+2000-email-trailing, parity-U+2001-email-blank, parity-U+2001-email-leading, parity-U+2001-email-trailing, parity-U+2002-email-blank, parity-U+2002-email-leading, parity-U+2002-email-trailing, parity-U+2003-email-blank, parity-U+2003-email-leading, parity-U+2003-email-trailing, parity-U+2004-email-blank, parity-U+2004-email-leading, parity-U+2004-email-trailing, parity-U+2005-email-blank, parity-U+2005-email-leading, parity-U+2005-email-trailing, parity-U+2006-email-blank, parity-U+2006-email-leading, parity-U+2006-email-trailing, parity-U+2007-email-blank, parity-U+2007-email-leading, parity-U+2007-email-trailing, parity-U+2008-email-blank, parity-U+2008-email-leading, parity-U+2008-email-trailing, parity-U+2009-email-blank, parity-U+2009-email-leading, parity-U+2009-email-trailing, parity-U+200A-email-blank, parity-U+200A-email-leading, parity-U+200A-email-trailing, parity-U+2028-email-blank, parity-U+2028-email-leading, parity-U+2028-email-trailing, parity-U+2029-email-blank, parity-U+2029-email-leading, parity-U+2029-email-trailing, parity-U+202F-email-blank, parity-U+202F-email-leading, parity-U+202F-email-trailing, parity-U+205F-email-blank, parity-U+205F-email-leading, parity-U+205F-email-trailing, parity-U+3000-email-blank, parity-U+3000-email-leading, parity-U+3000-email-trailing, unicode-email-padding-leading, unicode-email-padding-trailing | Always-true email helper validates oracle integration and every input case rejects via exact constraint. Add source-local whitespace-edge/blank regressions because a constant erases input distinctions; overlaps with constraint removal but targets a different responsible layer. |
| SQL-F017 | constraint-removed-users_email_clean | KEEP | F053-nbsp, email-blank, email-leading, email-spaces, email-trailing, parity-U+0009-email-blank, parity-U+0009-email-leading, parity-U+0009-email-trailing, parity-U+000A-email-blank, parity-U+000A-email-leading, parity-U+000A-email-trailing, parity-U+000B-email-blank, parity-U+000B-email-leading, parity-U+000B-email-trailing, parity-U+000C-email-blank, parity-U+000C-email-leading, parity-U+000C-email-trailing, parity-U+000D-email-blank, parity-U+000D-email-leading, parity-U+000D-email-trailing, parity-U+001C-email-blank, parity-U+001C-email-leading, parity-U+001C-email-trailing, parity-U+001D-email-blank, parity-U+001D-email-leading, parity-U+001D-email-trailing, parity-U+001E-email-blank, parity-U+001E-email-leading, parity-U+001E-email-trailing, parity-U+001F-email-blank, parity-U+001F-email-leading, parity-U+001F-email-trailing, parity-U+0020-email-blank, parity-U+0020-email-leading, parity-U+0020-email-trailing, parity-U+0085-email-blank, parity-U+0085-email-leading, parity-U+0085-email-trailing, parity-U+00A0-email-blank, parity-U+00A0-email-leading, parity-U+00A0-email-trailing, parity-U+1680-email-blank, parity-U+1680-email-leading, parity-U+1680-email-trailing, parity-U+2000-email-blank, parity-U+2000-email-leading, parity-U+2000-email-trailing, parity-U+2001-email-blank, parity-U+2001-email-leading, parity-U+2001-email-trailing, parity-U+2002-email-blank, parity-U+2002-email-leading, parity-U+2002-email-trailing, parity-U+2003-email-blank, parity-U+2003-email-leading, parity-U+2003-email-trailing, parity-U+2004-email-blank, parity-U+2004-email-leading, parity-U+2004-email-trailing, parity-U+2005-email-blank, parity-U+2005-email-leading, parity-U+2005-email-trailing, parity-U+2006-email-blank, parity-U+2006-email-leading, parity-U+2006-email-trailing, parity-U+2007-email-blank, parity-U+2007-email-leading, parity-U+2007-email-trailing, parity-U+2008-email-blank, parity-U+2008-email-leading, parity-U+2008-email-trailing, parity-U+2009-email-blank, parity-U+2009-email-leading, parity-U+2009-email-trailing, parity-U+200A-email-blank, parity-U+200A-email-leading, parity-U+200A-email-trailing, parity-U+2028-email-blank, parity-U+2028-email-leading, parity-U+2028-email-trailing, parity-U+2029-email-blank, parity-U+2029-email-leading, parity-U+2029-email-trailing, parity-U+202F-email-blank, parity-U+202F-email-leading, parity-U+202F-email-trailing, parity-U+205F-email-blank, parity-U+205F-email-leading, parity-U+205F-email-trailing, parity-U+3000-email-blank, parity-U+3000-email-leading, parity-U+3000-email-trailing, unicode-email-padding-leading, unicode-email-padding-trailing | Dropping email cleanliness constraint admits unpadded/blank storage through direct SQL; distinct from removing email uniqueness. |
| SQL-F018 | required-column-now-nullable | KEEP | username-null | Dropping username NOT NULL permits required username to become NULL because CHECK alone accepts SQL NULL; distinct SQL NULL semantic barrier. |
| SQL-F019 | constraint-removed-users_username_format | KEEP | username-empty, username-punctuation, username-twenty-one, username-upper | Dropping username format admits uppercase, empty, excessive length and punctuation inputs. Keep separate examples; a realistic faulty regex can affect one class only. |
| SQL-F020 | valid-username-limit-too-strict | IMPROVE | username-twenty | Synthetic blanket over-restriction predictably rejects valid input. Keep only a smoke pairing and prefer a localized existing limit/predicate regression. Blanket overcount affects other field constraints, obscuring tested title boundary. |
| SQL-F021 | constraint-removed-users_username_unique | KEEP | username-duplicate | Dropping username uniqueness admits another account name collision; distinct from generated canonical column protection. |
| SQL-F022 | canonical-column-not-generated | KEEP | F059 | Dropping generated expression permits independent canonical value update; proves exact generated-column error, not merely lookup agreement. |
| SQL-F023 | uuid-default-missing | KEEP | F061-user | Dropping users.id default rejects omitted-ID user insert; user default is separate catalog property from notes.id default. |
| SQL-F024 | uuid-default-missing | KEEP | F061-note | Dropping notes.id default rejects omitted-ID note insert; preserve independent user default test. |
| SQL-F025 | constraint-removed-users_id_uuidv4 | KEEP | uuid-users-variant, uuid-users-version | Dropping users_id_uuidv4 admits explicitly wrong version/variant user identifiers. Both bit properties are separate invalid inputs. |
| SQL-F026 | constraint-removed-notes_id_uuidv4 | KEEP | uuid-notes-variant, uuid-notes-version | Dropping notes_id_uuidv4 admits explicitly wrong version/variant note identifiers. This is a distinct table constraint from user IDs. |
| SQL-F027 | constraint-removed-notes_pkey | KEEP | F064 | Dropping notes primary key admits duplicate note IDs; weighted content and UUIDv4 checks cannot guarantee uniqueness. |
| SQL-F028 | required-column-now-nullable | KEEP | F065 | Dropping owner NOT NULL admits ownerless notes because FK alone accepts NULL; separate from nonexistent-owner FK rejection. |
| SQL-F029 | constraint-removed-notes_user_id_fkey | KEEP | F066 | Dropping notes owner FK admits otherwise valid UUID missing owner; separate from owner NULL and cascade action. |
| SQL-F030 | cascade-now-restricts | KEEP | F067, app-delete-account-cascade | Replacing CASCADE with NO ACTION preserves owner existence validation but breaks account deletion. Privileged and app-role cascade cases exercise distinct privilege interactions. |
| SQL-F031 | immutable-fields-no-longer-protected | KEEP | F068, F069, F070, F078, F079, F080 | Whole timestamp trigger pass-through removes multiple identity/creation protections. Relevant cases cover user/note IDs, note owner and server/device creation fields; keep distinct inputs. F069 requires isolated unreferenced user. |
| SQL-F032 | actor-policies-allow-everyone | KEEP | F071, F072, F073, F074, app-active-view, app-crossuser-delete, app-unset-actor | Opening users and notes actor policies tests cross-owner read/update/insert/delete and missing actor fail-closed. Broad mutation merits future separate USING/WITH CHECK/table faults; current operations are not redundant. |
| SQL-F033 | app-can-assume-owner | KEEP | F075-role | Granting owner membership introduces actual role-escalation ability; session authorization case checks member status and role switch independently of content RLS. |
| SQL-F034 | protected-column-write-granted | KEEP | app-column-id | Granting note id UPDATE removes expected permission rejection even though identity trigger still rejects with another SQLSTATE. Strict 42501 oracle is necessary. |
| SQL-F035 | protected-column-write-granted | KEEP | app-column-user_id | Granting note user_id UPDATE exposes owner-transfer trigger instead of required permission rejection; layered protection does not make column-grant oracle redundant. |
| SQL-F036 | protected-column-write-granted | KEEP | app-column-created_at | Granting created_at UPDATE exposes immutable server-creation trigger instead of required 42501; detects grant drift despite trigger protection. |
| SQL-F037 | protected-column-write-granted | KEEP | app-column-updated_at | Granting updated_at UPDATE lets no-op clock write proceed through normalization, so expected 42501 assertion detects this distinct clock grant. |
| SQL-F038 | protected-column-write-granted | KEEP | app-column-blank_body_expires_at | Granting blank_body_expires_at UPDATE lets write proceed through content-trigger normalization; expected permission error detects grant regression even with unchanged deadline. |
| SQL-F039 | actor-policy-rejects-owner | KEEP | app-own-edit, app-own-insert | Denying owner policy checks allowed own INSERT and own UPDATE; positive security cases prevent a deny-everything implementation from passing all negative cases. |
| SQL-F040 | saved-notes-permanently-deletable | KEEP | app-saved-delete | Opening restrictive saved-note deletion policy permits irreversible saved-note deletion for owner; distinct from cross-owner filtering. |
| SQL-F041 | blank-draft-deletion-forbidden | KEEP | app-blank-draft-delete, parity-U+0009-draft-delete, parity-U+000A-draft-delete, parity-U+000B-draft-delete, parity-U+000C-draft-delete, parity-U+000D-draft-delete, parity-U+001C-draft-delete, parity-U+001D-draft-delete, parity-U+001E-draft-delete, parity-U+001F-draft-delete, parity-U+0020-draft-delete, parity-U+0085-draft-delete, parity-U+00A0-draft-delete, parity-U+1680-draft-delete, parity-U+2000-draft-delete, parity-U+2001-draft-delete, parity-U+2002-draft-delete, parity-U+2003-draft-delete, parity-U+2004-draft-delete, parity-U+2005-draft-delete, parity-U+2006-draft-delete, parity-U+2007-draft-delete, parity-U+2008-draft-delete, parity-U+2009-draft-delete, parity-U+200A-draft-delete, parity-U+2028-draft-delete, parity-U+2029-draft-delete, parity-U+202F-draft-delete, parity-U+205F-draft-delete, parity-U+3000-draft-delete, unicode-blank-draft-delete | Denying blank draft deletion checks the permitted deletion exception. Distinct Unicode inputs must remain because predicate classification can regress per code point. |
| SQL-F042 | server-insert-clocks-forged | KEEP | F076, F077, user-clock-forged | Changing insert updated_at away from created_at targets equality for note/user inserts. F077 compares both table paths, while forged-input cases also assert server time. |
| SQL-F043 | server-edit-clock-wrong | KEEP | F081, F082, F083, F084, F085, F090 | Changing no-text-edit preservation assignment to future time targets no-op/hide/restore/metadata changes. Content-edit-only F081 survival is expected. |
| SQL-F044 | content-edits-keep-old-clock | KEEP | F081, F082, F083, F084, F085, F090 | Changing actual content-edit timestamp assignment to OLD time targets F081 advancement; no-op/hide/restore cases do not exercise it. |
| SQL-F045 | device-clock-not-normalized | KEEP | F086 | Removing insert device-edit normalization targets unequal supplied device clocks; separate from server creation/edited clocks. |
| SQL-F046 | trash-guards-and-clock-removed | KEEP | F088, F106, F107, F108, F112, F116, F117 | Pass-through deletion trigger removes creation/trash/edit/retention safeguards. Keep each transition and exact error; broad deletion no-op is smoke coverage, not local boundary completeness. |
| SQL-F047 | device-instant-shifted | KEEP | F089 | Adding one hour to device_created_at corrupts supplied instant and makes timezone-equivalent input observation fail; targets input preservation, not timezone library correctness in general. |
| SQL-F048 | body-refill-does-not-clear-countdown | KEEP | F093 | Replacing cleared deadline with 24-hour deadline breaks filled-body invariant and hits notes_deadline_matches_body. Valid refill rejection is relevant layered detection. |
| SQL-F049 | saved-notes-can-become-drafts | KEEP | F099 | Pass-through content trigger permits saved-to-draft reversal; exact forbidden-transition error oracle detects regression. Other content branches need their own targeted faults. |
| SQL-F050 | expiry-output-wrong | IMPROVE | F100, F103, F104, sql-valid-batch-cleanup_expired_blank_notes-1, sql-valid-batch-cleanup_expired_blank_notes-1000 | Constant-return stub is a useful gross-failure oracle exercise but chosen to contradict known expected outputs. Add source-local predicate/batch validation changes that preserve unaffected SQL, role, locking and side effects; do not call the stub proof of every worker rule. |
| SQL-F051 | expiry-output-wrong, invalid-batch-accepted | IMPROVE | F101, F102, app-no-cleanup-grant, expiry-batch-one, maintenance-expiry, parity-U+0009-maintenance, parity-U+000A-maintenance, parity-U+000B-maintenance, parity-U+000C-maintenance, parity-U+000D-maintenance, parity-U+001C-maintenance, parity-U+001D-maintenance, parity-U+001E-maintenance, parity-U+001F-maintenance, parity-U+0020-maintenance, parity-U+0085-maintenance, parity-U+00A0-maintenance, parity-U+1680-maintenance, parity-U+2000-maintenance, parity-U+2001-maintenance, parity-U+2002-maintenance, parity-U+2003-maintenance, parity-U+2004-maintenance, parity-U+2005-maintenance, parity-U+2006-maintenance, parity-U+2007-maintenance, parity-U+2008-maintenance, parity-U+2009-maintenance, parity-U+200A-maintenance, parity-U+2028-maintenance, parity-U+2029-maintenance, parity-U+202F-maintenance, parity-U+205F-maintenance, parity-U+3000-maintenance, sql-batch-cleanup_expired_blank_notes-0, sql-batch-cleanup_expired_blank_notes-1001, sql-batch-cleanup_expired_blank_notes-NULL | Constant-return stub is a useful gross-failure oracle exercise but chosen to contradict known expected outputs. Add source-local predicate/batch validation changes that preserve unaffected SQL, role, locking and side effects; do not call the stub proof of every worker rule. |
| SQL-F052 | active-view-filter-wrong | KEEP | F109 | View WHERE true exposes trash; active-view exclusion must remain separate from RLS owner boundary. |
| SQL-F053 | active-view-filter-wrong | KEEP | F110 | View WHERE false suppresses legitimate restored active row; proves positive visibility but not restore trigger correctness. |
| SQL-F054 | purge-output-wrong | IMPROVE | F113, F115, sql-valid-batch-purge_deleted_notes-1, sql-valid-batch-purge_deleted_notes-1000 | Constant-return stub is a useful gross-failure oracle exercise but chosen to contradict known expected outputs. Add source-local predicate/batch validation changes that preserve unaffected SQL, role, locking and side effects; do not call the stub proof of every worker rule. |
| SQL-F055 | invalid-batch-accepted, purge-output-wrong | IMPROVE | F114, maintenance-overdue-purge, purge-batch-one, purge-overdue, sql-batch-purge_deleted_notes-0, sql-batch-purge_deleted_notes-1001, sql-batch-purge_deleted_notes-NULL | Constant-return stub is a useful gross-failure oracle exercise but chosen to contradict known expected outputs. Add source-local predicate/batch validation changes that preserve unaffected SQL, role, locking and side effects; do not call the stub proof of every worker rule. |
| SQL-F056 | recent-trash-purge-allowed | KEEP | maintenance-fresh-delete | Opening worker restrictive deletion policy permits fresh-trash DELETE; direct worker deletion is a distinct boundary from purge-function selection. |
| SQL-F057 | worker-sees-active-private-content | KEEP | maintenance-active-read | Opening worker visibility policy exposes active private content; crucial negative confidentiality case independent of due-row expiry. |
| SQL-F058 | required-column-now-nullable | KEEP | required-body | Dropping body NOT NULL permits NULL body because other constraints have SQL NULL semantics; exact named column diagnostic matters. |
| SQL-F059 | required-column-now-nullable | KEEP | required-device_created_at | Dropping device_created_at NOT NULL admits missing client original instant; normalization of device_edited_at does not enforce this requirement. |
| SQL-F060 | required-column-now-nullable | KEEP | required-is_draft | Dropping is_draft NOT NULL admits unknown draft state; distinct nullable boolean hazard from body/client clock data. |
| SQL-F061 | permission-role-can-login | KEEP | permission-groups | Making app permission group LOGIN violates administrative role-group contract. Baseline checks all six dangerous flags across three roles; mutation proves one selected flag only. |
| SQL-F062 | owner-not-subject-to-rls | KEEP | rls-forced | Removing notes FORCE RLS changes owner enforcement catalog contract. Baseline also checks users, but this mutation proves only notes FORCE flag; future per-table flag mutants can strengthen. |
| SQL-F063 | app-incorrectly-granted-execute | KEEP | app-no-cleanup-grant | Granting cleanup execute to app removes exact permission denial even though count may return 0. Add separate purge execute denial; current fault is specific to cleanup. |
| SQL-F064 | app-can-create-schema-objects | KEEP | app-no-schema-create | Granting public CREATE lets app create forbidden schema object. Transaction rolls it back; no persistent object is authorized. |
| SQL-F065 | timeline-index-missing | KEEP | index-created | Dropping notes_user_created_idx breaks owner/server-creation timeline index inventory; separate ordering key from edit indexes. |
| SQL-F066 | timeline-index-missing | KEEP | index-edited | Dropping notes_user_updated_idx breaks owner/server-edit/id timeline index contract; server edit order is independent of device edit order. |
| SQL-F067 | timeline-index-missing | KEEP | index-device | Dropping notes_user_device_updated_idx breaks device-edit timeline ordering; cannot substitute server clock index. |
| SQL-F068 | timeline-index-missing | KEEP | index-draft | Dropping partial draft timeline index breaks owner/draft/edit/id active-row index contract; different predicate and key sequence from other timelines. |
| SQL-F069 | constraint-removed-users_pkey | IMPROVE | user-id-duplicate | Dropping users primary key CASCADE also drops dependent notes FK. Prefer independently removing duplicate-ID enforcement in isolated case while documenting collateral FK removal; do not infer owner integrity coverage from duplicate-user case. |
| SQL-F070 | invisible-content-misclassified-blank | IMPROVE | parity-nonwhitespace-U+200B, parity-nonwhitespace-U+2060, parity-nonwhitespace-U+FEFF | Constant helper replacement proves integration calls the helper, but erases all input distinctions. Add realistic regex/strip/grapheme or one-codepoint regressions; do not infer that repeated identical kills prove every Unicode branch. |
| SQL-F071 | missing-note-owner-foreign-key | IMPROVE | test_failed_second_write_rolls_back_first_write_after_reconnect | Keep foreign-key removal as invalid-owner fault. For reconnect atomicity add early commit between writes so the reconnect assertion detects persistence independently. |

## Every lifecycle case and fault

| Case | Decision | Input and assertion | Fault | Rationale |
|---|---|---|---|---|
| committed-reconnect-cascade | IMPROVE | Commit one synthetic user with two body-bearing notes; reconnect reads 2\|t, delete user, reconnect finds 0 notes. | DROP notes_user_id_fkey inside rollback-only transaction. | KEEP committed reconnect baseline; fault uses rollback-only in-transaction cascade assertion, so add a reconnect-specific disposable failure without committing a schema fault. |
| expiry-skips-locked | KEEP | Two overdue blank rows; second session holds oldest FOR UPDATE. Worker batch 1 returns 1, one row trashed, locked first active and second trashed. | Replace FOR UPDATE SKIP LOCKED with FOR UPDATE; observed lock timeout. | Two-session progress is absent from rollback-only single-session SQL. Expected lock timeout is relevant fault evidence. |
| purge-skips-locked | KEEP | Two overdue trash rows; second session locks oldest. Worker batch 1 returns 1, locked first remains and second disappears. | Replace FOR UPDATE SKIP LOCKED with FOR UPDATE; observed lock timeout. | Purge DELETE lock path differs from expiry UPDATE lock path; retain both concurrency faults. |
| expiry-batch-limit | KEEP | Two due blank rows; batch 1 changes exactly one and returns 1. | Remove LIMIT batch_size, observed 2 changed and return 2. | Committed fixtures independently check worker limit; overlap with single-session case does not substitute for lock/reconnect layer. |
| second-operation-failure-rolls-back-cleanup | KEEP | Committed two overdue blank rows; one transaction cleanup(1), purge(0) fails P0001, reconnect sees zero trashed rows. | Insert COMMIT;BEGIN between cleanup and invalid purge. | Real atomicity assertion detects premature commit and complements invalid-owner rollback scenario. |

## Every migration check

| Check | Decision | Concrete input and oracle | Rationale |
|---|---|---|---|
| roundtrip-public-create-false | KEEP | Synthetic public_create_before=False; undo 002 then 001, preserve unrelated review_sentinel/prerequisites/login/PUBLIC permission, replay 001+002, run all 388 CASES through savepoints, compare semantic schema after generated OID normalization and rollback.  | Both historical permission possibilities select different restoration branches. Synthetic baseline is not evidence of actual pre-001 permissions. |
| roundtrip-public-create-true | KEEP | Synthetic public_create_before=True; undo 002 then 001, preserve unrelated review_sentinel/prerequisites/login/PUBLIC permission, replay 001+002, run all 388 CASES through savepoints, compare semantic schema after generated OID normalization and rollback.  | Both historical permission possibilities select different restoration branches. Synthetic baseline is not evidence of actual pre-001 permissions. |
| autocommit-refused | KEEP | AUTOCOMMIT on; down must refuse before DDL. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| migration002-present | KEEP | Leave 002 helper functions installed; refuse unsupported migration order. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| missing-baseline | KEEP | Undo 002 but omit pg_temp permission baseline; refuse guessed permissions. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| valid-gate | MERGE | Undo 002 and supply exactly one non-NULL baseline row; down completes. Positive valid-gate must exit 0 and reach GATE_COMPLETE. | Successful down path is already exercised in both roundtrip branches. Reuse false-branch completion result for this success gate, preserving every negative gate. |
| wrong-cluster | IMPROVE | Replace expected cluster ID with 0 in in-memory down candidate; refuse identity mismatch. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | In-memory expected-constant alteration exercises mismatch branch, but does not connect to a genuine different cluster. Keep rehearsal branch test and label limitation; wrong-database concurrency check is real. |
| nonempty-target | KEEP | Insert gate_test user before down; refuse populated storage. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| missing-view | KEEP | Drop active_notes before down; refuse missing expected view. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| missing-function | KEEP | Drop cleanup_expired_blank_notes(integer); refuse incomplete function inventory. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| role-changed | KEEP | ALTER ROLE merlin_d6_app LOGIN; refuse unsafe permission group. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| membership-changed | KEEP | GRANT owner role TO app; refuse escalation membership. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| empty-baseline | KEEP | Create empty baseline table; reject row count 0. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| duplicate-baseline | KEEP | Add second baseline row; reject row count 2. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| blank-baseline-source | KEEP | Set baseline_source to empty string; reject incomplete provenance. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| null-baseline-value | KEEP | Set public_create_before NULL; reject unknown permissions. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| extra-index | KEEP | CREATE INDEX review_unexpected_idx ON notes(body). Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| extra-trigger | KEEP | Add BEFORE UPDATE trigger invoking manage_note_content. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| extra-constraint | KEEP | Add CHECK(length(body)>=0). Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| extra-policy | KEEP | Add app SELECT USING(true) policy. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| extra-column | KEEP | Add nullable review_extra text column. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| extra-rule | KEEP | Add users INSERT rule DO INSTEAD NOTHING. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| missing-index | KEEP | DROP users_username_canonical_idx. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| missing-trigger | KEEP | DROP notes_content trigger. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| missing-constraint | KEEP | DROP notes_title_limit. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| missing-policy | KEEP | DROP notes_own_account. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| missing-column | KEEP | Remove device_created_at and recreate view; inventory must refuse missing column. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| wrong-public-create | KEEP | Inject GRANT CREATE public TO PUBLIC before postchecks; baseline false must mismatch. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| lost-public-usage | KEEP | Inject REVOKE USAGE public FROM PUBLIC before postchecks. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| changed-schema-owner | KEEP | Inject ALTER SCHEMA public OWNER TO merlin_d6 before postchecks. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| lost-extension | KEEP | Inject DROP EXTENSION plpython3u before postchecks. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| changed-login | KEEP | Inject ALTER ROLE merlin_d6 NOLOGIN before postchecks. Nonzero exit, named expected refusal text, absence of completion marker; original fingerprint preserved. | Distinct unsafe input or preservation dimension has its own refusal/preservation oracle; another artifact kind or role condition does not substitute. |
| inventory-guard-removal-detected | KEEP | Disable IF EXISTS inventory guard in memory; extra index then reaches DOWN_FINISHED, violating the earlier refusal requirement. Disabled guard must exit 0 and reach DOWN_FINISHED; this violates original extra-index refusal oracle. | Important fault effectiveness proof: prior extra-index refusal becomes admitted when exact responsible guard is disabled. This is stronger than a generic injected postcheck error. |
| other-client-refused | KEEP | Open second client transaction; down must report another database client is connected.  | Real concurrent client/database boundary differs from single-session in-memory input faults. Preserve separate refusal and lock checks. |
| table-lock-blocks-concurrent-insert | KEEP | Hold completed down transaction; another client INSERT times out with SQLSTATE 55P03 at 200ms lock timeout.  | Real concurrent client/database boundary differs from single-session in-memory input faults. Preserve separate refusal and lock checks. |
| wrong-database-refused | KEEP | Connect to postgres database rather than merlin_d6; down refuses unexpected database or cluster.  | Real concurrent client/database boundary differs from single-session in-memory input faults. Preserve separate refusal and lock checks. |

## Pair review index

Every one of 653 pairs has its own decision, classification, rationale, exact fault ID and preserved observed error in the JSON. For compact scanning, the following index lists each case and its fault decisions.

| Case | Fault pair decisions |
|---|---|
| F015-plain | SQL-F001 KEEP INTENDED_ASSERTION_DETECTION |
| F015-emoji | SQL-F001 KEEP INTENDED_ASSERTION_DETECTION |
| F015-family | SQL-F001 KEEP INTENDED_ASSERTION_DETECTION |
| F015-skin | SQL-F001 KEEP INTENDED_ASSERTION_DETECTION |
| F015-flag | SQL-F001 KEEP INTENDED_ASSERTION_DETECTION |
| F015-keycap | SQL-F001 KEEP INTENDED_ASSERTION_DETECTION |
| F015-accent | SQL-F001 KEEP INTENDED_ASSERTION_DETECTION |
| F015-cjk | SQL-F001 KEEP INTENDED_ASSERTION_DETECTION |
| F015-empty | SQL-F002 KEEP INTENDED_ASSERTION_DETECTION |
| limit-title-174 | SQL-F003 IMPROVE OTHER_FIELD_REJECTION |
| limit-title-175 | SQL-F003 IMPROVE OTHER_FIELD_REJECTION |
| limit-title-176 | SQL-F004 KEEP INTENDED_ASSERTION_DETECTION |
| F020 | SQL-F003 IMPROVE OTHER_FIELD_REJECTION |
| draft-title-overflow | SQL-F004 KEEP INTENDED_ASSERTION_DETECTION |
| emoji-title-overflow | SQL-F004 KEEP INTENDED_ASSERTION_DETECTION |
| limit-body-6999 | SQL-F003 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| limit-body-7000 | SQL-F003 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| limit-body-7001 | SQL-F005 KEEP INTENDED_ASSERTION_DETECTION |
| F021 | SQL-F003 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| draft-body-overflow | SQL-F005 KEEP INTENDED_ASSERTION_DETECTION |
| emoji-body-overflow | SQL-F005 KEEP INTENDED_ASSERTION_DETECTION |
| F031 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| F033 | SQL-F007 KEEP INTENDED_ASSERTION_DETECTION |
| F034 | SQL-F008 KEEP INTENDED_ASSERTION_DETECTION |
| F036 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| F037 | SQL-F010 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| F038 | SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| F039 | SQL-F013 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| F040 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| F049-F050 | SQL-F014 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET |
| F051 | SQL-F015 KEEP INTENDED_ASSERTION_DETECTION |
| email-insert-duplicate | SQL-F015 KEEP INTENDED_ASSERTION_DETECTION; SQL-F016 REMOVE UNRELATED_SURVIVAL |
| email-blank | SQL-F017 KEEP INTENDED_ASSERTION_DETECTION; SQL-F016 KEEP INTENDED_ASSERTION_DETECTION |
| email-spaces | SQL-F017 KEEP INTENDED_ASSERTION_DETECTION; SQL-F016 KEEP INTENDED_ASSERTION_DETECTION |
| email-leading | SQL-F017 KEEP INTENDED_ASSERTION_DETECTION; SQL-F016 KEEP INTENDED_ASSERTION_DETECTION |
| email-trailing | SQL-F017 KEEP INTENDED_ASSERTION_DETECTION; SQL-F016 KEEP INTENDED_ASSERTION_DETECTION |
| username-null | SQL-F018 KEEP INTENDED_ASSERTION_DETECTION |
| username-upper | SQL-F019 KEEP INTENDED_ASSERTION_DETECTION |
| username-empty | SQL-F019 KEEP INTENDED_ASSERTION_DETECTION |
| username-twenty-one | SQL-F019 KEEP INTENDED_ASSERTION_DETECTION |
| username-punctuation | SQL-F019 KEEP INTENDED_ASSERTION_DETECTION |
| username-twenty | SQL-F020 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| username-duplicate | SQL-F021 KEEP INTENDED_ASSERTION_DETECTION |
| F059 | SQL-F022 KEEP INTENDED_ASSERTION_DETECTION |
| F061-user | SQL-F023 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| F061-note | SQL-F024 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| uuid-users-version | SQL-F025 KEEP INTENDED_ASSERTION_DETECTION |
| uuid-users-variant | SQL-F025 KEEP INTENDED_ASSERTION_DETECTION |
| uuid-notes-version | SQL-F026 KEEP INTENDED_ASSERTION_DETECTION |
| uuid-notes-variant | SQL-F026 KEEP INTENDED_ASSERTION_DETECTION |
| F064 | SQL-F027 KEEP INTENDED_ASSERTION_DETECTION |
| F065 | SQL-F028 KEEP INTENDED_ASSERTION_DETECTION |
| F066 | SQL-F029 KEEP INTENDED_ASSERTION_DETECTION |
| F067 | SQL-F030 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| F068 | SQL-F031 KEEP INTENDED_ASSERTION_DETECTION |
| F069 | SQL-F031 IMPROVE SECONDARY_GUARD_DIAGNOSTIC_DETECTION |
| F070 | SQL-F031 KEEP INTENDED_ASSERTION_DETECTION |
| F078 | SQL-F031 KEEP INTENDED_ASSERTION_DETECTION |
| F079 | SQL-F031 KEEP INTENDED_ASSERTION_DETECTION |
| F080 | SQL-F031 KEEP INTENDED_ASSERTION_DETECTION |
| F071 | SQL-F032 KEEP INTENDED_ASSERTION_DETECTION |
| F072 | SQL-F032 KEEP INTENDED_ASSERTION_DETECTION |
| F073 | SQL-F032 KEEP INTENDED_ASSERTION_DETECTION |
| F074 | SQL-F032 KEEP INTENDED_ASSERTION_DETECTION |
| F075-role | SQL-F033 KEEP INTENDED_ASSERTION_DETECTION |
| app-column-id | SQL-F034 KEEP SECONDARY_GUARD_DIAGNOSTIC_DETECTION |
| app-column-user_id | SQL-F035 KEEP SECONDARY_GUARD_DIAGNOSTIC_DETECTION |
| app-column-created_at | SQL-F036 KEEP SECONDARY_GUARD_DIAGNOSTIC_DETECTION |
| app-column-updated_at | SQL-F037 KEEP INTENDED_ASSERTION_DETECTION |
| app-column-blank_body_expires_at | SQL-F038 KEEP INTENDED_ASSERTION_DETECTION |
| app-own-edit | SQL-F039 KEEP INTENDED_ASSERTION_DETECTION |
| app-saved-delete | SQL-F040 KEEP INTENDED_ASSERTION_DETECTION |
| app-blank-draft-delete | SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| F076 | SQL-F042 KEEP INTENDED_ASSERTION_DETECTION |
| F077 | SQL-F042 KEEP INTENDED_ASSERTION_DETECTION |
| F081 | SQL-F043 REMOVE UNRELATED_SURVIVAL; SQL-F044 KEEP INTENDED_ASSERTION_DETECTION |
| F082 | SQL-F043 KEEP INTENDED_ASSERTION_DETECTION; SQL-F044 REMOVE UNRELATED_SURVIVAL |
| F083 | SQL-F043 KEEP INTENDED_ASSERTION_DETECTION; SQL-F044 REMOVE UNRELATED_SURVIVAL |
| F084 | SQL-F043 KEEP INTENDED_ASSERTION_DETECTION; SQL-F044 REMOVE UNRELATED_SURVIVAL |
| F085 | SQL-F043 KEEP INTENDED_ASSERTION_DETECTION; SQL-F044 REMOVE UNRELATED_SURVIVAL |
| F086 | SQL-F045 KEEP INTENDED_ASSERTION_DETECTION |
| F087 | SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| F088 | SQL-F046 KEEP INTENDED_ASSERTION_DETECTION |
| F089 | SQL-F047 KEEP INTENDED_ASSERTION_DETECTION |
| F090 | SQL-F043 KEEP INTENDED_ASSERTION_DETECTION; SQL-F044 REMOVE UNRELATED_SURVIVAL |
| F092 | SQL-F010 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| F093 | SQL-F048 KEEP INTENDED_VALID_BEHAVIOR_REJECTION; SQL-F011 REMOVE UNRELATED_SURVIVAL; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| F094 | SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| F095 | SQL-F011 REMOVE UNRELATED_SURVIVAL; SQL-F012 KEEP INTENDED_ASSERTION_DETECTION |
| F096 | SQL-F011 REMOVE UNRELATED_SURVIVAL; SQL-F012 KEEP INTENDED_ASSERTION_DETECTION |
| F097 | SQL-F011 REMOVE UNRELATED_SURVIVAL; SQL-F012 KEEP INTENDED_ASSERTION_DETECTION |
| F098 | SQL-F011 REMOVE UNRELATED_SURVIVAL; SQL-F012 KEEP INTENDED_ASSERTION_DETECTION |
| F099 | SQL-F049 KEEP INTENDED_ASSERTION_DETECTION |
| F100 | SQL-F050 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| F102 | SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| F103 | SQL-F050 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| F104 | SQL-F050 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| F106 | SQL-F046 KEEP INTENDED_ASSERTION_DETECTION |
| F107 | SQL-F046 KEEP INTENDED_ASSERTION_DETECTION |
| F108 | SQL-F046 KEEP INTENDED_ASSERTION_DETECTION |
| F109 | SQL-F052 KEEP INTENDED_ASSERTION_DETECTION |
| F110 | SQL-F053 KEEP INTENDED_ASSERTION_DETECTION |
| F112 | SQL-F046 KEEP INTENDED_ASSERTION_DETECTION |
| F113 | SQL-F054 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| F115 | SQL-F054 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| purge-overdue | SQL-F055 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| F116 | SQL-F046 KEEP INTENDED_ASSERTION_DETECTION |
| F117 | SQL-F046 KEEP INTENDED_ASSERTION_DETECTION |
| F118 | SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| sql-batch-cleanup_expired_blank_notes-NULL | SQL-F051 KEEP INTENDED_ASSERTION_DETECTION |
| sql-batch-cleanup_expired_blank_notes-0 | SQL-F051 KEEP INTENDED_ASSERTION_DETECTION |
| sql-batch-cleanup_expired_blank_notes-1001 | SQL-F051 KEEP INTENDED_ASSERTION_DETECTION |
| sql-batch-purge_deleted_notes-NULL | SQL-F055 KEEP INTENDED_ASSERTION_DETECTION |
| sql-batch-purge_deleted_notes-0 | SQL-F055 KEEP INTENDED_ASSERTION_DETECTION |
| sql-batch-purge_deleted_notes-1001 | SQL-F055 KEEP INTENDED_ASSERTION_DETECTION |
| maintenance-fresh-delete | SQL-F056 KEEP INTENDED_ASSERTION_DETECTION |
| maintenance-active-read | SQL-F057 KEEP INTENDED_ASSERTION_DETECTION |
| maintenance-overdue-purge | SQL-F055 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| maintenance-expiry | SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| F045-nbsp | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| F053-nbsp | SQL-F017 KEEP INTENDED_ASSERTION_DETECTION; SQL-F016 KEEP INTENDED_ASSERTION_DETECTION |
| F091 | SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| F101 | SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| F114 | SQL-F055 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| app-own-insert | SQL-F039 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| app-crossuser-delete | SQL-F032 KEEP INTENDED_ASSERTION_DETECTION |
| app-unset-actor | SQL-F032 KEEP INTENDED_ASSERTION_DETECTION |
| app-active-view | SQL-F032 KEEP INTENDED_ASSERTION_DETECTION |
| required-body | SQL-F058 KEEP INTENDED_ASSERTION_DETECTION |
| required-device_created_at | SQL-F059 KEEP INTENDED_ASSERTION_DETECTION |
| required-is_draft | SQL-F060 KEEP INTENDED_ASSERTION_DETECTION |
| permission-groups | SQL-F061 KEEP INTENDED_ASSERTION_DETECTION |
| rls-forced | SQL-F062 KEEP INTENDED_ASSERTION_DETECTION |
| app-no-cleanup-grant | SQL-F063 KEEP INTENDED_ASSERTION_DETECTION; SQL-F051 REMOVE UNRELATED_SURVIVAL |
| app-no-schema-create | SQL-F064 KEEP INTENDED_ASSERTION_DETECTION |
| index-created | SQL-F065 KEEP INTENDED_ASSERTION_DETECTION |
| index-edited | SQL-F066 KEEP INTENDED_ASSERTION_DETECTION |
| index-device | SQL-F067 KEEP INTENDED_ASSERTION_DETECTION |
| index-draft | SQL-F068 KEEP INTENDED_ASSERTION_DETECTION |
| app-delete-account-cascade | SQL-F030 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| sql-valid-batch-cleanup_expired_blank_notes-1 | SQL-F050 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| sql-valid-batch-cleanup_expired_blank_notes-1000 | SQL-F050 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| sql-valid-batch-purge_deleted_notes-1 | SQL-F054 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| sql-valid-batch-purge_deleted_notes-1000 | SQL-F054 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| expiry-batch-one | SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| purge-batch-one | SQL-F055 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| note-body-default | SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| user-id-duplicate | SQL-F069 KEEP INTENDED_ASSERTION_DETECTION |
| user-clock-forged | SQL-F042 KEEP INTENDED_ASSERTION_DETECTION |
| unicode-blank-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| unicode-blank-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| unicode-email-padding-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| unicode-email-padding-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| unicode-blank-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+0009 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+000A | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+000B | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+000C | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+000D | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+001C | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+001D | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+001E | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+001F | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+0020 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+0085 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+1680 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2000 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2001 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2002 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2003 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2004 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2005 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2006 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2007 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2008 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2009 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+200A | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2028 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+2029 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+202F | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+205F | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| blank-body-U+3000 | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F009 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0009-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0009-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+0009-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0009-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0009-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0009-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0009-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+000A-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000A-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+000A-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000A-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000A-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000A-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000A-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+000B-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000B-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+000B-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000B-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000B-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000B-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000B-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+000C-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000C-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+000C-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000C-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000C-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000C-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000C-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+000D-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000D-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+000D-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000D-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000D-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000D-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+000D-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+001C-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001C-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+001C-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001C-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001C-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001C-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001C-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+001D-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001D-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+001D-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001D-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001D-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001D-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001D-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+001E-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001E-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+001E-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001E-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001E-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001E-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001E-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+001F-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001F-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+001F-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001F-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001F-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001F-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+001F-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+0020-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0020-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+0020-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0020-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0020-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0020-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0020-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+0085-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0085-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+0085-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0085-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0085-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0085-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+0085-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+00A0-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+00A0-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+00A0-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+00A0-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+00A0-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+00A0-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+00A0-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+1680-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+1680-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+1680-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+1680-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+1680-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+1680-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+1680-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2000-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2000-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2000-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2000-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2000-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2000-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2000-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2001-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2001-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2001-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2001-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2001-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2001-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2001-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2002-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2002-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2002-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2002-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2002-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2002-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2002-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2003-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2003-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2003-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2003-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2003-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2003-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2003-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2004-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2004-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2004-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2004-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2004-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2004-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2004-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2005-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2005-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2005-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2005-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2005-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2005-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2005-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2006-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2006-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2006-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2006-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2006-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2006-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2006-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2007-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2007-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2007-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2007-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2007-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2007-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2007-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2008-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2008-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2008-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2008-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2008-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2008-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2008-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2009-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2009-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2009-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2009-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2009-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2009-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2009-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+200A-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+200A-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+200A-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+200A-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+200A-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+200A-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+200A-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2028-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2028-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2028-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2028-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2028-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2028-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2028-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+2029-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2029-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+2029-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2029-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2029-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2029-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+2029-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+202F-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+202F-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+202F-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+202F-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+202F-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+202F-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+202F-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+205F-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+205F-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+205F-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+205F-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+205F-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+205F-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+205F-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-U+3000-title | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+3000-countdown | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F011 KEEP INTENDED_ASSERTION_DETECTION; SQL-F012 REMOVE UNRELATED_SURVIVAL |
| parity-U+3000-email-leading | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+3000-email-trailing | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+3000-email-blank | SQL-F016 KEEP INTENDED_ASSERTION_DETECTION; SQL-F017 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+3000-draft-delete | SQL-F006 KEEP INTENDED_ASSERTION_DETECTION; SQL-F041 KEEP INTENDED_ASSERTION_DETECTION |
| parity-U+3000-maintenance | SQL-F006 IMPROVE FIXTURE_FAILURE_BEFORE_TARGET; SQL-F051 IMPROVE SYNTHETIC_RETURN_OR_SIDE_EFFECT_STUB |
| parity-nonwhitespace-U+200B | SQL-F070 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| parity-nonwhitespace-U+FEFF | SQL-F070 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| parity-nonwhitespace-U+2060 | SQL-F070 KEEP INTENDED_VALID_BEHAVIOR_REJECTION |
| test_failed_second_write_rolls_back_first_write_after_reconnect | SQL-F071 IMPROVE PRE_RECONNECT_ASSERTION_DETECTION |

## Evidence and limitations

Source hashes and evidence hashes are recorded in JSON. Archived SQL source hash differs from current source; latest supplied report matches current source. Case IDs match in order, and current review uses latest diagnostics. Source rows preserve original baseline results and fault stderr. Existing evidence under docs/testing/case-effectiveness-evidence remains untouched.

- No new runtime evidence collected. Green baseline and gross fault detection do not prove absence of defects.
- The four unrelated Python invalid import harness faults are outside this review.
- Many same-kill-set SQL mutations replace whole helpers with constants; these do not prove the Unicode input matrix redundant.
- Migration gate tests do not include cross-database role dependency, existing snapshot refusal, every administrative flag, every missing function, or malformed baseline-source types. These are review coverage gaps, not claims of demonstrated defects.
- Migration artifact inventory verifies names/counts, not full definitions before removal. A changed expression under an expected name is not among these tests.
- SQL app actor setting proves owner policy enforcement, not authenticated API identity; preserve independent Python and future HTTP/authentication layers.

A recommendation to merge applies only after preserving every input/property/assertion and exact diagnostic in its named successor. This review authorizes no deletion or implementation change.
