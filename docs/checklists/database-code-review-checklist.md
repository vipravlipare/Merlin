# Day 6: read these four files

Check a box only after you can explain that part in your own words. Reading code does not prove it works in PostgreSQL. This review uses the existing Day 6 time budget; actual minutes are still unknown.

## 1. Input rules

📚 Learn first: read [note_rules.py](../../app/note_rules.py), top to bottom.

- [ ] Explain a displayed character and why a family emoji counts as 4, not as its separate Unicode parts.
- [ ] Find the title limit of 175 and body limit of 7,000.
- [ ] Explain why blank titles become None, but actual body whitespace stays.
- [ ] Explain why email display casing stays and uniqueness is checked separately by SQL.
- [ ] Explain delete_on_save: it tells a future caller to delete; this helper does not delete anything.

↩ Return: identify which future save operation must call validate_note before writing. No API integrates it yet; direct SQL bypasses weighted limits.

## 2. Database rules

📚 Learn first: read [001_users_notes.up.sql](../../migrations/001_users_notes.up.sql), in sections: tables, indexes, triggers, policies, cleanup functions.

- [ ] Find UUIDv4 generation, required fields, username/email uniqueness and the owner foreign key.
- [ ] Explain account deletion versus soft deletion: account deletion permanently removes notes; deleted_at marks a note for later purge.
- [ ] Explain saved-note rejection versus blank-draft acceptance.
- [ ] Explain server timestamps versus device timestamps; identify fields that cannot change.
- [ ] Trace title-only expiry: first save starts 24 hours, content cancels it, clearing content restarts it, repeated blank saves preserve it.
- [ ] Explain each index's query purpose; an index is not a rate limiter.
- [ ] Explain owner policies and why a privileged administrator does not prove ordinary-user restrictions.
- [ ] Explain bounded cleanup, locked rows, 30-day purge and explicit function permissions.

↩ Return: list pending database acceptance tests. This migration is unapplied; do not run it on Sprint 0 storage. The down migration remains deferred.

## 3. Maintenance process

📚 Learn first: read [notes_maintenance.py](../../app/notes_maintenance.py).

- [ ] Find the fixed disposable target and expected cluster fingerprint.
- [ ] Explain why fingerprint verification must happen before cleanup.
- [ ] Explain transaction commit/rollback, batch size and query timeouts.
- [ ] Explain password prompting and bound SQL parameters.
- [ ] Explain --once, the default 60-second interval and stopping with Ctrl+C.

↩ Return: keep the scheduler stopped until disposable migration, permissions and cleanup tests pass. This is a foreground development worker, not a deployed production service.

## 4. Evidence

📚 Learn first: read [test_note_rules_and_maintenance.py](../../tests/test_note_rules_and_maintenance.py).

- [ ] Explain the accepted boundary and the first rejected value for each text limit.
- [ ] Explain what pytest.raises checks.
- [ ] Explain MagicMock and patch: database responses are simulated, not measured.
- [ ] Find the test proving a wrong cluster cannot reach cleanup calls.
- [ ] Run the unit suite from the Ubuntu repository root:

```bash
uv run python -m pytest tests/test_note_rules_and_maintenance.py -q
```

- [ ] Record your actual output and minutes; do not copy the assistant's result as your own.

↩ Return: assistant observed 18 passing unit cases. Database constraints, actual deletion, concurrency, reconnect, rollback/reapplication and ordinary-role denial remain untested.

## Exact next step

Start with file 1. Explain why validate_note can request deletion without deleting a row. Then continue in this order. Review the comments before making further changes; no migration or maintenance command is part of this reading checklist.
