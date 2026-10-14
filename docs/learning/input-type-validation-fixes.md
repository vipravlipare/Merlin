# Fix the eight input-validation failures

Observed October 10, 2026: the current unit suite reports **82 passed, 8 failed**. These failures happen in Python before SQL runs. The migration already uses INTEGER batch arguments and a BOOLEAN draft column; changing those declarations will not fix these failures.

## Two changes for you to write

In `app/notes_maintenance.py`, at the start of `run_once`, before the range comparison or connection, require the exact built-in integer type. The acceptance condition is `type(batch_size) is int`. Reject other types with ValueError and a message containing `Batch size`. Keep the existing range of 1–1000. Do not convert inputs: converting a float or Boolean can silently change its meaning. An isinstance check alone accepts True because Boolean inherits from integer in Python.

In `app/note_rules.py`, at the start of `validate_note`, before normalization or deletion decisions, require the exact Boolean type. The acceptance condition is `type(is_draft) is bool`. Reject other types with ValueError. Keep the False default. Do not convert inputs with bool: the nonempty string "false" becomes True.

| Case | Current defect | Required result after your change |
|---|---|---|
| Batch True | Reaches the mocked connection | ValueError before any connection |
| Batch 1.5 | Reaches the mocked connection | ValueError before any connection |
| Batch 1.0 | Reaches the mocked connection | ValueError before any connection |
| Batch None | Accidental comparison TypeError | Deliberate ValueError before any connection |
| Batch "100" | Accidental comparison TypeError | Deliberate ValueError before any connection |
| Draft "false" | Accepted as truthy, protecting a blank note | ValueError before deciding draft/deletion behavior |
| Draft 1 | Accepted as truthy | ValueError before deciding draft/deletion behavior |
| Draft None | Accepted as false-like | ValueError before deciding draft/deletion behavior |

## Verify the changes

Run from the Ubuntu checkout `/home/vipra/Merlin`:

```bash
.venv/bin/python -m pytest tests/test_note_rules_and_maintenance.py -q
```

Keep the existing tests unchanged: batch tests require ValueError and prove the connector was never called; draft tests require rejection rather than coercion. A successful rerun must also preserve valid integer batches and actual True/False draft behavior. Record the observed result; do not assume 90 passes before running it.

This suite uses mocked connections and refuses accidental real connections. It does not prove SQL constraints, real transaction rollback, migration application, or ownership security. Those remain pending; the isolated PostgreSQL image currently lacks the required PL/Python extension. Do not run the migration on preserved Sprint 0 storage.

📚 Learn first: Python built-in functions, `type` and `isinstance`: https://docs.python.org/3/library/functions.html ; Boolean type: https://docs.python.org/3/library/stdtypes.html#boolean-type-bool . Reference links; not reverified online this turn.

↩ Return: write the two guards, run the unchanged suite, and compare every failing case with the required result above.

Application code and migration were not edited in this review. Actual minutes are unknown; this work consumes the existing Day 6 verification allocation within the 360-minute cap.
