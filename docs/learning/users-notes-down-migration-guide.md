# Fill in migration 001's down file from its up file

Your starter file is [001_users_notes.down.sql](../../migrations/001_users_notes.down.sql). You filled TODOs 3–9 after the initial scaffold. At your explicit request, the assistant repaired inventory refusal, preservation checks and the header. The current file is executable destructive SQL; its rollback-only undo/reapply checks pass. Genuine historical baseline evidence remains required before the agreed real execution can proceed.

The source to work alongside it is [001_users_notes.up.sql](../../migrations/001_users_notes.up.sql). Open both side by side in VS Code. Search for `CREATE`, `GRANT`, `REVOKE` and `ALTER`: those statements identify the effects you must account for.

**A completed down migration will remove the users/notes structure and its stored rows.** This exercise must reject populated tables and unexpected targets before any destructive statement. Never use preserved Sprint 0 volume `merlin_postgres_data` or cluster `7691749973399031842`. Only rollback-only safety-gate tests were executed for TODOs 1–2; the installed database state was preserved.

## 1. Understand the job before writing SQL

An up migration builds or changes database structure. A down migration reverses those particular structural changes. It is not a backup, and it does not recover deleted rows.

Do not reverse the file line by line. Instead, list created objects, work out their dependencies, and remove dependent objects before the objects they depend on. A view uses a table; a note references a user; triggers and checks use functions. This determines the order.

Your database currently has migration 002 applied too. The supported input for this down file is **001 applied, 002 undone**. Otherwise 002's additional functions and dependencies still exist. You must separately prove the supported starting state rather than assuming it from a filename.

📚 Learn first: [DROP TABLE](https://www.postgresql.org/docs/17/sql-droptable.html), read automatic removal of table-owned objects and RESTRICT versus CASCADE; [step 4 acceptance contract](../testing/database-step-four-verification.md), read section 4.3. Official page opened October 11, 2026.
↩ Return: draw `active_notes depends on notes; notes references users; table triggers/checks use functions`. Explain why deleting users first is the wrong starting point. Use the existing learning/implementation allocation; this is not additional funded work.

## 2. Map each part of up to its undo

| Find in migration 001 up | What it did | What your down must account for |
|---|---|---|
| PL/Python prerequisite block | Required an already-installed extension | Keep the extension. Up did not create it. |
| `SELECT ...note_weighted_length('check')` | Checked imports and pinned runtime | No persistent object was created by the check itself. |
| Six `CREATE FUNCTION` statements | Created reusable functions | Remove each by exact schema/name/input signature after removing dependencies. |
| Three `CREATE ROLE` statements | Created permission groups | Remove only these groups after removing owned objects and remaining grants. |
| `CREATE TABLE public.users` | Created users and its column/constraint definitions | Remove the table after notes. |
| `CREATE TABLE public.notes` | Created notes with its foreign key | Remove after the active view, before users. |
| `CREATE INDEX` statements | Added table indexes | Table removal also removes its indexes; do not repeat unnecessary index drops. |
| Four `CREATE TRIGGER` statements | Attached functions to tables | Table removal also removes its triggers; functions remain separate objects. |
| RLS and `CREATE POLICY` statements | Added table access rules | Table removal removes its attached policies; no separate disable step is needed. |
| `CREATE VIEW public.active_notes` | Created a stored query over notes | Remove first so it no longer depends on notes. |
| Object `ALTER ... OWNER` statements | Assigned ownership | Removing those objects ends their ownership dependencies. No guessed reassignment is needed. |
| Table/function privileges | Granted access to created objects | Grants disappear with the removed objects. |
| Schema grants to the three groups | Granted access to existing `public` schema | Revoke those specific grants before role removal; the schema remains. |
| `REVOKE CREATE ... FROM PUBLIC` | Changed permissions on an existing schema | Restore only the known pre-migration state, not guessed broader access. |

The point of this table is to account for all effects without writing redundant reversal statements. An external dependency is a reason to investigate, not to append CASCADE until the error disappears.

## 3. TODOs 1–2: transaction and safety gate

Use a **caller-owned transaction** for this learner implementation. That means the execution/rehearsal opens the transaction and decides whether to roll back or commit; your file does not secretly commit it. This matches migration 001 up's existing caller-transaction contract. Document that requirement in the file.

Before removal, verify the exact database and cluster: `merlin_d6` and `7694311451826794534`. Migration 002 already contains a `DO` block showing how `current_database()`, `pg_control_system()` and `RAISE EXCEPTION` can make a wrong identity stop execution. Study that pattern and write your own gate; do not copy its transaction ending into a rollback-only rehearsal.

Also require expected objects, empty users/notes, migration 002 undone, and no unexpected role memberships or outside dependencies. Lock the tables before checking emptiness so another transaction cannot insert rows between the check and removal. The worker must remain stopped. Mere comments saying “empty” or “correct target” are not executable protection.

Migration 002 down has its own BEGIN/COMMIT. Passing it unchanged into an outer rollback-only transaction can commit that outer work. The full rehearsal needs explicit review of boundaries for both 002 files. Do not run the sequence while learning the syntax.

📚 Learn first: [Transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), read commit/rollback; [migration 002 up](../../migrations/002_whitespace_parity.up.sql), inspect its existing target check. Official transaction page was opened earlier on October 11, 2026.
↩ Return: implement the gate first and explain which check refuses a wrong cluster, nonempty table or unsupported starting state. Review this section before adding destructive statements.

## 4. TODOs 3–4: remove the view, then tables

Write statements for the known view, notes table and users table in that order. Schema-qualify their names so the intended schema is explicit. Find the syntax in the linked PostgreSQL reference; use the object names listed in the mapping table.

Table removal includes attached indexes, triggers, constraints and policies. Do not write one statement for every column. Standalone functions and permission groups need later treatment. [PostgreSQL DROP TABLE](https://www.postgresql.org/docs/17/sql-droptable.html).

Use RESTRICT, which is the default, to refuse unknown dependent objects. For this strict single-use reversal, do not hide a wrong starting state with blanket IF EXISTS. A missing required object should fail the gate rather than make a half-applied migration look successful.

Hint ladder: first locate `CREATE VIEW`; next locate the notes foreign key; finally name the three objects in dependency-removal order before writing syntax. You do not need to reproduce their original columns.

## 5. TODO 5: remove functions using signatures

Copy the identity of each function, not its body. A signature uses the input types to distinguish functions with the same name. A default parameter value does not make the parameter disappear from that identity.

| Function in up | Input identity to use |
|---|---|
| `cleanup_expired_blank_notes` | `(INTEGER)` |
| `purge_deleted_notes` | `(INTEGER)` |
| `manage_note_content` | `()` |
| `manage_note_deletion` | `()` |
| `manage_users_notes_timestamps` | `()` |
| `note_weighted_length` | `(TEXT)` |

You do not include `RETURNS`, `DEFAULT 100`, parameter names or the function body in its removal identity. Keep `public.` in the name. Tables are removed first because their triggers/checks use these functions. PL/pgSQL body references do not necessarily provide a complete dependency inventory by themselves; review known references too. [PostgreSQL DROP FUNCTION](https://www.postgresql.org/docs/17/sql-dropfunction.html).

📚 Learn first: the DROP FUNCTION page above, read input arguments and RESTRICT. Official page opened October 11, 2026.
↩ Return: explain why a function callable without an explicit batch argument still has `(INTEGER)` in its signature. Then fill the six function TODOs.

## 6. TODOs 6–8: schema grants, baseline and roles

Up granted `USAGE, CREATE` on public to `merlin_d6_owner`, and `USAGE` to `merlin_d6_app` and `merlin_d6_maintenance`. Write the specific corresponding revocations using those privileges, that schema and those grantees. Removing tables does not remove grants on the surviving schema. [PostgreSQL REVOKE](https://www.postgresql.org/docs/17/sql-revoke.html).

Do not interpret “reverse REVOKE” as permission to automatically grant PUBLIC CREATE. PUBLIC means all roles. If the pre-001 baseline already denied PUBLIC CREATE, granting it would weaken security. If the earlier state is unknown, record that missing prerequisite and stop the strict restore path. A rebuilt disposable test can capture a known baseline before running up; that does not retroactively prove the original baseline.

Only after owned objects and schema grants are removed should you remove the three NOLOGIN groups. Preserve the actual `merlin_d6` login. Roles exist across the cluster; a dependency in another database must stop removal. PostgreSQL automatically removes memberships when dropping a role, so check for unexpected memberships beforehand instead of silently erasing later setup. [PostgreSQL DROP ROLE](https://www.postgresql.org/docs/17/sql-droprole.html).

Avoid broad DROP OWNED, deleting the public schema or touching databases/volumes to get around dependency errors. The goal is a narrow undo of migration 001.

📚 Learn first: REVOKE and DROP ROLE above, read remaining dependencies and memberships. Official pages opened October 11, 2026.
↩ Return: explain why dropping a table does not revoke a schema grant, why NOLOGIN groups differ from the connection login, and what evidence determines PUBLIC CREATE restoration.

## 7. TODO 9: prove behavior, not file existence

The following is a review contract, not a command to execute immediately:

| Stage | Required observation |
|---|---|
| Before | Correct disposable identity; empty tables; supported 001-only state; captured unrelated state/permissions. |
| After down | Known view/tables/functions/groups absent; PL/Python, login, schema and unrelated objects preserved; recorded baseline permissions restored. |
| After up 001, then up 002 | Expected structure, grants, roles, policies, triggers, constraints and indexes restored. |
| Behavior | Valid inserts accepted; intended duplicate/missing-owner/invalid-title failures; rollback/reconnect and SQL ownership rules still pass. |
| After rollback-only rehearsal | Fresh connection sees the original installed state and empty tables; fingerprints match. |

A transaction-local rehearsal and a committed rebuild are different evidence. Preserve that distinction in the results. The previously passing 389 database cases do not automatically prove your new down file.

Do not run a migration command simply because the starter exists. Finish its executable gates and statements, explain its intended post-state, review transaction boundaries and then run the reviewed disposable rehearsal. Jira 4.3 remains PENDING until this happens.

## Start with this small task

Open the scaffold and up file side by side. Review implemented TODOs 1–2, then explain the transaction requirement and why the table locks protect the empty-table check. Continue with TODO 3 (the view) and TODO 4 (notes before users). You can develop the dependency-removal sections from the mapping table while the baseline-permission question remains explicitly unresolved.

Your explain-back: “What exactly will disappear, what must survive, and what prevents this file from changing the wrong database?” Record your own answer; copying the guide is not proof of understanding.


## Implemented TODOs 1–2: what each line does

The file is now **psql-specific**, because its backslash commands are interpreted by psql rather than PostgreSQL. Do not pass the entire file to Psycopg as ordinary SQL.

`\set ON_ERROR_STOP on` makes a script stop at its first failure. `\if :AUTOCOMMIT` rejects the default automatic-commit mode. The caller must choose `AUTOCOMMIT=off`; psql then opens a transaction before SQL as needed. The file has no BEGIN or COMMIT of its own. Rehearsal must explicitly ROLLBACK. This avoids a hidden commit ending your protective outer transaction. [psql documentation](https://www.postgresql.org/docs/17/app-psql.html), opened October 11, 2026.

The two SET LOCAL commands limit lock waiting to two seconds and each statement to ten seconds, only for the transaction. The DO block is a small procedural block: IF checks a condition and RAISE EXCEPTION stops unsupported execution. It checks the fixed database/cluster, required objects/functions, absence of 002's helpers, other client sessions, emptiness, permission-group attributes/memberships and role references in other databases.

An ACCESS EXCLUSIVE lock on users/notes is acquired **before** emptiness is checked. It remains until transaction end. A competing insert must wait or time out, instead of slipping between the empty check and later table removal. The other-client check is a conservative snapshot, not a permanent barrier against new connections. [Explicit locking](https://www.postgresql.org/docs/17/explicit-locking.html), opened October 11, 2026.

The baseline prerequisite is a caller-provided temporary table `pg_temp.merlin_001_undo_baseline` with columns `public_create_before BOOLEAN` and `baseline_source TEXT`, exactly one row, a non-NULL boolean and a nonblank source description. It records whether PUBLIC had CREATE before 001, and where that historical observation came from. The gate never invents this evidence or grants CREATE. A caller can lie about provenance, so review the record; validation of its shape is not proof that its contents are true. Other earlier schema grants also need review if the starting environment was customized.

The real original pre-001 baseline has not been established here. Accordingly, a genuine run still requires that evidence; the gate tests used clearly labelled synthetic baseline rows only inside transactions that rolled back. On the normally installed current database the gate correctly refuses because 002 remains applied. Nothing was permanently reversed to get a passing result.

Unexpected remaining dependencies must still be caught by the reviewed RESTRICT operations in TODOs 3–9. The gate is not a complete fingerprint comparison of every original schema object or a production migration runner. See [the focused gate results](../testing/users-notes-down-gate-verification.md).


## Current review repairs

The preflight now compares expected and actual table-owned artifact names in both directions. This catches additions as well as missing indexes, user triggers, constraints, policies and columns. Unexpected table rules are also refused. It prevents the demonstrated extra-index removal that RESTRICT alone could not prevent. It does not certify that every same-named object's original definition is unchanged.

A temporary preservation snapshot freezes the reviewed baseline boolean, schema identity/owner, other schema grants, connection-login attributes and PL/Python extension state. Restoration reads the frozen baseline. Postchecks compare surviving state with that snapshot and assert the expected PUBLIC CREATE value. The snapshot is temporary and drops at transaction end; its existence is not proof of historical baseline provenance.

Both baseline branches and the 17 targeted regression checks pass; see [review and repairs](../testing/users-notes-down-migration-review.md). No migration was committed. Continue by locating genuine baseline evidence and explaining the reviewed execution contract, rather than filling already-completed SQL sections.
