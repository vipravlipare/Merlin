# Migration replay equivalence review

Reviewed 2026-10-12. Two authorized source files changed: tools/audit_database_cases.py and tools/audit_migration_undo.py. No database commands or full suite ran.

The false PUBLIC CREATE branch still executes all 382 SQL CASES after undo/rebuild. The true branch performs its complete independent undo, permission restoration, sentinel/prerequisite/login preservation, rebuild, runtime/metadata comparison and rollback. Its repeated business corpus is consolidated only when the same-run equivalence witness matches the successful false branch. Its reported case_count is explicitly zero, never 382.

All 14 gates, 17 repairs, three concurrency checks, five lifecycle cases, SQL baseline tests and 607 fault pairs remain. No evidence is reused from an earlier run.

## Equality dimensions

The fingerprint now checks the following logical metadata. Full original definitions, owners and grants remain included.

- Columns: relation and ordinal, type name and type modifier, collation identity, array dimensionality, required and generated flags, identity mode, ACL, storage and compression, column options, missing-value metadata.
- Relations: owner and ACL, row-security enable/force, relation kind and persistence, access method, table/view options including security_invoker, replica identity, tablespace identity.
- Functions: full stored definition, owner and ACL, SET configuration, strictness, volatility, parallel mode, SECURITY DEFINER flag, leakproof flag.
- Constraints: full definition, validation status, deferrable and initially-deferred flags.
- Policies: name, command kind, permissive/restrictive flag, roles, USING and WITH CHECK expressions.
- Indexes: definition, key/expression order, directions and predicates, valid, ready and live state, unique, primary and NULL uniqueness flags, key and attribute counts, access method and options.
- Roles: login/superuser/bypass/create DB/create role/replication flags, role configuration, inherit flag, connection limit, valid-until, database/role default-setting records.
- Memberships: role/member/grantor identities, admin, inherit and set-role options.
- Other: public schema owner/ACL, column defaults and generated expressions, trigger definition and enabled state, view definition, rewrite rules and enabled state, inheritance parents and sequence.
- Runtime: same per-run command/target, same server version, same database encoding/collation/ctype/version, same session/current user, same selected parsing/time/row-security/access-method/compression/locale settings, same extension names and versions, pinned Unicode helper probe and version guard embedded in unchanged up SQL, zero users and notes before and after rebuild.
- Sources: all four migration file hashes unchanged before/after each branch, SQL test source hash unchanged, both audit tool source hashes unchanged.
- Normalization: role OIDs map to role names, generated RI constraint trigger numeric suffixes normalize, only outer inventory ordering normalizes, nested arrays retain exact order.

## Fail-closed witness

Both rows include equivalence_witness. All boolean evidence must be true; rebuilt/reference schema and runtime digests must agree. The source hash dictionary covers all four migrations, the SQL test file and both audit tools, checked before and after each branch. The target command is fixed within the run. The parent result gate additionally binds both rebuilt branches to the executed false branch, the assigned migration container/socket command digest and the exact seven current source hashes; contradictory reference digests cannot establish equivalence. False reports replay_mode=executed and case_count=382; true reports replay_mode=equivalent_rebuild and case_count=0. A failed first replay cannot establish the reference. Missing snapshots or any changed metadata/runtime/source rejects the audit.

Role OIDs and PostgreSQL-generated RI trigger numeric suffixes normalize because rebuilding changes identities. Only the outer inventory order normalizes. Nested array order is preserved, preventing equality from concealing an ordered metadata change.

## Validation and limits

Offline AST/import checks pass. In-memory mocked audit runs accept identical rebuilds with counts 382/0 and reject a changed second-branch column type, TimeZone, or nested-array order. These experiments validate Python witness logic only; they do not validate PostgreSQL SQL syntax or fresh database execution.

This proof is scoped to the fixed current migrations and tests. Physical file IDs, pages, transaction IDs and planner statistics may differ. Random UUID values and server clock readings also differ naturally. The matching logical definitions, settings, empty state, verified per-run runtime and unchanged sources justify sharing one business replay; this is not a universal PostgreSQL-equivalence theorem. The strengthened fingerprint changes recorded preservation values. Fresh full-suite validation subsequently passed: all ten default stages in 55.65 seconds, with actual branch case counts 382/0 and source preservation/cleanup PASS. Real validator positive and nine negative counterfactuals also passed. See [the final review](../test-suite-second-review.md) and its durable evidence.

Catalog fields verified 2026-10-12 against [PostgreSQL 17 pg_attribute](https://www.postgresql.org/docs/17/catalog-pg-attribute.html), [pg_class](https://www.postgresql.org/docs/17/catalog-pg-class.html) and [pg_db_role_setting](https://www.postgresql.org/docs/17/catalog-pg-db-role-setting.html).
