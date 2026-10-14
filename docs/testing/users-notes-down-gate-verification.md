# Migration 001 down: TODOs 1–2 verification

October 11, 2026. The learner explicitly authorized implementation of TODOs 1–2 in [the partial down file](../../migrations/001_users_notes.down.sql). No undo commands for TODOs 3–9 were implemented.

## Acceptance and observed results

**17 focused checks passed.** These counts are separate from the earlier 798-case audit; that historical total was not regenerated. Gate execution is not complete migration undo/reapplication, so Jira 4.3 remains PENDING.

| Check | Result | Assertion |
|---|---|---|
| Default autocommit | PASS | Nonzero exit, transaction-mode refusal, no completion marker. |
| Migration 002 still installed | PASS | Refuses until 002 is undone. |
| Missing baseline table | PASS | Refuses missing pre-001 permission evidence. |
| Supported test input | PASS | Gate reaches completion in manual transaction mode with 001-only state and labelled synthetic baseline. |
| Wrong cluster expectation | PASS | Temporary in-memory file copy with a different expected fingerprint refuses the actual cluster. |
| Populated target | PASS | Synthetic user inside the transaction causes empty-table refusal. |
| Missing view | PASS | Transaction-local removal causes required-object refusal. |
| Missing function | PASS | Transaction-local removal causes required-function refusal. |
| Changed role powers | PASS | Transaction-local LOGIN attribute causes role refusal. |
| Unexpected membership | PASS | Transaction-local owner/app membership causes refusal. |
| Empty baseline | PASS | Refuses zero rows. |
| Duplicate baseline | PASS | Refuses two rows. |
| Blank baseline source | PASS | Refuses empty source description. |
| NULL baseline value | PASS | Refuses missing boolean value. |
| Other connected client | PASS | An independent live session causes conservative concurrency refusal. |
| Insert after successful gate | PASS | Independent insert times out with SQLSTATE 55P03 while the gate transaction holds its table locks. |
| Wrong database | PASS | Connection to the disposable cluster's existing postgres database refuses before target-object access. No objects were created there. |

Negative cases require the intended error and nonzero exit, not arbitrary failure. The successful case proves the full current gate can execute. The concurrency check proves the locks persist beyond the DO block until rollback.

## Isolation and preservation

The initial read verified database merlin_d6, cluster7694311451826794534, zero users/notes and no other connected client. All state changes were transaction-local on this disposable cluster. To test the supported 001-only state, the existing 002 down script was used in memory with only its verified top-level BEGIN/COMMIT wrapper removed; it remained within a test transaction that could only roll back. The applied migration files were unchanged.

Temporary baseline rows were explicitly labelled synthetic test evidence. They do not establish the original pre-001 PUBLIC CREATE value. Tests also rolled back temporary fixture rows, view/function removal, role attribute/membership changes and the attempted concurrent insert. A fresh preservation check after each test verified the exact original schema/permission fingerprint, identity and zero stored users/notes. The two test runners exited 0. No permanent schema change or data loss occurred.

Preserved Sprint 0 storage was not accessed. No worker was started, no migration undo was committed, and Jira/credentials/commits/pushes were unchanged.

The focused runners and first raw JSON output are temporary files in /tmp (`merlin-undo-gate-check.py`, `merlin-undo-gate-concurrency.py`, `merlin-undo-gate-results.json`), not installed services or a maintained full migration test suite. The first runner covers 14 cases; the second covers three live-session/database cases. Reproduction requires those files or reconstruction of the described cases, not a claim that temporary files will exist forever.

## Limits and next action

The role-reference guard for dependencies in another database was implemented but not exercised by creating cross-database role-owned objects in this verification. A full original-schema fingerprint match, all dependency variations, malicious caller input, every concurrent worker race and actual PUBLIC permission restoration remain unproven. These are not included in the 17 passing checks.

TODOs 3–9 still need reviewed explicit object removal, schema-grant handling, baseline-driven permission restoration, role removal and postconditions. Unknown external dependencies must cause those RESTRICT operations to stop. The current gate does not replace that dependency proof. Full undo/reapplication remains PENDING.

📚 Learn first: [psql](https://www.postgresql.org/docs/17/app-psql.html), read AUTOCOMMIT and ON_ERROR_STOP; [PostgreSQL locking](https://www.postgresql.org/docs/17/explicit-locking.html), read ACCESS EXCLUSIVE and lock lifetime. Official pages opened October 11, 2026.
↩ Return: explain why autocommit mode is refused, why emptiness is checked after locking and why a synthetic permission baseline cannot authorize restoration of the original database's privileges. Continue with the [fill-in guide](../learning/users-notes-down-migration-guide.md), TODOs 3–9, inside existing learning/implementation time.
