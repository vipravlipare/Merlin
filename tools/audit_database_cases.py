"""Exercise every SQL case against transaction-local faulty schema definitions.

Only the already isolated Day 6 cluster is allowed. Faults, fixtures, grants,
roles, indexes and function replacements stay inside transactions that never
commit. No schema fault is installed permanently. Failed sessions roll back.
The separate reconnect fault deliberately commits only its synthetic first user;
a gated finally block deletes that exact user before preservation is checked.
"""

import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SESSION = None


def load_cases():
    spec = importlib.util.spec_from_file_location("audited_db_cases", ROOT / "tests/test_users_notes_database.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if os.environ.get('MERLIN_FAST_DB_TESTS') == '1':
        from tools.database_test_session import container_command
        module.COMMAND = container_command(module.COMMAND[7:])
    tree = ast.parse((ROOT / "tests/test_users_notes_database.py").read_text())
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "test_database_rule")
    setup = next(node.value.value for node in ast.walk(function) if isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name) and target.id == "setup" for target in node.targets))
    return module, setup


def replace_function(name, body, language="plpgsql", returns="TRIGGER", arguments=""):
    return f"CREATE OR REPLACE FUNCTION public.{name}({arguments}) RETURNS {returns} LANGUAGE {language} AS $fault$\n{body}\n$fault$;"


def edit_function(name, old, new):
    # Fetch the installed definition and refuse a recipe that does not apply.
    return ("DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public." + name +
            "'::regprocedure) INTO original; IF position($old$" + old + "$old$ IN original)=0 THEN "
            "RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$" + old +
            "$old$,$new$" + new + "$new$); END $mutate$;")


def recipes(case):
    ident, sql = case.id, case.sql
    rows = []
    def add(name, fault, before_seed=False):
        rows.append({"name": name, "sql": fault, "before_seed": before_seed})
    if ident == "auth-lookup-exact-name":
        add("auth-lookup-ignores-name", edit_function(
            "lookup_auth_credential(text)",
            "WHERE u.username_canonical = lower(p_username)",
            "WHERE u.username_canonical <> lower(p_username)"))
    if ident == "auth-lookup-unknown-user-empty":
        add("auth-lookup-leaks-unknown-user", edit_function(
            "lookup_auth_credential(text)",
            "WHERE u.username_canonical = lower(p_username)",
            "WHERE true"))
    if ident == "auth-credentials-not-directly-readable":
        add("auth-password-hash-direct-grant",
            "GRANT SELECT ON public.auth_credentials TO merlin_api;")
    if ident == "runtime-role-cannot-read-notes":
        add("runtime-role-note-read-granted",
            "GRANT SELECT ON public.notes TO merlin_api;")
    if ident == "auth-refresh-family-owner-filter":
        add("auth-refresh-owner-policy-removed",
            "DROP POLICY auth_refresh_families_owner ON public.auth_refresh_families; "
            "CREATE POLICY auth_refresh_families_owner ON public.auth_refresh_families "
            "FOR ALL TO merlin_api USING (true) WITH CHECK (true);")
    if ident == "auth-refresh-idle-expiry-cap":
        add("auth-idle-window-unbounded", edit_function(
            "validate_auth_refresh_family()",
            "NEW.idle_expires_at > statement_timestamp() + INTERVAL '30 days'",
            "FALSE"))
    if ident == "auth-refresh-absolute-expiry-cap":
        add("auth-absolute-window-unbounded", edit_function(
            "validate_auth_refresh_family()",
            "NEW.absolute_expires_at > NEW.created_at + INTERVAL '90 days'",
            "FALSE"))
    if ident == "auth-refresh-token-expiry-bound":
        add("auth-refresh-token-outlives-family", edit_function(
            "validate_auth_refresh_token()",
            "NEW.expires_at > family.idle_expires_at",
            "FALSE"))
    if ident == "auth-refresh-token-consumed-once":
        add("auth-refresh-token-reuse-accepted", edit_function(
            "validate_auth_refresh_token()",
            "OLD.consumed_at IS NOT NULL OR NEW.consumed_at IS NULL",
            "FALSE"))
    blank_false = replace_function("note_text_is_blank", "return value is None", "plpython3u", "BOOLEAN", "value TEXT")
    blank_true = replace_function("note_text_is_blank", "return True", "plpython3u", "BOOLEAN", "value TEXT")
    content_pass = replace_function("manage_note_content", "BEGIN RETURN NEW; END")
    if ident.startswith("F015-"):
        add("incorrect-weighted-count", replace_function("note_weighted_length", "return 1" if ident.endswith("empty") else "return 0", "plpython3u", "INTEGER", "value TEXT"))
    if "parity-" in ident or "unicode-" in ident or ident.startswith("blank-body-") or ident in {"F045-nbsp", "F031", "F036", "F040"}:
        if "email" in ident or ident == "F053-nbsp":
            add("email-cleanliness-always-accepts", replace_function("note_email_is_clean", "return True", "plpython3u", "BOOLEAN", "value TEXT"))
        elif "nonwhitespace" in ident:
            add("invisible-content-misclassified-blank", blank_true)
        elif ident.endswith("-maintenance"):
            codepoint = ident.split("-")[1].removeprefix("U+")
            add("worker-whitespace-codepoint-skipped", edit_function(
                "cleanup_expired_blank_notes(integer)",
                "public.note_text_is_blank(body)",
                "(public.note_text_is_blank(body) AND body <> U&'\\" + codepoint + "')"))
        else:
            add("whitespace-misclassified-content", blank_false)
    # Disable the exact constraint that a negative case claims must enforce it.
    for constraint in re.findall(r"got_constraint = '([^']+)'", sql):
        if constraint == "users_email_unique":
            add("email-uniqueness-removed", "DROP INDEX public.users_email_unique;")
        else:
            table = "users" if constraint.startswith("users_") else "notes"
            cascade = " CASCADE" if constraint == "users_pkey" else ""
            add("constraint-removed-" + constraint, f"ALTER TABLE public.{table} DROP CONSTRAINT {constraint}{cascade};")
    for column in re.findall(r"got_column = '([^']+)'", sql):
        table = "users" if ident.startswith("username-") else "notes"
        add("required-column-now-nullable", f"ALTER TABLE public.{table} ALTER COLUMN {column} DROP NOT NULL;")
    if ident.startswith("limit-") and "got_constraint" not in sql or ident in {"F020", "F021"}:
        field = "title" if ident in {"F020"} or ident.startswith("limit-title-") else "body"
        limit = 175 if field == "title" else 7000
        add("valid-text-overcounted", edit_function("note_weighted_length(text)",
            'return sum(4 if emoji.is_emoji(part) else 1 for part in regex.findall(r"\\X", value))',
            'return sum(4 if emoji.is_emoji(part) else 1 for part in regex.findall(r"\\X", value)) + (2 if len(value) >= ' + str(limit - 1) + ' else 0)'))
    if (ident.startswith("email-") and ident != "email-insert-duplicate") or ident == "F053-nbsp":
        add("stored-email-validation-removed", replace_function("note_email_is_clean", "return True", "plpython3u", "BOOLEAN", "value TEXT"))
    if ident in {"F033", "F034"}:
        field = "title" if ident == "F033" else "body"
        add("real-content-trimmed", replace_function("manage_note_content", f"BEGIN NEW.{field}:=btrim(NEW.{field}); RETURN NEW; END"))
    if ident in {"F037", "F092"}:
        add("drafts-now-forbidden", "ALTER TABLE public.notes ADD CONSTRAINT audit_reject_drafts CHECK (NOT is_draft);")
    if ident == "F039":
        add("optional-title-now-required", "ALTER TABLE public.notes ALTER COLUMN title SET NOT NULL;")
    if ident == "F049-F050":
        add("null-emails-now-unique", "UPDATE public.users SET email=id::text || '@example.test'; CREATE UNIQUE INDEX audit_null_email ON public.users(email) NULLS NOT DISTINCT;")
    if ident == "username-twenty":
        add("valid-username-limit-too-strict", "ALTER TABLE public.users ADD CONSTRAINT audit_username_limit CHECK(length(username)<20);")
    if ident == "F059":
        add("canonical-column-not-generated", "ALTER TABLE public.users ALTER COLUMN username_canonical DROP EXPRESSION;")
    if ident.startswith("F061-"):
        table = "users" if ident.endswith("user") else "notes"
        add("uuid-default-missing", f"ALTER TABLE public.{table} ALTER COLUMN id DROP DEFAULT;")
        add("uuid-default-repeats-valid-v4", f"ALTER TABLE public.{table} ALTER COLUMN id SET DEFAULT '11111111-1111-4111-8111-111111111111'::uuid;")
    if ident in {"F067", "app-delete-account-cascade"}:
        add("cascade-now-restricts", "ALTER TABLE public.notes DROP CONSTRAINT notes_user_id_fkey; ALTER TABLE public.notes ADD CONSTRAINT notes_user_id_fkey FOREIGN KEY(user_id) REFERENCES public.users(id) ON DELETE NO ACTION;")
    if ident in {"F068", "F069", "F070", "F078", "F079", "F080"}:
        add("immutable-fields-no-longer-protected", replace_function("manage_users_notes_timestamps", "BEGIN RETURN NEW; END"))
    if ident in {"F071", "F072", "F073", "F074", "app-crossuser-delete", "app-unset-actor", "app-active-view"}:
        add("actor-policies-allow-everyone", "ALTER POLICY users_own_account ON public.users USING(true) WITH CHECK(true); ALTER POLICY notes_own_account ON public.notes USING(true) WITH CHECK(true);")
    if ident == "F075-role":
        add("app-can-assume-owner", "GRANT merlin_d6_owner TO merlin_d6_app;")
    if ident.startswith("app-column-"):
        column = ident.removeprefix("app-column-")
        add("protected-column-write-granted", f"GRANT UPDATE({column}) ON public.notes TO merlin_d6_app;")
    if ident in {"app-own-edit", "app-own-insert"}:
        add("actor-policy-rejects-owner", "ALTER POLICY notes_own_account ON public.notes USING(false) WITH CHECK(false);")
    if ident == "app-saved-delete":
        add("saved-notes-permanently-deletable", "ALTER POLICY notes_app_delete_limit ON public.notes USING(true);")
    if ident in {"app-blank-draft-delete", "unicode-blank-draft-delete"} or ident.endswith("draft-delete"):
        add("blank-draft-deletion-forbidden", "ALTER POLICY notes_app_delete_limit ON public.notes USING(false);")
    if ident in {"F076", "F077", "user-clock-forged"}:
        add("server-insert-clocks-forged", edit_function("manage_users_notes_timestamps()", "NEW.updated_at := NEW.created_at;", "NEW.updated_at := NEW.created_at - INTERVAL '1 day';"))
    if ident == "F093":
        add("body-refill-does-not-clear-countdown", edit_function("manage_note_content()", "NEW.blank_body_expires_at := NULL;", "NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '24 hours';"))
    if ident in {"F081", "F082", "F083", "F084", "F085", "F090"}:
        if ident != "F081":
            add("server-edit-clock-wrong", edit_function("manage_users_notes_timestamps()", "NEW.updated_at := OLD.updated_at;", "NEW.updated_at := statement_timestamp() + INTERVAL '1 day';"))
        if ident == "F081":
            add("content-edits-keep-old-clock", edit_function("manage_users_notes_timestamps()", "NEW.updated_at := statement_timestamp();", "NEW.updated_at := OLD.updated_at;"))
    if ident == "F086":
        add("device-clock-not-normalized", edit_function("manage_note_content()", "NEW.device_edited_at := NEW.device_created_at;", "NULL;"))
    if ident == "F089":
        add("device-instant-shifted", edit_function("manage_note_content()", "NEW.device_edited_at := NEW.device_created_at;", "NEW.device_created_at := NEW.device_created_at + INTERVAL '1 hour'; NEW.device_edited_at := NEW.device_created_at;"))
    if ident in {"F038", "F087", "F091", "F093", "F094", "F095", "F096", "F097", "F098", "F118", "note-body-default"} or ident.endswith("countdown"):
        if ident not in {"F093", "F095", "F096", "F097", "F098"}:
            add("countdown-too-short", edit_function("manage_note_content()", "INTERVAL '24 hours'", "INTERVAL '1 hour'"))
        if ident in {"F095", "F096", "F097", "F098"}:
            add("countdown-not-preserved", edit_function("manage_note_content()", "NEW.blank_body_expires_at := OLD.blank_body_expires_at;", "NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '48 hours';"))
    if ident == "F099":
        add("saved-notes-can-become-drafts", content_pass)
    if ident in {"F088", "F106", "F107", "F108", "F112", "F116", "F117"}:
        add("trash-guards-and-clock-removed", replace_function("manage_note_deletion", "BEGIN RETURN NEW; END"))
    if ident == "F109":
        add("active-view-filter-wrong", "CREATE OR REPLACE VIEW public.active_notes WITH (security_invoker=true) AS SELECT * FROM public.notes WHERE true;")
    if ident == "F110":
        add("fresh-restore-forbidden", edit_function("manage_note_deletion()",
            "IF clock_timestamp() >= OLD.deleted_at + INTERVAL '14 days' THEN",
            "IF true OR clock_timestamp() >= OLD.deleted_at + INTERVAL '14 days' THEN"))
    if ident.startswith("sql-batch-"):
        name = "cleanup_expired_blank_notes" if "cleanup_expired" in ident else "purge_deleted_notes"
        add("invalid-batch-accepted", edit_function(name + "(integer)", "IF batch_size IS NULL OR batch_size NOT BETWEEN 1 AND 1000 THEN", "IF false THEN"))
    if ident == "maintenance-fresh-delete":
        add("recent-trash-purge-allowed", "ALTER POLICY notes_maintenance_delete_limit ON public.notes USING(true);")
    if ident == "maintenance-active-read":
        add("worker-sees-active-private-content", "ALTER POLICY notes_maintenance ON public.notes USING(true);")
    if "cleanup_expired_blank_notes(" in sql and not ident.startswith("sql-batch-") and ident != "app-no-cleanup-grant":
        name = "cleanup_expired_blank_notes(integer)"
        if ident.startswith("sql-valid-batch-"):
            old, new = "LIMIT batch_size FOR UPDATE SKIP LOCKED", ("FOR UPDATE SKIP LOCKED" if ident.endswith("-1") else "LIMIT LEAST(batch_size,1) FOR UPDATE SKIP LOCKED")
        elif ident == "expiry-batch-one":
            add("expiry-source-selection-wrong", edit_function(name, "LIMIT batch_size FOR UPDATE SKIP LOCKED", "FOR UPDATE SKIP LOCKED"))
            old, new = "ORDER BY blank_body_expires_at, id", "ORDER BY blank_body_expires_at DESC, id"
        elif ident == "F101":
            old, new = "<= statement_timestamp()", "< statement_timestamp()"
        elif ident == "F100":
            old, new = "<= statement_timestamp()", ">= statement_timestamp()"
        elif ident == "F103":
            fault = edit_function(name, "WHERE blank_body_expires_at <= statement_timestamp()", "WHERE true")
            fault += edit_function(name, "AND public.note_text_is_blank(body)", "AND true")
            fault += edit_function(name, "AND n.blank_body_expires_at <= statement_timestamp()", "AND true")
            fault += edit_function(name, "AND public.note_text_is_blank(n.body)", "AND true")
            add("expiry-filled-content-selected", fault)
            old = None
        elif ident == "F104":
            fault = edit_function(name, "AND NOT is_draft AND deleted_at IS NULL", "AND NOT is_draft")
            fault += edit_function(name, "AND NOT n.is_draft AND n.deleted_at IS NULL", "AND NOT n.is_draft")
            add("expiry-selects-trash-again", fault)
            old = None
        else:
            old, new = "<= statement_timestamp()", ">= statement_timestamp()"
        if old is not None:
            add("expiry-source-selection-wrong", edit_function(name, old, new))
    if "purge_deleted_notes(" in sql and not ident.startswith("sql-batch-") and ident != "app-no-purge-grant":
        name = "purge_deleted_notes(integer)"
        if ident.startswith("sql-valid-batch-"):
            old, new = "LIMIT batch_size FOR UPDATE SKIP LOCKED", ("FOR UPDATE SKIP LOCKED" if ident.endswith("-1") else "LIMIT LEAST(batch_size,1) FOR UPDATE SKIP LOCKED")
        elif ident == "purge-batch-one":
            add("purge-source-selection-wrong", edit_function(name, "LIMIT batch_size FOR UPDATE SKIP LOCKED", "FOR UPDATE SKIP LOCKED"))
            old, new = "ORDER BY deleted_at, id", "ORDER BY deleted_at DESC, id"
        elif ident == "F114":
            old, new = "<= statement_timestamp()", "< statement_timestamp()"
        elif ident == "F113":
            old, new = "INTERVAL '14 days'", "INTERVAL '1 day'"
        elif ident == "F115":
            fault = edit_function(name, "WHERE deleted_at <= statement_timestamp() - INTERVAL '14 days'", "WHERE deleted_at IS NULL")
            fault += edit_function(name, "AND n.deleted_at <= statement_timestamp() - INTERVAL '14 days'", "AND n.deleted_at IS NULL")
            add("purge-selects-active-rows", fault)
            old = None
        else:
            old, new = "<= statement_timestamp()", ">= statement_timestamp()"
        if old is not None:
            add("purge-source-selection-wrong", edit_function(name, old, new))
    if ident == "permission-groups":
        add("permission-role-can-login", "ALTER ROLE merlin_d6_app LOGIN;")
        for power in ["SUPERUSER", "CREATEDB", "CREATEROLE", "REPLICATION", "BYPASSRLS"]:
            add("permission-role-incorrect-" + power.lower(), "ALTER ROLE merlin_d6_app " + power + ";")
        for role in ["merlin_d6_owner", "merlin_d6_maintenance"]:
            add("permission-group-can-login-" + role, "ALTER ROLE " + role + " LOGIN;")
        add("runtime-role-no-login", "ALTER ROLE merlin_api NOLOGIN;")
        add("runtime-role-inherit-enabled", "ALTER ROLE merlin_api INHERIT;")
        for power in ["SUPERUSER", "CREATEDB", "CREATEROLE", "REPLICATION", "BYPASSRLS"]:
            add("runtime-role-incorrect-" + power.lower(), "ALTER ROLE merlin_api " + power + ";")
        add("runtime-role-inherits-notes-permissions", "GRANT merlin_d6_app TO merlin_api;")
    if ident == "rls-forced":
        add("owner-not-subject-to-rls", "ALTER TABLE public.notes NO FORCE ROW LEVEL SECURITY;")
        add("user-owner-not-subject-to-rls", "ALTER TABLE public.users NO FORCE ROW LEVEL SECURITY;")
        for table in ["users", "notes"]:
            add("row-policy-disabled-" + table, "ALTER TABLE public." + table + " DISABLE ROW LEVEL SECURITY;")
    if ident == "app-no-cleanup-grant":
        rows.insert(0, {"name": "app-incorrectly-granted-execute", "sql": "GRANT EXECUTE ON FUNCTION public.cleanup_expired_blank_notes(INTEGER) TO merlin_d6_app;", "before_seed": False})
    if ident == "app-no-purge-grant":
        add("app-incorrectly-granted-purge-execute", "GRANT EXECUTE ON FUNCTION public.purge_deleted_notes(INTEGER) TO merlin_d6_app;")
    if ident == "app-no-schema-create":
        add("app-can-create-schema-objects", "GRANT CREATE ON SCHEMA public TO merlin_d6_app;")
    if ident.startswith("index-"):
        names = {"created": "notes_user_created_idx", "edited": "notes_user_updated_idx", "device": "notes_user_device_updated_idx", "draft": "notes_user_draft_updated_idx"}
        add("timeline-index-missing", "DROP INDEX public." + names[ident.removeprefix("index-")] + ";")
    return rows


FINGERPRINT = """SELECT md5(jsonb_agg(row_data ORDER BY row_data::text)::text) FROM (
 SELECT jsonb_build_object('function',oid::regprocedure::text,'def',pg_get_functiondef(oid),'owner',proowner,'acl',proacl::text,'config',proconfig,'strict',proisstrict,'volatility',provolatile,'parallel',proparallel,'security_definer',prosecdef,'leakproof',proleakproof) AS row_data
 FROM pg_proc WHERE pronamespace='public'::regnamespace AND proname IN ('note_weighted_length','note_text_is_blank','note_email_is_clean','manage_note_content','manage_note_deletion','manage_users_notes_timestamps','cleanup_expired_blank_notes','purge_deleted_notes','lookup_auth_credential','validate_auth_refresh_family','validate_auth_refresh_token')
 UNION ALL SELECT jsonb_build_object('constraint',conname,'def',pg_get_constraintdef(oid),'validated',convalidated,'deferrable',condeferrable,'deferred',condeferred) FROM pg_constraint WHERE conrelid IN ('public.users'::regclass,'public.notes'::regclass,to_regclass('public.auth_credentials'),to_regclass('public.auth_refresh_families'),to_regclass('public.auth_refresh_tokens'))
 UNION ALL SELECT jsonb_build_object('policy',polname,'command',polcmd,'permissive',polpermissive,'roles',polroles::text,'using',pg_get_expr(polqual,polrelid),'check',pg_get_expr(polwithcheck,polrelid)) FROM pg_policy WHERE polrelid IN ('public.users'::regclass,'public.notes'::regclass,to_regclass('public.auth_credentials'),to_regclass('public.auth_refresh_families'),to_regclass('public.auth_refresh_tokens'))
 UNION ALL SELECT jsonb_build_object('table',relname,'owner',relowner,'acl',relacl::text,'rls',relrowsecurity,'force',relforcerowsecurity,'kind',relkind,'persistence',relpersistence,'options',reloptions,'access_method',(SELECT amname FROM pg_am WHERE oid=relam),'replica_identity',relreplident,'tablespace',(SELECT spcname FROM pg_tablespace WHERE oid=reltablespace)) FROM pg_class WHERE oid IN ('public.users'::regclass,'public.notes'::regclass,'public.active_notes'::regclass,to_regclass('public.auth_credentials'),to_regclass('public.auth_refresh_families'),to_regclass('public.auth_refresh_tokens'))
 UNION ALL SELECT jsonb_build_object('index',indexname,'def',indexdef) FROM pg_indexes WHERE schemaname='public' AND tablename IN ('users','notes','auth_credentials','auth_refresh_families','auth_refresh_tokens')
 UNION ALL SELECT jsonb_build_object('role',rolname,'login',rolcanlogin,'super',rolsuper,'bypass',rolbypassrls,'createdb',rolcreatedb,'createrole',rolcreaterole,'replication',rolreplication,'config',rolconfig,'inherit',rolinherit,'connection_limit',rolconnlimit,'valid_until',rolvaliduntil) FROM pg_roles WHERE rolname LIKE 'merlin_d6%' OR rolname='merlin_api'
 UNION ALL SELECT jsonb_build_object('membership',roleid,'member',member,'grantor',grantor,'admin',admin_option,'inherit',inherit_option,'set',set_option) FROM pg_auth_members WHERE member IN ('merlin_d6_app'::regrole,'merlin_d6_maintenance'::regrole,'merlin_d6_owner'::regrole,to_regrole('merlin_api'))
 UNION ALL SELECT jsonb_build_object('column',attrelid::regclass::text||'.'||attname,'acl',attacl::text,'notnull',attnotnull,'generated',attgenerated,'number',attnum,'type',format_type(atttypid,atttypmod),'type_modifier',atttypmod,'collation',attcollation::regcollation::text,'dimensions',attndims,'identity',attidentity,'storage',attstorage,'compression',attcompression,'options',attoptions,'has_missing',atthasmissing,'missing_value',attmissingval::text) FROM pg_attribute WHERE attrelid IN ('public.users'::regclass,'public.notes'::regclass,'public.active_notes'::regclass,to_regclass('public.auth_credentials'),to_regclass('public.auth_refresh_families'),to_regclass('public.auth_refresh_tokens')) AND attnum>0 AND NOT attisdropped
 UNION ALL SELECT jsonb_build_object('schema',nspname,'owner',nspowner,'acl',nspacl::text) FROM pg_namespace WHERE nspname='public'
 UNION ALL SELECT jsonb_build_object('default',adrelid::regclass::text||'.'||adnum,'expr',pg_get_expr(adbin,adrelid)) FROM pg_attrdef WHERE adrelid IN ('public.users'::regclass,'public.notes'::regclass,to_regclass('public.auth_credentials'),to_regclass('public.auth_refresh_families'),to_regclass('public.auth_refresh_tokens'))
 UNION ALL SELECT jsonb_build_object('trigger',tgname,'enabled',tgenabled,'def',pg_get_triggerdef(oid)) FROM pg_trigger WHERE tgrelid IN ('public.users'::regclass,'public.notes'::regclass,to_regclass('public.auth_refresh_families'),to_regclass('public.auth_refresh_tokens'))
 UNION ALL SELECT jsonb_build_object('view','active_notes','def',pg_get_viewdef('public.active_notes'::regclass))
 UNION ALL SELECT jsonb_build_object('index_state',i.indexrelid::regclass::text,'valid',i.indisvalid,'ready',i.indisready,'live',i.indislive,'unique',i.indisunique,'primary',i.indisprimary,'nulls_not_distinct',i.indnullsnotdistinct,'key_count',i.indnkeyatts,'attribute_count',i.indnatts,'options',c.reloptions,'method',a.amname) FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid JOIN pg_am a ON a.oid=c.relam WHERE i.indrelid IN ('public.users'::regclass,'public.notes'::regclass,to_regclass('public.auth_credentials'),to_regclass('public.auth_refresh_families'),to_regclass('public.auth_refresh_tokens'))
 UNION ALL SELECT jsonb_build_object('role_setting',CASE WHEN d.setrole=0 THEN 'all roles' ELSE r.rolname::text END,'database',CASE WHEN d.setdatabase=0 THEN 'all databases' ELSE b.datname::text END,'config',d.setconfig) FROM pg_db_role_setting d LEFT JOIN pg_roles r ON r.oid=d.setrole LEFT JOIN pg_database b ON b.oid=d.setdatabase WHERE (d.setdatabase=0 OR b.datname=current_database()) AND (d.setrole=0 OR r.rolname LIKE 'merlin_d6%' OR r.rolname='merlin_api')
 UNION ALL SELECT jsonb_build_object('rule',r.rulename,'table',r.ev_class::regclass::text,'enabled',r.ev_enabled,'definition',pg_get_ruledef(r.oid)) FROM pg_rewrite r WHERE r.ev_class IN ('public.users'::regclass,'public.notes'::regclass,'public.active_notes'::regclass)
 UNION ALL SELECT jsonb_build_object('inheritance',inhrelid::regclass::text,'parent',inhparent::regclass::text,'sequence',inhseqno) FROM pg_inherits WHERE inhrelid IN ('public.users'::regclass,'public.notes'::regclass) OR inhparent IN ('public.users'::regclass,'public.notes'::regclass)

) AS definitions;
"""


def run_sql(module, script):
    if re.search(r"\bCOMMIT\b", script, re.I):
        raise ValueError("Mutation scripts must never commit")
    try:
        from tools.native_psql import run as native_run
        runner = SESSION.run if SESSION is not None else native_run
        result = runner(module.COMMAND, input=script, capture_output=True, text=True, timeout=30)
        return {"exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"exit": None, "stdout": "", "stderr": "Timed out; not a detected fault"}


def preservation(module):
    result = run_sql(module, "SELECT current_database(),system_identifier FROM pg_control_system();\n"
                     "SELECT (SELECT count(*) FROM public.users),(SELECT count(*) FROM public.notes);\n" + FINGERPRINT)
    lines = result["stdout"].splitlines()
    if result["exit"] or lines[:2] != ["merlin_d6|" + module.CLUSTER, "0|0"] or len(lines) != 3:
        raise RuntimeError("Identity, empty-table or fingerprint gate failed; preserve storage")
    return lines[-1]


def shard_argument(value):
    if not re.fullmatch(r"[0-9]+/[0-9]+", value):
        raise argparse.ArgumentTypeError("Shard must be INDEX/TOTAL with zero-based integers")
    index, total = map(int, value.split("/"))
    if total < 1 or not 0 <= index < total:
        raise argparse.ArgumentTypeError("Shard requires TOTAL >= 1 and 0 <= INDEX < TOTAL")
    return index, total


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--only", help="Substring of case IDs")
    parser.add_argument("--shard", type=shard_argument,
                        help="Zero-based INDEX/TOTAL; case position modulo TOTAL selects its independent copy")
    args = parser.parse_args()
    if args.only is not None and args.shard is not None:
        parser.error("--only and --shard cannot be combined")
    return args


def audit_main(args=None):
    args = parse_arguments() if args is None else args
    module, setup = load_cases()
    original = preservation(module)
    results = []
    try:
        for position, case in enumerate(module.CASES):
            if args.only and args.only not in case.id:
                continue
            if args.shard is not None and position % args.shard[1] != args.shard[0]:
                continue
            values = {key: str(uuid.uuid4()) for key in ["a", "b", "n", "other", "extra", "missing"]}
            values.update(name_a="audit_a_" + uuid.uuid4().hex[:8], name_b="audit_b_" + uuid.uuid4().hex[:8])
            start, body = setup.format(**values), case.sql.format(**values)
            baseline = run_sql(module, start + body + "\nSELECT 'CASE_PASS';\nROLLBACK;\n")
            row = {"case": case.id, "rule": case.rule, "baseline": baseline, "faults": []}
            if baseline["exit"] or baseline["stdout"].splitlines()[-1:] != ["CASE_PASS"]:
                row["effectiveness"] = "BASELINE_FAIL"
            else:
                for fault in recipes(case):
                    if fault["before_seed"]:
                        marker = "INSERT INTO public.users"
                        mutated = start.replace(marker, fault["sql"] + "\nSELECT 'MUTATION_READY';\n" + marker, 1)
                    else:
                        mutated = start + fault["sql"] + "\nSELECT 'MUTATION_READY';\n"
                    run = run_sql(module, mutated + body + "\nSELECT 'CASE_PASS';\nROLLBACK;\n")
                    ready = "MUTATION_READY" in run["stdout"].splitlines()
                    if not ready:
                        status = "UNAPPLIED" if "UNAPPLIED" in run["stderr"] else "INVALID"
                    elif run["exit"] is None:
                        status = "TIMEOUT"
                    elif run["exit"] == 0:
                        status = "SURVIVED"
                    else:
                        status = "DETECTED_ASSERTION" if "ASSERTION:" in run["stderr"] else "DETECTED_BEHAVIOR_ERROR"
                    row["faults"].append({**fault, "status": status, **run})
                row["effectiveness"] = "DEMONSTRATED" if any(f["status"].startswith("DETECTED") for f in row["faults"]) else "NO_MATCHING_DETECTION"
            results.append(row)
            if len(results) % 20 == 0:
                print(f"Audited {len(results)} SQL cases", flush=True)
        # Exercise the separate reconnect/rollback test's actual Python assertions.
        if not args.only and (args.shard is None or args.shard[0] == 0):
            # Reconnect is a feature under test: close the reused session first.
            if SESSION is not None:
                SESSION.close()
                globals()['SESSION'] = None
            module.test_failed_second_write_rolls_back_first_write_after_reconnect()
            original_run = subprocess.run
            committed_user = None
            def premature_commit(*positional, **keywords):
                nonlocal committed_user
                text = keywords.get("input", "")
                if "Unexpected success" in text:
                    match = re.search(r"INSERT INTO public.users\(id,username\) VALUES \('([0-9a-f-]{36})'", text)
                    if match is None:
                        raise RuntimeError("Reconnect mutation did not identify its synthetic user")
                    committed_user = match.group(1)
                    keywords["input"] = text.replace("INSERT INTO public.notes", "COMMIT; BEGIN;\nINSERT INTO public.notes", 1)
                return original_run(*positional, **keywords)
            try:
                with patch.object(module.subprocess, "run", side_effect=premature_commit):
                    module.test_failed_second_write_rolls_back_first_write_after_reconnect()
            except AssertionError:
                detected = True
            else:
                detected = False
            finally:
                if committed_user is not None:
                    # The fault commits only its synthetic row, never schema changes.
                    cleanup = original_run(module.COMMAND,
                        input="BEGIN;\nDO $gate$ BEGIN IF current_database()<>'merlin_d6' OR "
                              "(SELECT system_identifier::text FROM pg_control_system())<>'" + module.CLUSTER +
                              "' THEN RAISE EXCEPTION 'Unexpected reconnect cleanup target'; END IF; END $gate$;\n"
                              "DELETE FROM public.users WHERE id='" + committed_user + "';\nCOMMIT;\n",
                        capture_output=True, text=True, timeout=30)
                    if cleanup.returncode != 0:
                        raise RuntimeError("Reconnect fault cleanup failed; preserve storage and investigate")
            results.append({"case": "test_failed_second_write_rolls_back_first_write_after_reconnect", "rule": "Failed second write rolls back first after reconnect", "baseline": {"exit": 0}, "effectiveness": "DEMONSTRATED" if detected else "NO_MATCHING_DETECTION", "faults": [{"name": "premature-first-write-commit", "status": "DETECTED_ASSERTION" if detected else "SURVIVED"}]})
    finally:
        final = preservation(module)
        payload = {"source_sha256": hashlib.sha256((ROOT / "tests/test_users_notes_database.py").read_bytes()).hexdigest(),
                   "original_fingerprint": original, "final_fingerprint": final, "preserved": original == final, "cases": results}
        if args.shard is not None:
            index, total = args.shard
            payload["shard"] = {"index": index, "total": total,
                                "ordinary_case_count": len(module.CASES),
                                "ordinary_case_ids": [case.id for position, case in enumerate(module.CASES)
                                                      if position % total == index],
                                "includes_reconnect": index == 0}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n")
        if original != final:
            raise RuntimeError("SQL audit changed persistent definitions; investigate before further work")
    print(json.dumps({"cases": len(results), "demonstrated": sum(r["effectiveness"] == "DEMONSTRATED" for r in results), "baseline_failures": sum(r["effectiveness"] == "BASELINE_FAIL" for r in results), "preserved": original == final}))


def main():
    global SESSION
    # Reject malformed/ambiguous selections before opening any database transport.
    args = parse_arguments()
    if os.environ.get('MERLIN_FAST_DB_TESTS') == '1':
        from tools.database_test_session import DatabaseTestSession
        with DatabaseTestSession() as session:
            SESSION = session
            try:
                audit_main(args)
            finally:
                SESSION = None
    else:
        audit_main(args)


if __name__ == "__main__":
    main()
