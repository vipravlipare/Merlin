# Day 6 — implemented draft rules

This document now lists only mechanisms already written. It replaces the previous accumulated design and future-rule list at the learner's request. “Written” does not mean applied, tested in PostgreSQL or production-ready.

## Users

| Field | Stored type | Written rule |
|---|---|---|
| ID | UUID | Generated UUIDv4, unique primary key, cannot change. |
| Username | TEXT | Required; 1–20 lowercase ASCII letters, digits or underscores; unique. |
| Canonical username | TEXT | Generated from lowercase username; indexed for lookup. |
| Email | TEXT | Optional; preserve display casing; reject blank/edge-whitespace storage; unique when compared lowercase. |
| Creation/update times | TIMESTAMPTZ | Database chooses server time; creation time cannot change. |

The Python email helper trims surrounding whitespace and maps blank input to None. It does not verify email ownership.

## Notes

| Field | Stored type | Written rule |
|---|---|---|
| ID | UUID | Independent generated UUIDv4, unique primary key, cannot change. |
| Owner | UUID | Required existing user; cannot change; deleting the account permanently removes its notes. |
| Title | TEXT | Optional, non-unique; whitespace-only becomes NULL; weighted limit 175. |
| Body | TEXT | Empty text allowed when a title exists; preserve writing whitespace; weighted limit 7,000. |
| Server creation/update times | TIMESTAMPTZ | Database chooses time; creation is fixed; only title/body edits change Last Edited. |
| Device creation/edit times | TIMESTAMPTZ | Required device metadata; initial edit equals device creation; device creation is fixed. These are not trusted security clocks. |
| Blank-body expiry | TIMESTAMPTZ | Database controls the 24-hour title-only countdown; submitted deadlines are overridden. |
| Deleted time | TIMESTAMPTZ | NULL means active; database chooses the first trash time and preserves it on repeated hiding. |
| Draft flag | BOOLEAN | Default false; blank drafts allowed; draft may become saved, but saved cannot become draft. |

Saved rows must contain a real title or body. A database rejection does not delete a row. The Python helper returns delete_on_save for a blank non-draft note; the helper itself does not write or delete anything.

## Counting and deadlines

Each displayed emoji sequence recognized by pinned emoji2.16.0 counts as 4. Every other grapheme counts as 1. Pinned regex2026.9.29 splits the displayed characters. Python validation and the migration's PL/Python helper use the same rule.

A saved title-only note starts a 24-hour countdown. Body content cancels it. Clearing body content starts a new countdown. Repeated blank saves preserve the existing deadline. Automatic expiry moves the note to trash. Restore is refused at or after 14 days; restoring a title-only note starts a fresh 24-hour countdown. Hiding or restoring alone preserves Last Edited. A note that remains in trash cannot have its text/draft state edited.

## Storage access and maintenance

Indexes support creation/update/device-edit timelines, draft lists, expiry and trash purge. active_notes is a security-invoker view that excludes trash. Owner RLS checks the transaction's merlin.actor_id setting; this is conditional database access control, not implemented authentication. Administrators can bypass it.

The draft defines separate NOLOGIN owner/application/maintenance permission groups. Application grants exclude protected clocks, IDs and owner changes. Direct note deletion is limited to blank drafts. Maintenance visibility is limited to due expiry rows/trash, and deletion is limited to trash at least 14 days old. Maintenance functions have no PUBLIC execution permission.

Both maintenance functions process bounded batches and skip locked rows. The foreground scheduler prompts for a password, verifies the known disposable cluster before writes, uses transaction/timeouts and runs once or every 60 seconds. It has not been started or installed as a service. It uses the disposable administrative connection; that does not prove limited-role behavior.

## Files to review

- [ ] [Input rules](../../app/note_rules.py): text counting, normalization and blank-save decision.
- [ ] [Migration](../../migrations/001_users_notes.up.sql): tables, checks, clocks, trash, grants and maintenance functions.
- [ ] [Maintenance](../../app/notes_maintenance.py): target guard and scheduled cycles.
- [ ] [Unit tests](../../tests/test_note_rules_and_maintenance.py): real helper checks and simulated database responses.

📚 Learn first: read each linked file's short comments. [Four-file review checklist](../checklists/database-code-review-checklist.md).
↩ Return: explain what each file does before running database changes.

## Prerequisites and observed results

The migration requires plpython3u already installed in the disposable database and both pinned packages available to the server's Python runtime. The application virtual environment does not supply them. Preflight refuses missing prerequisites. No extension or Docker changes were made.

Previously observed: 18 Python/mock unit cases passed and 10 embedded-validator comparisons agreed. SQL was not applied or database-tested. The scheduler remains stopped. These observations do not establish deletion, restore, constraints or ordinary-role security in PostgreSQL. No down migration exists.

Exact next action: verify disposable-server PL/Python/package availability read-only, then review this draft before any isolated migration attempt. Preserve Sprint 0 volume merlin_postgres_data and cluster7691749973399031842. No commit/push/upload. Day 6 remains capped at 360 minutes; actual minutes are unknown. DSA/AWS remain deferred.
