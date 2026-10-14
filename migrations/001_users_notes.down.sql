-- DESTRUCTIVE DOWN MIGRATION: removes the migration-001 objects and roles.
-- psql-only; refuse populated storage and unreviewed schema changes.
-- Caller contract: psql -X, AUTOCOMMIT=off, one transaction, explicit ROLLBACK
-- for rehearsal. No BEGIN/COMMIT here; never combine unreviewed 002 COMMITs.
-- Supported input: 001 installed, 002 undone, empty verified disposable target.
-- Guide: docs/learning/users-notes-down-migration-guide.md

-- TODO 1 COMPLETE: stop at the first error and require manual transaction mode.
\set ON_ERROR_STOP on
\if :AUTOCOMMIT
DO $transaction_required$
BEGIN
    RAISE EXCEPTION 'Refusing undo: psql AUTOCOMMIT must be off';
END;
$transaction_required$;
\endif
-- With AUTOCOMMIT off, psql begins a transaction before the first SQL command.
SET LOCAL lock_timeout = '2s';
SET LOCAL statement_timeout = '10s';

-- TODO 2 COMPLETE: reject unsupported states before any destructive commands.
-- Caller supplies pg_temp.merlin_001_undo_baseline with exactly one row:
-- public_create_before BOOLEAN NOT NULL, baseline_source TEXT NOT NULL.
-- The row must describe a recorded pre-001 baseline, not guessed permissions.
-- Synthetic baseline rows are permitted only for rollback-only gate tests.
DO $undo_gate$
DECLARE
    object_name TEXT;
    role_count INTEGER;
    baseline_count BIGINT;
    baseline_create BOOLEAN;
    baseline_source TEXT;
BEGIN
    IF current_database() <> 'merlin_d6' OR
       (SELECT system_identifier::text FROM pg_control_system()) <> '7694311451826794534'
    THEN
        RAISE EXCEPTION 'Refusing undo: unexpected database or cluster';
    END IF;

    IF to_regclass('public.users') IS NULL OR to_regclass('public.notes') IS NULL OR
       to_regclass('public.active_notes') IS NULL THEN
        RAISE EXCEPTION 'Refusing undo: migration 001 objects missing';
    END IF;
    IF to_regprocedure('public.note_text_is_blank(text)') IS NOT NULL OR
       to_regprocedure('public.note_email_is_clean(text)') IS NOT NULL THEN
        RAISE EXCEPTION 'Refusing undo: undo migration 002 first';
    END IF;
    FOREACH object_name IN ARRAY ARRAY[
        'public.note_weighted_length(text)',
        'public.manage_users_notes_timestamps()', 'public.manage_note_content()',
        'public.manage_note_deletion()', 'public.cleanup_expired_blank_notes(integer)',
        'public.purge_deleted_notes(integer)'
    ] LOOP
        IF to_regprocedure(object_name) IS NULL THEN
            RAISE EXCEPTION 'Refusing undo: migration 001 function missing';
        END IF;
    END LOOP;

    -- Any other client session is conservatively treated as a possible writer.
    -- This is a snapshot, not a permanent connection barrier; locks protect rows.
    IF EXISTS (SELECT 1 FROM pg_stat_activity
               WHERE datname = current_database() AND pid <> pg_backend_pid()
                 AND backend_type = 'client backend') THEN
        RAISE EXCEPTION 'Refusing undo: another database client is connected';
    END IF;
    -- Prevent concurrent inserts/updates between empty-table checks and removal.
    LOCK TABLE public.users, public.notes IN ACCESS EXCLUSIVE MODE;
    IF EXISTS (SELECT 1 FROM public.users) OR EXISTS (SELECT 1 FROM public.notes) THEN
        RAISE EXCEPTION 'Refusing undo: users and notes must be empty';
    END IF;

    SELECT count(*) INTO role_count FROM pg_roles
    WHERE rolname IN ('merlin_d6_owner', 'merlin_d6_app', 'merlin_d6_maintenance');
    IF role_count <> 3 OR EXISTS (
        SELECT 1 FROM pg_roles
        WHERE rolname IN ('merlin_d6_owner', 'merlin_d6_app', 'merlin_d6_maintenance')
          AND (rolcanlogin OR rolsuper OR rolcreatedb OR rolcreaterole OR
               rolreplication OR rolbypassrls)
    ) THEN
        RAISE EXCEPTION 'Refusing undo: permission groups missing or changed';
    END IF;
    IF EXISTS (
        SELECT 1 FROM pg_auth_members m JOIN pg_roles r
          ON r.oid = m.roleid OR r.oid = m.member
        WHERE r.rolname IN ('merlin_d6_owner', 'merlin_d6_app', 'merlin_d6_maintenance')
    ) THEN
        RAISE EXCEPTION 'Refusing undo: unexpected permission-group membership';
    END IF;
    IF EXISTS (
        SELECT 1 FROM pg_shdepend d JOIN pg_roles r ON r.oid = d.refobjid
        WHERE d.refclassid = 'pg_authid'::regclass
          AND r.rolname IN ('merlin_d6_owner', 'merlin_d6_app', 'merlin_d6_maintenance')
          AND d.dbid <> 0 AND d.dbid <> (SELECT oid FROM pg_database WHERE datname = current_database())
    ) THEN
        RAISE EXCEPTION 'Refusing undo: permission group referenced by another database';
    END IF;

    IF to_regclass('pg_temp.merlin_001_undo_baseline') IS NULL THEN
        RAISE EXCEPTION 'Refusing undo: recorded pre-001 permission baseline required';
    END IF;
    SELECT count(*) INTO baseline_count FROM pg_temp.merlin_001_undo_baseline;
    IF baseline_count <> 1 THEN
        RAISE EXCEPTION 'Refusing undo: permission baseline must contain one row';
    END IF;
    SELECT public_create_before, b.baseline_source INTO baseline_create, baseline_source
    FROM pg_temp.merlin_001_undo_baseline AS b;
    IF baseline_create IS NULL OR baseline_source IS NULL OR btrim(baseline_source) = '' THEN
        RAISE EXCEPTION 'Refusing undo: permission baseline is incomplete';
    END IF;
    -- DROP TABLE also removes its attached artifacts under RESTRICT. Compare
    -- both directions so extra and missing objects cannot silently disappear.
    IF EXISTS (
        WITH expected(kind, table_name, name) AS (VALUES
            ('index','users','users_pkey'),
            ('index','users','users_username_unique'),
            ('index','users','users_username_canonical_idx'),
            ('index','users','users_email_unique'),
            ('index','notes','notes_pkey'),
            ('index','notes','notes_user_created_idx'),
            ('index','notes','notes_user_updated_idx'),
            ('index','notes','notes_user_device_updated_idx'),
            ('index','notes','notes_blank_body_expiry_idx'),
            ('index','notes','notes_user_draft_updated_idx'),
            ('index','notes','notes_deleted_at_idx'),
            ('trigger','users','users_timestamps'),
            ('trigger','notes','notes_content'),
            ('trigger','notes','notes_deletion'),
            ('trigger','notes','notes_timestamps'),
            ('constraint','users','users_pkey'),
            ('constraint','users','users_username_unique'),
            ('constraint','users','users_id_uuidv4'),
            ('constraint','users','users_username_format'),
            ('constraint','users','users_email_clean'),
            ('constraint','notes','notes_pkey'),
            ('constraint','notes','notes_user_id_fkey'),
            ('constraint','notes','notes_id_uuidv4'),
            ('constraint','notes','notes_title_nonblank'),
            ('constraint','notes','notes_has_content'),
            ('constraint','notes','notes_deadline_matches_body'),
            ('constraint','notes','notes_title_limit'),
            ('constraint','notes','notes_body_limit'),
            ('policy','users','users_own_account'),
            ('policy','notes','notes_own_account'),
            ('policy','notes','notes_maintenance'),
            ('policy','notes','notes_app_delete_limit'),
            ('policy','notes','notes_maintenance_delete_limit'),
            ('column','users','id'), ('column','users','username'),
            ('column','users','username_canonical'), ('column','users','email'),
            ('column','users','created_at'), ('column','users','updated_at'),
            ('column','notes','id'), ('column','notes','user_id'),
            ('column','notes','title'), ('column','notes','body'),
            ('column','notes','created_at'), ('column','notes','updated_at'),
            ('column','notes','device_created_at'), ('column','notes','device_edited_at'),
            ('column','notes','blank_body_expires_at'), ('column','notes','deleted_at'),
            ('column','notes','is_draft')
        ), actual AS (
            SELECT 'index' AS kind, tablename::text AS table_name, indexname::text AS name
            FROM pg_indexes WHERE schemaname='public' AND tablename IN ('users','notes')
            UNION ALL
            SELECT 'trigger', c.relname::text, t.tgname::text
            FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid
            WHERE t.tgrelid IN ('public.users'::regclass,'public.notes'::regclass) AND NOT t.tgisinternal
            UNION ALL
            SELECT 'constraint', c.relname::text, k.conname::text
            FROM pg_constraint k JOIN pg_class c ON c.oid=k.conrelid
            WHERE k.conrelid IN ('public.users'::regclass,'public.notes'::regclass)
            UNION ALL
            SELECT 'policy', c.relname::text, k.polname::text
            FROM pg_policy k JOIN pg_class c ON c.oid=k.polrelid
            WHERE k.polrelid IN ('public.users'::regclass,'public.notes'::regclass)
            UNION ALL
            SELECT 'column', c.relname::text, a.attname::text
            FROM pg_attribute a JOIN pg_class c ON c.oid=a.attrelid
            WHERE a.attrelid IN ('public.users'::regclass,'public.notes'::regclass)
              AND a.attnum>0 AND NOT a.attisdropped
        )
        (SELECT * FROM actual EXCEPT SELECT * FROM expected)
        UNION ALL (SELECT * FROM expected EXCEPT SELECT * FROM actual)
    ) OR EXISTS (
        SELECT 1 FROM pg_rewrite WHERE ev_class IN ('public.users'::regclass,'public.notes'::regclass)
    ) THEN
        RAISE EXCEPTION 'Refusing undo: unexpected or missing table-owned artifact';
    END IF;
    IF (SELECT relkind FROM pg_class WHERE oid='public.users'::regclass) <> 'r' OR
       (SELECT relkind FROM pg_class WHERE oid='public.notes'::regclass) <> 'r' OR
       (SELECT relkind FROM pg_class WHERE oid='public.active_notes'::regclass) <> 'v' THEN
        RAISE EXCEPTION 'Refusing undo: unexpected object kind';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname='plpython3u') OR
       NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='merlin_d6' AND rolcanlogin) THEN
        RAISE EXCEPTION 'Refusing undo: required extension or connection login missing';
    END IF;
    IF to_regclass('pg_temp.merlin_001_undo_preserved') IS NOT NULL THEN
        RAISE EXCEPTION 'Refusing undo: preservation snapshot already exists';
    END IF;
    -- Freeze the reviewed inputs and state that must survive this undo.
    CREATE TEMP TABLE merlin_001_undo_preserved ON COMMIT DROP AS
    SELECT baseline_create AS public_create_before,
           n.oid AS schema_oid, n.nspowner AS schema_owner,
           (SELECT array_agg(oid) FROM pg_roles WHERE rolname IN
             ('merlin_d6_owner','merlin_d6_app','merlin_d6_maintenance')) AS removed_role_oids,
           (SELECT jsonb_agg(to_jsonb(e) ORDER BY e.oid) FROM pg_extension e
             WHERE e.extname='plpython3u') AS extension_state,
           (SELECT jsonb_build_object('oid',r.oid,'login',r.rolcanlogin,
              'super',r.rolsuper,'createdb',r.rolcreatedb,'createrole',r.rolcreaterole,
              'replication',r.rolreplication,'bypassrls',r.rolbypassrls)
              FROM pg_roles r WHERE r.rolname='merlin_d6') AS login_state,
           (SELECT COALESCE(jsonb_agg(to_jsonb(a) ORDER BY a.grantee,a.grantor,a.privilege_type),'[]'::jsonb)
              FROM aclexplode(COALESCE(n.nspacl,acldefault('n',n.nspowner))) a
              WHERE a.grantee NOT IN (SELECT oid FROM pg_roles WHERE rolname IN
                ('merlin_d6_owner','merlin_d6_app','merlin_d6_maintenance'))
                AND NOT (a.grantee=0 AND a.privilege_type='CREATE')) AS other_schema_acl
    FROM pg_namespace n WHERE n.nspname='public';
    -- This inventories names, not every original definition or baseline provenance.
    -- External dependencies are still refused by the subsequent RESTRICT drops.
END;
$undo_gate$;

-- TODO 3: Remove public.active_notes before its underlying table.
DROP VIEW public.active_notes RESTRICT;

-- TODO 4: Remove public.notes before public.users (foreign-key dependency).
-- Table-owned indexes, triggers, policies and constraints disappear with tables.
-- Prefer default RESTRICT; an unknown external dependency should stop execution.
DROP TABLE public.notes RESTRICT;
DROP TABLE public.users RESTRICT;

-- TODO 5: Remove exactly these migration-001 functions, once dependents are gone:
-- public.cleanup_expired_blank_notes(INTEGER)
-- public.purge_deleted_notes(INTEGER)
-- public.manage_note_content()
-- public.manage_note_deletion()
-- public.manage_users_notes_timestamps()
-- public.note_weighted_length(TEXT)
-- Input argument types identify functions; do not copy bodies or return types.
DROP FUNCTION public.cleanup_expired_blank_notes(INTEGER) RESTRICT;
DROP FUNCTION public.purge_deleted_notes(INTEGER) RESTRICT;
DROP FUNCTION public.manage_note_content() RESTRICT;
DROP FUNCTION public.manage_note_deletion() RESTRICT;
DROP FUNCTION public.manage_users_notes_timestamps() RESTRICT;
DROP FUNCTION public.note_weighted_length(TEXT) RESTRICT;

-- TODO 6: Revoke the explicit public-schema grants added by migration 001:
-- USAGE, CREATE for merlin_d6_owner; USAGE for app and maintenance groups.
-- Do not indiscriminately drop everything owned by a role or drop public schema.
REVOKE CREATE, USAGE ON SCHEMA public FROM merlin_d6_owner;
REVOKE USAGE ON SCHEMA public FROM merlin_d6_app;
REVOKE USAGE ON SCHEMA public FROM merlin_d6_maintenance;

-- TODO 7: Restore PUBLIC CREATE only if the recorded pre-001 baseline granted it.
-- Otherwise retain the reviewed baseline; never guess broader permissions.
DO $restore_baseline$
DECLARE
    baseline_create BOOLEAN;
BEGIN
    SELECT public_create_before INTO baseline_create
    FROM pg_temp.merlin_001_undo_preserved;

    IF baseline_create THEN
        GRANT CREATE ON SCHEMA public TO PUBLIC;
    ELSE
        REVOKE CREATE ON SCHEMA public FROM PUBLIC;
    END IF;
END;
$restore_baseline$;

-- TODO 8: Remove exactly merlin_d6_app, merlin_d6_maintenance, merlin_d6_owner.
-- These roles are cluster-wide. Unexpected dependencies or memberships must stop.
-- Preserve the merlin_d6 login, all databases, volumes and PL/Python prerequisite.
DROP ROLE merlin_d6_app;
DROP ROLE merlin_d6_maintenance;
DROP ROLE merlin_d6_owner;

-- TODO 9: Assert expected objects/roles are gone, unrelated state is preserved.
-- Caller must verify reapplication of 001 then 002 and restored behavior.
-- Leave Jira 4.3 PENDING until actual SQL and its undo/reapply proof pass.
DO $undo_postchecks$
DECLARE
    role_count INTEGER;
    preserved RECORD;
    observed_acl JSONB;
BEGIN
    SELECT * INTO STRICT preserved FROM pg_temp.merlin_001_undo_preserved;
    -- 1. Verify all migration-001 tables and views are gone
    IF to_regclass('public.users') IS NOT NULL OR
       to_regclass('public.notes') IS NOT NULL OR
       to_regclass('public.active_notes') IS NOT NULL THEN
        RAISE EXCEPTION 'Undo verification failed: migration-001 tables/views still exist';
    END IF;

    -- 2. Verify all migration-001 functions are gone
    IF to_regprocedure('public.note_weighted_length(text)') IS NOT NULL OR
       to_regprocedure('public.manage_users_notes_timestamps()') IS NOT NULL OR
       to_regprocedure('public.manage_note_content()') IS NOT NULL OR
       to_regprocedure('public.manage_note_deletion()') IS NOT NULL OR
       to_regprocedure('public.cleanup_expired_blank_notes(integer)') IS NOT NULL OR
       to_regprocedure('public.purge_deleted_notes(integer)') IS NOT NULL THEN
        RAISE EXCEPTION 'Undo verification failed: migration-001 functions still exist';
    END IF;

    -- 3. Verify all migration-001 roles are gone
    SELECT count(*) INTO role_count
    FROM pg_roles
    WHERE rolname IN ('merlin_d6_owner', 'merlin_d6_app', 'merlin_d6_maintenance');

    IF role_count <> 0 THEN
        RAISE EXCEPTION 'Undo verification failed: migration-001 roles still exist';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE oid=preserved.schema_oid
                   AND nspname='public' AND nspowner=preserved.schema_owner) THEN
        RAISE EXCEPTION 'Undo verification failed: public schema changed';
    END IF;
    IF (SELECT jsonb_agg(to_jsonb(e) ORDER BY e.oid) FROM pg_extension e
        WHERE e.extname='plpython3u') IS DISTINCT FROM preserved.extension_state THEN
        RAISE EXCEPTION 'Undo verification failed: PL/Python prerequisite changed';
    END IF;
    IF (SELECT jsonb_build_object('oid',r.oid,'login',r.rolcanlogin,
          'super',r.rolsuper,'createdb',r.rolcreatedb,'createrole',r.rolcreaterole,
          'replication',r.rolreplication,'bypassrls',r.rolbypassrls)
          FROM pg_roles r WHERE r.rolname='merlin_d6') IS DISTINCT FROM preserved.login_state THEN
        RAISE EXCEPTION 'Undo verification failed: connection login changed';
    END IF;
    IF EXISTS (SELECT 1 FROM pg_namespace n,
               LATERAL aclexplode(COALESCE(n.nspacl,acldefault('n',n.nspowner))) a
               WHERE n.oid=preserved.schema_oid AND a.grantee=0 AND a.privilege_type='CREATE')
       IS DISTINCT FROM preserved.public_create_before THEN
        RAISE EXCEPTION 'Undo verification failed: PUBLIC CREATE does not match baseline';
    END IF;
    SELECT COALESCE(jsonb_agg(to_jsonb(a) ORDER BY a.grantee,a.grantor,a.privilege_type),'[]'::jsonb)
    INTO observed_acl FROM pg_namespace n,
         LATERAL aclexplode(COALESCE(n.nspacl,acldefault('n',n.nspowner))) a
    WHERE n.oid=preserved.schema_oid AND NOT (a.grantee=0 AND a.privilege_type='CREATE');
    IF observed_acl IS DISTINCT FROM preserved.other_schema_acl THEN
        RAISE EXCEPTION 'Undo verification failed: unrelated schema grants changed';
    END IF;
END;
$undo_postchecks$;
