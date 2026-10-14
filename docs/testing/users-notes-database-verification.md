# Verify the database foundation — 39 minutes

## Start here

A passing Python test proves the Python behavior it actually exercises. It does not prove a SQL constraint, deletion, permission or database rollback. No mocked response is accepted as database evidence.

**Observed October 10:** disposable project is healthy at loopback55432. Its database is merlin_d6 and cluster is 7694311451826794534. Read-only inspection found no available plpython3u extension and no Users/Notes tables. The migration has not run. The first blocker is therefore PL/Python availability; database cases below are PENDING, not failed constraints or passes. The down migration is also missing.

Do not repeat Sprint 0 setup or use its database. Never modify volume merlin_postgres_data/cluster7691749973399031842. No extension installation, migration or maintenance was run during this review.

## Your 39-minute order

| Minutes | Work |
|---|---|
| 5 | Confirm the target and prerequisites; stop database attempts if blocked. |
| 8 | Run/read the helper tests; explain one accepted and one rejected boundary. |
| 12 | If prerequisites pass, valid/invalid records and constraints. Otherwise review the expected cases and record PENDING. |
| 7 | If ready, transaction rollback/reconnect evidence. Otherwise record PENDING. |
| 4 | If reviewed down file exists, undo/reapply only in disposable storage. Otherwise record PENDING. |
| 3 | Record first blocker/failure, actual results, minutes and exact next action. |
| **39** | Stop at the cap; unfinished cases move to later feature time. |

This agenda cannot guarantee execution of every case below. The matrix is the complete regression target; report which cases you actually ran.

📚 Learn first: [pytest assertions](https://docs.pytest.org/en/stable/how-to/assert.html) and [Psycopg transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html), verified October 10, 2026. The online Psycopg page may describe a newer patch release; local package remains3.3.6.
↩ Return: run the Python suite first; database cases require the gate below.

## 1. Run the real helper tests

In the Ubuntu terminal at /home/vipra/Merlin:

```bash
uv run --locked --no-sync python -m pytest tests/test_note_rules_and_maintenance.py -v
```

The manually reviewed suite now has 90 cases, with 82 passing and 8 failing on batch/draft input-type checks. See [individual current-case review](notes-unit-test-deep-audit.md). Comments state the purpose and limits of each group. Expected answers are fixed independently: title175 accepted/176 rejected; body7000 accepted/7001 rejected; a family emoji counts4. Invalid inputs must raise the correct error, not merely any error. Boundary tests also run through validate_note, so a correct counting helper cannot hide a missing limit check.

Covered: plain/combined emoji, flags/skin tones/keycaps, combining accents, control/whitespace graphemes, limits below/at/above, draft length rejection, blank save/draft differences, unchanged actual text, email normalization, invalid text/NUL, refused cluster/database, invalid batch before connection, allowed batch extremes and simulated failure propagation. The worker cases replace the connector: they prove refusal and call/control-flow behavior only. They do not establish SQL commit/rollback or successful purge.

Observed latest assistant result: **82 PASS, 8 FAIL**. Wrong batch/draft input types expose validation gaps; see the deep review. Your result and learning check remain unrecorded. Do not check learning complete merely because the suite passes.

## 2. Database gate — read only

Run only the explicit disposable project command below. Do not substitute a default project.

```bash
 docker compose -p merlin-d6-20261008105707 exec -T postgres psql -X -U merlin_d6 -d merlin_d6 -P pager=off -c "SELECT current_database(), system_identifier FROM pg_control_system(); SELECT name, installed_version FROM pg_available_extensions WHERE name = 'plpython3u'; SELECT to_regclass('public.users'), to_regclass('public.notes');"
```

An empty extension result means this image cannot currently install that extension. Even an available/installed extension does not prove its server Python has emoji2.16.0 and regex2026.9.29. Local .venv packages do not satisfy that prerequisite. Prepare an isolated server-runtime change for review separately; do not apply the migration now.

After the extension/runtime gate passes, review the migration and role names, then personally attempt it as a single transaction with ON_ERROR_STOP on this disposable target. Do not reuse historical schema insert examples: usernames and device creation time are required. If it fails, record the first error and confirm rollback rather than rerunning partial CREATE statements.

📚 Learn first: [Migration](../../migrations/001_users_notes.up.sql) comments, especially its preflight.
↩ Return: get the prerequisite result before writing any database fixture.

## 3. Precise database cases — all currently PENDING

Use synthetic owners A/B and distinct UUIDs/usernames/emails. Start every rejection case with otherwise-valid input, change only the named value, and check the exact violated constraint/SQLSTATE. If an unrelated required field fails first, the intended case was not exercised. Use savepoints or fresh transactions after expected errors; an aborted transaction cannot run further useful checks.

A valid note fixture supplies an existing user_id, real title/body as appropriate, required device_created_at, and defaults for server-managed fields. A contentful fixture has NULL expiry. Do not trust a supplied deleted_at or deadline as test fixture setup: triggers override them. For elapsed-time tests use isolated, reviewed privileged fixture setup that explicitly restores/re-enables protections before calling the real operation. Waiting 14 days or testing a fake Python copy of the SQL is not required and is not equivalent evidence.

| ID | Input/action | Exact expected observation |
|---|---|---|
| U01 | Insert two valid users, omit IDs | Distinct UUIDv4 IDs; required names/canonical/server times stored. |
| U02 | Explicit valid UUIDv4; duplicate ID; UUIDv7/nil UUID | First accepted; duplicate23505; wrong version CHECK23514. |
| U03 | Username lengths1/20/21; empty; uppercase; spaces; Unicode letter | 1/20 accepted; other values users_username_format23514. |
| U04 | Duplicate username | users_username_unique23505; original unchanged. |
| U05 | Omit/NULL username | NOT NULL23502; no inserted row. |
| U06 | Supply canonical column directly | Generated-column write rejected; generation from username remains correct. |
| U07 | Rename username to valid unused name | Canonical follows; creation fixed; update server time changes. |
| E01 | Distinct mixed-case stored emails | Original casing survives. |
| E02 | Same email exact/case variant | users_email_unique23505 for each; no duplicate row. |
| E03 | NULL email on two users | Both accepted. |
| E04 | Empty/spaces/tab/newline/padded email | users_email_clean23514 for each direct write. |
| E05 | Change an email to another account's case variant | Rejected; both original emails unchanged. |
| N01 | Real title/body; body-only; title-only | Accepted; only title-only has expiry. |
| N02 | Identical text/titles with distinct note IDs | Both accepted; no accidental title uniqueness. |
| N03 | Omit/NULL owner; nonexistent owner | Required23502 or FK23503, matching actual defect. |
| N04 | Explicit duplicate/wrong-version note IDs | Primary-key23505/version CHECK23514. |
| N05 | Blank/whitespace title with real body | Stored NULL title; body whitespace unchanged. |
| N06 | Both fields blank: saved versus draft | Saved notes_has_content23514; draft accepted. |
| N07 | NULL body directly; omitted body with title | NULL23502; omitted body stored empty text. |
| N08 | Body containing spaces/newlines plus real text | Exact stored content retained after reconnect. |
| L01 | Title plain lengths174/175/176 | First two accepted;176 notes_title_limit23514. |
| L02 | Title43family emoji +3/4 letters | Weighted175 accepted/176 notes_title_limit23514. |
| L03 | Body6999/7000/7001 ordinary characters | First two accepted;7001 notes_body_limit23514. |
| L04 | Body1750/1751 emoji | Weighted7000 accepted/7004 notes_body_limit23514. |
| L05 | Over-limit title/body on UPDATE and drafts | Same respective constraints reject; prior row unchanged. |
| L06 | Accents/flags/keycaps/skin tones through direct SQL | Database count matches the independently specified Python case values. |
| T01 | Insert client-supplied server times | Trigger chooses server times; initially creation=update. |
| T02 | Content edit with earlier device time | Accepted device metadata; server update remains server-based; creation fixed. |
| T03 | No-op update/read/hide/restore | Each alone preserves both Last Edited values. |
| T04 | Change user/note ID, server creation, device creation, owner separately | Each protected change23514 or column-permission42501; original intact. |
| T05 | Text edit | Server edit time changes; supplied device edit time stored; fresh-time submission is not proven by SQL. |
| D01 | Title-only first insert; repeated blank save | First expiry approximately server now+24h; repeated save exact same deadline. |
| D02 | Add body; clear it later; repeat blank save | NULL deadline; fresh24h deadline; repeated save preserves it. |
| D03 | Submit past/future/NULL deadlines during each transition | Trigger chooses/preserves the correct value; supplied clock has no effect. |
| D04 | Blank draft then publish with title | Draft expiryNULL; published expiry24h. |
| D05 | Saved note changed back to draft | Rejected23514; existing countdown retained. |
| X01 | Hide active note with chosen past/future deletion time | Server deletion time stored; edit times retained. |
| X02 | Hide same note again with altered clock | First deletion time retained;14daywindow not extended. |
| X03 | New note starts deleted | Rejected by deletion guard when otherwise valid. |
| X04 | Restore before/exactly at/after14days | Before accepted; exact/after23514; no late resurrection. |
| X05 | Restore title-only note | Fresh24h deadline; original Last Edited preserved. |
| X06 | Edit text/draft while still trashed | Rejected23514; restore first. |
| X07 | Normal view versus owner trash query | active_notes excludes trash; own raw rows accessible under actor; other owner not visible. |
| M01 | Due/future title-only rows and contentful/draft rows | Expiry changes only due title-only rows to trash; correct changed-row count. |
| M02 | Trash just younger/exactly14days/older; active row | Purge retains younger/active; deletes exact/older; correct count. |
| M03 | Batch1/1000 and0/1001/NULL | Valid bounds cap work; invalid rejected before writes. |
| M04 | Lock candidate in session1; maintenance in session2 | Locked row skipped; other eligible rows processed; later cycle processes released row. |
| M05 | Concurrent content edit/expiry; restore/purge | No contentful row wrongly expired and no missing row resurrected; one consistent committed outcome. |
| A01 | A actor selects/inserts/updates B owner as limited app role | No B rows exposed/changed; unauthorized write rejected42501 where appropriate. Admin evidence does not count. |
| A02 | Missing actor | No owner rows visible; writes rejected; no default user assumed. |
| A03 | App tries table alteration/trigger disable/protected-column update/maintenance call | Permission42501; protections remain installed. |
| A04 | App DELETE saved/contentful draft versus blank draft | Saved/contentful retained; own blank draft removed. |
| A05 | Maintenance direct DELETE active/unexpired trash versus expired trash | First two retained; expired eligible only. |
| A06 | Account A deletion | A notes cascade, including trash; B notes remain. |
| I01 | Query one user timeline and draft lists | Correct owner/order/id tie-break; index exists with expected key. Do not force index use on tiny data. |

📚 Learn first: [Current implemented rules](../architecture/users-notes-design.md).
↩ Return: choose N01/E02/N03/L01 first after the gate passes; record actual returned data and exact errors.

## 4. Transaction and migration evidence

| ID | Action | Expected observation | Current result |
|---|---|---|---|
| R01 | One transaction: insert synthetic user, then deliberately fail note FK; roll back | New connection sees neither uncommitted user nor note; pre-existing sentinel unchanged | PENDING |
| R02 | One transaction: valid user/note and commit; close/reconnect | Fresh connection sees exact committed IDs/text | PENDING |
| R03 | Expected constraint error with savepoint rollback | Can run subsequent valid query; failed row absent | PENDING |
| R04 | Reviewed down migration then catalog inspection | Only owned migration objects removed; unrelated sentinel/extension preserved | PENDING; down file missing |
| R05 | Reapply reviewed up migration in disposable storage | Same tables/constraints/grants recreated; run representative cases again | PENDING |

Roles are cluster-wide. Undo must account for newly created roles, function signatures, view and original schema privileges; never drop pre-existing roles/extensions or unrelated objects. Do not invent a broad CASCADE reset to make reapplication pass.

Cross-user database denial requires tests using the limited role and verified actor handling. End-to-end authorization stays PENDING while no authenticated application boundary exists, even if limited-role SQL cases later pass.

📚 Learn first: [Psycopg transaction contexts](https://www.psycopg.org/psycopg3/docs/basic/transactions.html).
↩ Return: explain why the first user insert must vanish after the second write fails.

## Evidence ledger

| Scope | Result | Evidence |
|---|---|---|
| Reviewed Python tests |82PASS/8FAIL| Batch/draft runtime type-validation gaps; helper/worker-mock evidence only |
| Disposable identity/container | PASS | healthy; merlin_d6; cluster7694311451826794534 |
| Extension availability gate | FAIL | pg_available_extensions returned zero rows for plpython3u |
| Migration/tables/SQL cases | PENDING | No Users/Notes tables; no SQL changes attempted |
| Undo/reapplication | PENDING | Missing down migration |
| Cross-user end-to-end denial | PENDING | No authenticated application boundary |
| Actual minutes/learner explain-back | Unknown/not observed | Do not infer completion |

Record each executed case as ID, expected, observed, PASS/FAIL/PENDING and exact first error. A rejection from the wrong constraint is not a pass. First database blocker: missing PL/Python; first new unit failure: boolean batch reaches connector. Exact next action: review/fix integer-only batch validation and rerun focused tests, then inspect a disposable-server PL/Python/runtime setup plan; do not run the current up migration yet. No extra hours are assumed.
