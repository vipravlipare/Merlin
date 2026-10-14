# Review of the learner-completed migration 001 down file

## Current 4.3 completion

**PASS — fresh disposable-storage verification.** The [committed undo/reapplication report](migration-undo-reapplication-results.json) captures the actual pre-001 permissions of a fresh database inside a private copy, commits undo/reapplication, verifies semantic equivalence after reconnecting, and passes all 389 rebuilt database cases. Unrelated sentinel data and external prerequisites survived; source preservation and temporary-container/volume cleanup passed. No migration file was changed. This supersedes the 4.3 PENDING verdicts in the historical review below. The original source database's historical baseline remains unknown; the fresh baseline is not permission to undo that source.

📚 Learn first: [4.3 execution and scope](database-step-four-verification.md#43-undoreapplication-current-review).
↩ Return: review the captured baseline and down/up sequence before repeating the focused disposable verifier.

## Historical review

Reviewed October 11, 2026. Source: [001_users_notes.down.sql](../../migrations/001_users_notes.down.sql), SHA-256 `7bd5af8b3396154f1afcf1b8abf0bfe1293df8f668543de64fe1a68d37bbfae7`. TODOs 3–9 now contain the learner's SQL. This review did not edit the migration.

**The main undo/reapply sequence works in a transaction-local rehearsal, but the agreed strict safety contract is not yet fully satisfied.** One unexpected-object refusal failure was reproduced. Historical descriptions calling TODOs 3–9 empty now describe the earlier scaffold, not this reviewed file.

## Authorized fixes after this review

The learner explicitly requested repairs. The current down file fixes all three findings below: its header identifies destructive behavior; preflight compares expected versus actual names of indexes, user triggers, constraints, policies and columns, and refuses table rules; postchecks validate PUBLIC CREATE, other schema grants, schema identity/owner, connection-login attributes and PL/Python extension state. Permission inputs are frozen in a temporary preservation snapshot before object removal. External dependencies still use RESTRICT.

Current source SHA-256: `22cd8805e287303999c4aac8b084f6d7e08bf209950ede4b3f6038a7e0ca3275`. Both rollback-only branches passed again with 388 table-driven cases per branch, semantic schema/privilege equivalence and exact original fingerprint preservation after rollback. All 17 focused regression checks passed: 11 added/missing artifact/rule states, five deliberate preservation defects and one inventory-guard-removal experiment. These are separate from the historical 798-case count.

The missing-column fixture initially failed during setup because the view depended on that column. Its corrected transaction-local fixture removes/recreates the view around the column change so the same inventory-refusal assertion actually reaches the gate. The initial failure and corrected outcomes are retained in [raw repair results](users-notes-down-repair-results.json); no assertion was weakened.

The true/false baseline rows were explicitly synthetic test data. Genuine historical pre-001 PUBLIC CREATE evidence remains unresolved. Names are inventoried, not every original object definition or every possible database dependency. The new postchecks protect specified schema/permission/login/extension state; broader unrelated-object preservation is additionally supported by the sentinel and rollback fingerprint checks, not a claim of exhaustive production proof. No committed undo or deployment occurred. 4.3 stays PENDING until authentic baseline evidence and the agreed execution proof are complete.

## Findings from the pre-repair review (resolved by the authorized patch)

### 1. Unexpected table-owned objects can be silently removed

At the table drops (lines 121–122), RESTRICT protects against external dependencies such as another view. It does not protect an extra index attached to the table: PostgreSQL drops that index as part of dropping its table. This behavior is documented in [DROP TABLE](https://www.postgresql.org/docs/17/sql-droptable.html), opened earlier on October 11, 2026.

Reproduction added an index named `review_unexpected_idx` on notes.body within a disposable transaction, then ran the actual down file. It finished with exit 0 and removed the index along with notes, instead of refusing the unexpected object. Everything was rolled back afterward. The matching external-view experiment correctly stopped with exit 3 at the notes drop.

The strict [step 4 contract](database-step-four-verification.md) requires unexpected objects/dependencies to cause refusal rather than silent removal. The existing gate supplied by the assistant does not inventory table-owned artifacts, so this is a shared gate limitation, not evidence that the learner chose the wrong DROP order. Strengthen the preflight before destructive statements: compare actual indexes, triggers, constraints and policies with the known migration-001 inventory. Do not allow unknown objects merely because DROP TABLE automatically removes them. Use the up file and installed catalog definitions to determine the expected inventory, and test added/missing artifacts individually. Do not replace RESTRICT with CASCADE.

### 2. Postchecks verify disappearance, but not all promised preservation

The block at lines 173–203 correctly checks absence of the known view/tables/functions/roles. It does not assert that PUBLIC CREATE matches the baseline, or that the public schema, connection login and PL/Python prerequisite survive. The review harness checked those separately and they passed, so this is missing self-verification rather than an observed failure of the ordinary undo sequence.

Fill out the existing postchecks using the recorded baseline and explicit prerequisites. Compare unrelated-object state using a captured inventory/fingerprint where appropriate. Checking that the target objects are gone does not by itself prove everything else survived. These postchecks complement rather than replace the preflight that must prevent unexpected-object removal.

### 3. Header is now misleading

Lines 1–2 say TODOs 3–9 are unfinished and that the file removes no application objects. The current file contains executable DROP VIEW, DROP TABLE, DROP FUNCTION and DROP ROLE statements. Replace those comments with an accurate destructive-operation notice, supported starting state and review/execution limitations. A reader must not treat this as a harmless comment-only scaffold.

## What passed

| Portion | Observation |
|---|---|
| TODO 3 | View removal precedes its underlying table. |
| TODO 4 | Notes removal precedes users, respecting the foreign-key dependency. |
| TODO 5 | All six function names/input signatures are correct and execute after table dependencies are removed. |
| TODO 6 | Explicit schema grants are revoked before role removal. |
| TODO 7 | Both synthetic baseline values restore the expected PUBLIC CREATE state. |
| TODO 8 | All three permission groups are removed; the connection login remains. |
| TODO 9 | Absence checks execute successfully after the removal sequence. |
| Reapply | Migration 001 up followed by 002 up succeeds after undo. |
| Rebuilt behavior | All 388 table-driven database cases pass for each of the two baseline branches. |
| Rebuilt structure | Semantic schema and privilege definitions match before undo and after reapplication. |
| Preservation after rehearsal | Original fingerprint, target identity and zero users/notes restored after rollback. |

The two branches produce 776 passing case executions, not 776 new distinct cases. The separate failed-second-write/reconnect pytest case was not rerun against the uncommitted rebuilt schema: it requires separate sessions. Its earlier passing evidence remains separate. The historical 798-case audit total is unchanged.

## How the verification worked

The allowed target was database merlin_d6, cluster7694311451826794534, Compose project merlin-d6-20261008105707. A fresh read verified identity and empty tables before any writes.

Each rehearsal began in manual transaction mode. The existing 002 down was used in memory with only its inspected top-level BEGIN/COMMIT removed, preserving its actual body inside the rollback-only transaction. The actual learner down file then ran with a labelled synthetic baseline. Separate assertions checked schema/login/extension preservation, the chosen PUBLIC CREATE value and an unrelated sentinel table.

Migration 001 up and 002 up were reapplied inside the same transaction. The 002 up transaction wrapper was handled in memory in the same reviewed way. No migration source was rewritten. Each table-driven case used a savepoint with independent UUID fixtures; returning to the savepoint removed its data/role-setting changes without undoing the rebuilt schema.

The structure comparison included functions, constraints, policies, object/column/schema grants, roles/memberships, defaults, indexes, triggers and the view. Recreated role OIDs and generated internal foreign-key trigger names were normalized for semantic comparison; their changed physical identifiers were not incorrectly treated as a behavioral difference. After final ROLLBACK, the original raw preservation fingerprint matched exactly.

The two dependency experiments also rolled back. Neither an unexpected index nor a view was left installed. All runners exited successfully after recording their expected outcomes; the index refusal requirement itself failed and remains a finding, not a passing safety check.

Temporary execution records: `/tmp/merlin-down-review-results.json` and `/tmp/merlin-down-dependency-review-results.json`, with the corresponding temporary Python runners. These are temporary audit artifacts, not a maintained migration runner or a promise of permanent reproducibility. The saved observations and source hash above are the durable review record.

## What remains before 4.3 can be called complete

Repair unexpected-artifact preflight, complete preservation assertions and correct the header. Rerun the affected refusal/roundtrip checks after the edits. The genuine pre-001 permission baseline is still unresolved: successful synthetic true/false branches prove conditional logic, not the original historical permission state. Do not invent that baseline to get a passing result.

This was transaction-local undo/reapplication, not a committed rebuild or crash/restart recovery test. It is meaningful evidence for the migration path but does not establish every environment/recovery scenario. No commit, push, Jira edit, scheduler start or permanent migration was performed. Preserved Sprint 0 storage was excluded. Keep 4.3 PENDING while the strict safety failure and baseline proof remain open.

📚 Learn first: [DROP TABLE](https://www.postgresql.org/docs/17/sql-droptable.html), read which attached objects are removed automatically; [fill-in guide](../learning/users-notes-down-migration-guide.md), revisit preflight and postconditions. Official page opened earlier October 11, 2026.
↩ Return: explain why RESTRICT caught the external view but not the attached index; update the expected-artifact preflight and postconditions, then review the changed SQL before executing another rollback-only rehearsal. Use existing learning/implementation time; extra work replaces later tasks.
