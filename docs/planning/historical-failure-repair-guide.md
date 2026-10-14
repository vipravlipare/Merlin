# Fix the three observed failures

**Historical repair instructions, superseded October 11, 2026.** The user subsequently authorized responsible code fixes. See the [test-hardening and repair report](../testing/test-hardening-and-repairs.md) for actual changes and verification, including a fourth maintenance-identity defect. Migration 002 was applied to the disposable Day 6 database; do not repeat these application instructions or rerun applied migrations.

These are learner implementation steps, not completed fixes. Saved audit results show 14 database failures, one probe failure and one quiz failure. Keep the existing assertions. Do not turn an unexpected rejection, exception or skipped test into a pass.

## 1. Handle database probe errors safely

File: `app/database_connectivity_probe.py`.

The current handler catches only `psycopg.OperationalError`. Query failures can raise `psycopg.ProgrammingError` instead.

- Change the database-error handler to catch the common `psycopg.Error` base class.
- Keep exit status 1 and a short generic stderr message beginning `DB Probe Failed:`. Explain that connection or query failed.
- Do not print the exception, password or connection string. Remove the unused exception variable.
- Keep the connection context manager and read-only setting before the query. Do not catch every Python exception: unrelated programming bugs should remain visible.

Run from the Ubuntu checkout:

`uv run --locked pytest -q tests/test_database_connectivity_probe.py`

Expected: all four cases pass. The tests mock the connection, so they do not modify PostgreSQL.

## 2. Use the same whitespace definition in Python and PostgreSQL

File: `migrations/001_users_notes.up.sql` describes the original schema. Its POSIX `[[:space:]]` expressions do not match Python's whitespace definition. Changing this file alone does not change functions, constraints or policies already installed in PostgreSQL.

Keep the agreed rule: whitespace-only text is empty. Preserve whitespace in real note text.

Design two database helpers using the existing PL/Python facility:

- An empty-text predicate: NULL is empty; otherwise text is empty when Python `strip()` leaves no characters. Always return a boolean.
- An email-cleanliness predicate: NULL is allowed; otherwise text must contain non-whitespace content and equal its stripped form. Do not lowercase or change the stored display address.

Use these consistently in every location below. For a content requirement, use the inverse of the empty-text predicate.

| Location | Required behavior |
|---|---|
| `users_email_clean` | Reject blank or padded stored email; allow NULL. |
| `notes_title_nonblank` | Allow NULL or a real title. |
| `notes_has_content` | Saved notes need a real title or real body; drafts may be empty. |
| `notes_deadline_matches_body` | Saved empty bodies need a deadline; drafts and nonempty bodies have none. |
| `manage_note_content` | Normalize empty title to NULL and use the same body test for starting, preserving and clearing deadlines. |
| Blank-draft DELETE policy | Allow the intended owner to delete a draft with empty title and body, including Unicode whitespace. |
| Cleanup function and maintenance policy | Find expired empty bodies using exactly the same predicate. |

Find all sites with:

`rg -n '\[:space:\]' migrations/001_users_notes.up.sql`

Give helpers the intended owner and only the execution permissions needed by the existing roles. Keep their schema-qualified names and existing ownership restrictions.

Because migration 001 has already been applied, prepare a separate repair migration. In one transaction, add the helpers and replace the affected constraints, trigger function, cleanup function and policies. Review the installed definitions against the repair; updating comments is not a schema repair. Check existing isolated rows before validating stronger constraints; do not silently delete data to make validation succeed.

Do not rerun migration 001. Do not apply any repair to Sprint 0. Review the repair and prove the Day 6 target identity before applying it: database `merlin_d6`, cluster `7694311451826794534`, port 55432. The preserved Sprint 0 cluster is `7691749973399031842`.

After applying the reviewed repair only on Day 6, run:

`MERLIN_RUN_DB_TESTS=1 uv run --locked pytest -q tests/test_users_notes_database.py`

Expected: all 183 database cases pass. This suite requires empty isolated tables at its initial safety gate and rolls back its synthetic rows. A failed gate is a blocker, not permission to reset storage. Also run `uv run --locked pytest -q tests/test_note_rules_and_maintenance.py` to preserve Python behavior.

## 3. Reject malformed quiz answer storage

File: `quizzes/sprint-0-quiz.html`, function `validSaved`.

The check for an object accepts arrays. Answers are keyed by question ID. Assigning an answer to array index 1 creates an unused index 0; JSON saves that gap as NULL. The next validation rejects it and progress disappears.

- Require `saved.answers` to be a non-null object and not an array.
- Keep the existing answer-value checks and question/order checks.
- Keep accepting an empty answers object for a session with no answered questions.
- Do not reject order arrays solely to satisfy a new restriction: the audit found no equivalent persistence defect there.

Run `pnpm test` from the checkout. Expected: all 35 cases pass. Then manually answer a question, reload and confirm that progress remains. The automated JSON round-trip check does not replace browser verification.

## Finish and record evidence

Run `uv run --locked pytest -q`, then `uv run --locked python tools/check_mutations.py`. The default pytest command skips the opt-in database cases; record the separate database run too. The mutation checker covers 55 specific injected Python faults, not every possible defect.

Record actual results and the first failure. No repairs or fresh test runs have been performed by writing this guide. Actual learner minutes remain unknown; all repair work consumes the existing Day 6 budget, with DSA and AWS deferred.
