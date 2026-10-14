# MER-1 step 4: database verification

## Scope and safety

This records step 4 of MER-1: valid/invalid writes, transaction/reconnect behavior, migration undo/reapplication, and honest outcomes. The verification allocation remains **39 minutes**, not an added feature budget. Learner elapsed time is unknown; automated runtime is recorded separately below.

Allowed target: Compose project `merlin-d6-20261008105707`, database `merlin_d6`, cluster `7694311451826794534`. A fresh read verified that identity and zero users/notes before testing. Preserved Sprint 0 volume `merlin_postgres_data` and cluster `7691749973399031842` are excluded. Do not run a cleanup worker concurrently with these tests.

The existing migration files and application code were unchanged. The latest 4.3 verification executed those migrations only in private disposable storage, as described below. No Jira checkbox or status was changed.

## 4.1 Valid and invalid records

📚 Learn first: [Constraints](https://www.postgresql.org/docs/17/ddl-constraints.html), read required fields, unique and foreign-key constraints; [individual database evidence](case-effectiveness-evidence/database-cases.md), locate the cases below. Official constraints page opened October 11, 2026.
↩ Return: predict success or the exact rejection before reading each observed result. Suggested allocation: 10 minutes within step 4.

| Requirement | Case evidence | Expected result |
|---|---|---|
| Valid owned inserts | `app-own-insert`, default-ID cases and ordinary fixture creation | Stored values satisfy rules; app role accepts its own actor. |
| Duplicate email | `F051` | Case variants reject through `users_email_unique`, not an unrelated error. |
| Absent optional email | `F049-F050` | More than one user can omit email. |
| Missing required owner | `F065` | Required `user_id` is rejected. |
| Nonexistent owner | `F066` | Foreign-key rejection. |
| Valid title length | `limit-title-174`, `limit-title-175` | Accepted at/below weighted limit. |
| Invalid title length | `limit-title-176`, `emoji-title-overflow`, `draft-title-overflow` | Rejected by `notes_title_limit`; drafts do not bypass the limit. |
| Blank title with contentful body | `F031`, Unicode title cases | Title normalizes to NULL; body is retained. This is valid, not an invalid-title case. |
| Completely blank saved content | `F040` and whitespace parity cases | Rejected as contentless saved data. A blank draft is a separate permitted state. |

Tests deliberately make the other fields valid when exercising a particular rejection. SQLSTATE and constraint/trigger assertions distinguish intended rejection from a syntax, permission or connection error. The tests use synthetic rows and rollback. A skipped opt-in database test is not a pass.

## 4.2 Transaction rollback and reconnect

📚 Learn first: [Transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), read commit and rollback; [lifecycle evidence](case-effectiveness-evidence/database-lifecycle-cases.md). The official transaction page was opened earlier in this session on October 11, 2026.
↩ Return: explain why reconnecting after an uncommitted fixture cannot prove durable committed visibility. Suggested allocation: 8 minutes within step 4.

Two different proofs are required:

1. The ordinary suite's failed-second-write test performs two operations in one transaction, deliberately fails the second, reconnects and verifies the first uncommitted operation left no row behind.
2. `committed-reconnect-cascade` explicitly commits synthetic rows, opens another database session and verifies those rows exist. It then deletes the synthetic account and reconnects to verify its notes cascaded away.

`second-operation-failure-rolls-back-cleanup` separately proves that failure of the second cleanup does not retain the first cleanup's modifications. Committed synthetic lifecycle fixtures are removed by their exact generated owner, not a broad table deletion. Run lifecycle checks only after the empty-database suite finishes.

These checks do not prove recovery from a PostgreSQL restart, a host crash or uncertain connection loss during commit.

## 4.3 Undo/reapplication: current review

**PASS — disposable-storage verification completed October 11, 2026.** A fresh database was created inside an independently guarded temporary PostgreSQL copy. Its actual schema permissions and prerequisite state were recorded before applying migration 001. Migration 001 and 002 were applied and committed; 002 and 001 were then undone and committed; reconnecting confirmed absence of their objects/roles and exact restoration of the captured baseline. Reapplying 001 and 002 restored equivalent schema/permissions. All 389 rebuilt database cases passed, including real reconnect/failed-write rollback behavior. An unrelated sentinel row survived. Source identity, fingerprint and empty tables were preserved, and all disposable containers/volumes were removed. [Current committed verification evidence](migration-undo-reapplication-results.json).

The genuine baseline belongs to this fresh disposable database. It is not a recovered historical baseline for the existing Day 6 source database. That missing history still forbids a guessed committed undo of the source; it does not prevent verifying the requested path on fresh disposable storage. Earlier synthetic rollback-only branches and safety regressions remain useful additional evidence in the [down-file review](users-notes-down-migration-review.md).

To repeat this focused committed rehearsal without adding it to the fast routine fault suite:

```bash
.venv/bin/python tools/verify_migration_roundtrip.py --out /tmp/merlin-migration-roundtrip-results.json
```

The verifier creates its own guarded copies and refuses an inherited sandbox target. It uses the same suite lock, so it cannot overlap another complete-suite run. It never applies migrations to the source. Its output reports PASS/FAIL, individual checks, the real captured baseline, migration hashes and preservation/cleanup evidence. Existing routine tests remain unchanged.

📚 Learn first: [Migration explanation](../learning/docker-and-database-migrations.md), distinguish transaction rollback from executable migration reversal; [current setup walkthrough](../learning/current-app-setup-walkthrough.md), sections 7–10 and 14. Use these local sources before writing SQL.
↩ Return: explain why the baseline must be captured before the first up, why undo runs 002 then 001, and why reapplication runs 001 then 002. Review or repeat the recorded disposable rehearsal. Suggested review allocation: 12 minutes within step 4; extra coding replaces later work rather than adding hours.

### Acceptance contract for your undo file

- Define its supported starting state explicitly. Undo migration 002 before undoing 001; retain the external PL/Python prerequisite rather than assuming migration 001 created it.
- Gate the exact disposable database and cluster before any destructive change. Refuse unexpected identities. Require an empty synthetic target so dropping tables cannot silently destroy populated storage.
- Require transaction-safe execution and stop at the first error. Unexpected objects, dependencies, role memberships or target state must fail rather than be removed silently.
- Remove the view, tables and their dependent indexes/triggers/policies, then the functions no longer required. Use reviewed explicit dependencies; do not use broad schema deletion or indiscriminate CASCADE to erase unknown objects.
- Handle the three migration-created permission groups and their schema grants explicitly. Roles are cluster-wide, not scoped to one database. Confirm there are no dependencies in another database before removing them.
- Explain the intended post-undo public-schema permissions. Migration 001 revoked PUBLIC CREATE and added named-role grants. Restoring a guessed default is not proof of restoring the original state; use a captured pre-migration baseline or record the limitation.
- Preserve unrelated objects, extension/runtime setup, credentials, databases and storage. Down migrations do not recover deleted user data.

### Proof required before calling this PASS

Capture target identity, empty rows, expected objects and privilege state. Use an independently isolated test target whose server runtime matches the prerequisites, or a reviewed transaction-local exercise on the verified disposable target that cannot commit destructive changes. The chosen method must accommodate cluster-wide role names and migration 002's fixed identity gate; a new database alone does not solve either issue.

Undo 002, undo 001, assert that only the expected objects/roles are absent, reapply 001, then reapply 002. Compare structure and behavior: constraints, functions, triggers, indexes, RLS, grants, defaults, view and role powers. Execute the valid/invalid and ownership checks against the rebuilt state. Roll back the entire rehearsal when using transaction-local verification and then reconnect to confirm the original installed state is intact.

Do not paste migration 002 unchanged inside an outer rollback-only transaction: its embedded COMMIT would end that outer transaction. A safe rehearsal needs an explicitly reviewed handling of those transaction boundaries. Never rerun existing up files on the unchanged installed database.

Record whether proof is transaction-local or a committed disposable rebuild. One does not establish every recovery property of the other. Keep 4.3 unchecked until the actual path succeeds.

## 4.4 Results and ownership scope

📚 Learn first: [Effectiveness audit](case-effectiveness-audit.md), read remaining limits; [MER-1 completion audit](mer-1-completion-audit.md), distinguish technical proof from learner confirmation.
↩ Return: record PASS, FAIL or PENDING for each requirement, identify the first real failure or missing prerequisite and name one exact next action. Suggested allocation: 9 minutes, including identity review and handoff; total allocations are 10 + 8 + 12 + 9 = 39 minutes.

Database role/actor ownership checks can pass because an SQL ownership boundary exists. Authenticated API ownership remains **PENDING** because the backend is unbuilt. Do not substitute administrative access or a caller-controlled actor setting for authenticated identity.

First unresolved prerequisite: missing migration 001 down file. This is **PENDING / not executed**, not a fabricated test failure. The initial Docker socket denial was an execution-permission problem; the approved identity check subsequently succeeded. Neither is an application defect.

## Execution results

Fresh verification completed October 11, 2026. Historical fault-detection evidence remains linked above; no new mutation audit is implied by rerunning the baseline suite.

| Item | Actual result | Evidence |
|---|---|---|
| 4.1 valid inserts and intended rejections | **PASS** | All 389 installed PostgreSQL cases passed, including the case IDs listed above. |
| 4.2 failed second write / reconnect | **PASS** | Included in the 389-case run; two additional focused lifecycle baselines also passed. |
| 4.3 foundation undo/reapplication | **PASS** | Committed undo/reapplication on fresh private storage with a real captured baseline; 389 rebuilt cases passed; source and unrelated data preserved. |
| 4.4 honest results record | **PASS** | This table records execution, missing proof and first unresolved prerequisite. |
| SQL ownership boundary | **PASS** | Restricted app-role actor, cross-user insert/read/edit/delete and privilege checks in the real database suite. |
| Authenticated API cross-user denial | **PENDING** | No authenticated backend exists. SQL role proof is not API identity proof. |
| Preservation | **PASS** | Identity and empty tables verified; final schema/privilege fingerprint equals the original and saved audit fingerprint. |

Database command:

```bash
MERLIN_RUN_DB_TESTS=1 .venv/bin/python -m pytest -q tests/test_users_notes_database.py --tb=short
```

Actual output: `389 passed in 139.40s (0:02:19)`, exit status 0. No failing case or unexpected application error occurred.

After this suite finished, the existing lifecycle implementation was imported and its `execute(case)` baseline was called sequentially for `committed-reconnect-cascade` and `second-operation-failure-rolls-back-cleanup`. Both returned `{'outcome': 'passed'}`. Its existing preservation check verified the initial fingerprint against saved lifecycle evidence, and verified the same fingerprint after synthetic teardown. Exit status 0. No lifecycle source or test expectation was changed.

The shell permission denial was resolved before tests ran. The interrupted chat turn did not invalidate the running checks: their completed output was recovered and checked before recording these results.

**First application failure: none observed.** Initial focused-verifier attempts exposed report-directory setup, baseline queries assuming installed objects, and an overlong generated test username. Those harness defects were fixed without changing application constraints or migration files; initial reports are preserved in the committed-verification artifact. All four step-4 requirements now have technical PASS evidence within their stated scope. Authenticated API denial remains PENDING and is recorded honestly. No source migration commit, credential change, scheduler start, Jira edit, Git commit or push was performed.
