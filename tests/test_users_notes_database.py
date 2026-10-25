"""Opt-in PostgreSQL checks: synthetic rows, fixed disposable cluster, always rollback.

Run with MERLIN_RUN_DB_TESTS=1. These tests never apply a migration, change stored
functions, commit data, or connect to the preserved Sprint 0 project.
"""

import os
import subprocess
import uuid
from dataclasses import dataclass

import pytest


PROJECT = "merlin-d6-20261008105707"
CLUSTER = "7694311451826794534"
COMMAND = ["docker", "compose", "-p", PROJECT, "exec", "-T", "postgres",
           "psql", "-X", "-qAt", "-U", "merlin_d6", "-d", "merlin_d6",
           "-v", "ON_ERROR_STOP=1"]
pytestmark = pytest.mark.skipif(os.environ.get("MERLIN_RUN_DB_TESTS") != "1",
                                reason="Disposable PostgreSQL checks require explicit opt-in")


@dataclass(frozen=True)
class Case:
    id: str
    rule: str
    sql: str


def require(condition, description):
    # IS NOT TRUE also rejects NULL; SQL's unknown result cannot pass an assertion.
    return f"IF ({condition}) IS NOT TRUE THEN RAISE EXCEPTION 'ASSERTION: {description}'; END IF;"


def check(condition, description="Expected database state was not observed"):
    return "DO $check$ BEGIN " + require(condition, description) + " END $check$;"


def reject(statement, state, *, constraint=None, message=None, column=None):
    # Only the intended SQLSTATE counts. A syntax/permission/connection error is a failure.
    expected = ""
    if constraint:
        expected += require(f"got_constraint = '{constraint}'", "Wrong constraint rejected the write")
    if column:
        expected += require(f"got_column = '{column}'", "Wrong required column rejected the write")
    if message:
        expected += require(f"SQLERRM = '{message}'", "Wrong trigger rejected the write")
    return f"""DO $negative$
DECLARE caught BOOLEAN := false; got_constraint TEXT; got_column TEXT;
BEGIN
    BEGIN
        {statement};
    EXCEPTION WHEN SQLSTATE '{state}' THEN
        caught := true;
        GET STACKED DIAGNOSTICS got_constraint = CONSTRAINT_NAME, got_column = COLUMN_NAME;
        {expected}
    END;
    IF NOT caught THEN RAISE EXCEPTION 'ASSERTION: Expected rejection {state}'; END IF;
END $negative$;"""


def note_insert(columns="", values=""):
    return ("INSERT INTO public.notes (id,user_id,title,body,device_created_at,device_edited_at" + columns + ") "
            "VALUES ('{extra}','{a}','New title','new body','2026-01-01 UTC','2026-01-01 UTC'" + values + ")")


def seed_history(assignments):
    # Test fixture only: seed past times without waiting 14 days. Undo is transaction rollback.
    # No trigger/function is altered. The setting is restored before behavior is tested.
    return ("SET LOCAL session_replication_role = replica; "
            "UPDATE public.notes SET " + assignments + " WHERE id='{n}'; "
            "SET LOCAL session_replication_role = origin; ")


SESSION = None
CASES = []


def add(id, rule, sql):
    CASES.append(Case(id, rule, sql))


# MER-12 authentication schema checks. These cases run only in the project's
# guarded disposable PostgreSQL target. They verify least privilege and expiry
# enforcement in PostgreSQL, rather than trusting Python helpers alone.
_auth_seed = "INSERT INTO public.auth_credentials(user_id,password_hash) VALUES " \
             "('{a}','$argon2id$'||repeat('a',40)),('{b}','$argon2id$'||repeat('b',40));"
add("auth-lookup-exact-name", "Login lookup returns one matching account hash",
    _auth_seed + "SET LOCAL ROLE merlin_api; "
    "DO $auth$ DECLARE found RECORD; BEGIN "
    "SELECT * INTO found FROM public.lookup_auth_credential('{name_b}'); "
    + require("found.user_id = '{b}'::uuid AND found.password_hash = '$argon2id$'||repeat('b',40)",
              "Login lookup returned the wrong credential") + " END $auth$; RESET ROLE;")
add("auth-lookup-unknown-user-empty", "Unknown login names return no credential",
    _auth_seed + "SET LOCAL ROLE merlin_api; "
    "DO $auth$ BEGIN "
    + require("NOT EXISTS(SELECT 1 FROM public.lookup_auth_credential('no_such_user'))",
              "Unknown login name returned a credential") + " END $auth$; RESET ROLE;")
add("auth-credentials-not-directly-readable", "Runtime role cannot scan password hashes",
    _auth_seed + "SET LOCAL ROLE merlin_api; "
    + reject("SELECT password_hash FROM public.auth_credentials WHERE user_id='{a}'",
             "42501") + " RESET ROLE;")
add("runtime-role-cannot-read-notes", "Authentication runtime role has no note-table access",
    "SET LOCAL ROLE merlin_api; SELECT set_config('merlin.actor_id','{a}',true); "
    + reject("SELECT body FROM public.notes WHERE user_id='{a}'", "42501") + " RESET ROLE;")
add("auth-refresh-family-owner-filter", "Refresh families remain isolated by trusted actor policy",
    "INSERT INTO public.auth_refresh_families(id,user_id,idle_expires_at,absolute_expires_at) VALUES "
    "('{n}','{a}',statement_timestamp()+interval '30 days',statement_timestamp()+interval '90 days'),"
    "('{extra}','{b}',statement_timestamp()+interval '30 days',statement_timestamp()+interval '90 days'); "
    "SET LOCAL ROLE merlin_api; SELECT set_config('merlin.actor_id','{a}',true); "
    + check("NOT EXISTS(SELECT 1 FROM public.auth_refresh_families WHERE id='{extra}')") + " RESET ROLE;")
add("auth-refresh-idle-expiry-cap", "Idle refresh expiry never exceeds 30 days from now",
    reject("INSERT INTO public.auth_refresh_families(id,user_id,idle_expires_at,absolute_expires_at) "
           "VALUES ('{n}','{a}',statement_timestamp()+interval '31 days',statement_timestamp()+interval '90 days')",
           "23514", message="Invalid authentication session expiry"))
add("auth-refresh-absolute-expiry-cap", "Absolute refresh expiry never exceeds 90 days from creation",
    reject("INSERT INTO public.auth_refresh_families(id,user_id,idle_expires_at,absolute_expires_at) "
           "VALUES ('{n}','{a}',statement_timestamp()+interval '30 days',statement_timestamp()+interval '91 days')",
           "23514", message="Invalid authentication session expiry"))
add("auth-refresh-token-expiry-bound", "Refresh token cannot outlive its device family",
    "INSERT INTO public.auth_refresh_families(id,user_id,idle_expires_at,absolute_expires_at) "
    "VALUES ('{extra}','{a}',statement_timestamp()+interval '15 days',statement_timestamp()+interval '90 days'); "
    + reject("INSERT INTO public.auth_refresh_tokens(token_hash,family_id,expires_at) "
             "VALUES (decode(repeat('ab',32),'hex'),'{extra}',statement_timestamp()+interval '16 days')",
             "23514", message="Invalid authentication refresh token"))
add("auth-refresh-token-consumed-once", "Consumed refresh tokens cannot be rotated twice",
    "INSERT INTO public.auth_refresh_families(id,user_id,idle_expires_at,absolute_expires_at) "
    "VALUES ('{extra}','{a}',statement_timestamp()+interval '30 days',statement_timestamp()+interval '90 days'); "
    "INSERT INTO public.auth_refresh_tokens(token_hash,family_id,created_at,expires_at) VALUES "
    "(decode(repeat('01',32),'hex'),'{extra}',statement_timestamp()-interval '1 hour',statement_timestamp()+interval '10 days'), "
    "(decode(repeat('02',32),'hex'),'{extra}',statement_timestamp(),statement_timestamp()+interval '10 days'); "
    "UPDATE public.auth_refresh_tokens SET consumed_at=statement_timestamp(), "
    "replaced_by_hash=decode(repeat('02',32),'hex') WHERE token_hash=decode(repeat('01',32),'hex'); "
    + reject("UPDATE public.auth_refresh_tokens SET consumed_at=statement_timestamp() "
             "WHERE token_hash=decode(repeat('01',32),'hex')",
             "23514", message="Invalid refresh-token rotation"))


# Unicode counts use independent expected answers, not the Python helper's output.
for name, text, weight in [("plain", "abc", 3), ("emoji", "😀", 4), ("family", "👨‍👩‍👧‍👦", 4),
                           ("skin", "👍🏽", 4), ("flag", "🇺🇸", 4), ("keycap", "1️⃣", 4),
                           ("accent", "e\u0301", 1), ("cjk", "中文", 2), ("empty", "", 0)]:
    add("F015-" + name, "Database uses the pinned grapheme-weighting rule",
        check(f"public.note_weighted_length('{text}') = {weight}", "Wrong Unicode weight"))


# Both valid boundaries and invalid writes protect against overly strict or weak checks.
for field, limit, constraint in [("title", 175, "notes_title_limit"), ("body", 7000, "notes_body_limit")]:
    for size in [limit - 1, limit, limit + 1]:
        write = f"UPDATE public.notes SET {field}=repeat('a',{size}) WHERE id='{{n}}'"
        sql = (write + ";" + check(f"(SELECT {field}=repeat('a',{size}) FROM public.notes WHERE id='{{n}}')")
               if size <= limit else reject(write, "23514", constraint=constraint))
        add(f"limit-{field}-{size}", "Weighted text limit also applies to updates", sql)
    add(f"F0{'20' if field == 'title' else '21'}", "Combining graphemes fit at the limit",
        f"UPDATE public.notes SET {field}=repeat('é',{limit}) WHERE id='{{n}}';" +
        check(f"(SELECT {field}=repeat('é',{limit}) FROM public.notes WHERE id='{{n}}')"))
    add(f"draft-{field}-overflow", "Drafts cannot bypass text limits",
        reject(note_insert(",is_draft", ",true").replace("'New title'" if field == "title" else "'new body'",
               f"repeat('😀',{limit // 4 + 1})"), "23514", constraint=constraint))
    add(f"emoji-{field}-overflow", "Emoji weigh four in direct SQL",
        reject(f"UPDATE public.notes SET {field}=repeat('😀',{limit // 4 + 1}) WHERE id='{{n}}'",
               "23514", constraint=constraint))

add("F031", "Blank titles normalize to NULL and preserve body", "UPDATE public.notes SET title=E' \\t\\n' WHERE id='{n}';" +
    check("(SELECT title IS NULL AND body='original body' FROM public.notes WHERE id='{n}')"))
add("F033", "Nonblank title whitespace is preserved", "UPDATE public.notes SET title='  Keep  ' WHERE id='{n}';" +
    check("(SELECT title='  Keep  ' FROM public.notes WHERE id='{n}')"))
add("F034", "Body whitespace is preserved", "UPDATE public.notes SET body=E'  Body\\n ' WHERE id='{n}';" +
    check("(SELECT body=E'  Body\\n ' FROM public.notes WHERE id='{n}')"))
add("F036", "Fully blank saved rows reject", reject("UPDATE public.notes SET title=NULL,body='' WHERE id='{n}'",
    "23514", constraint="notes_has_content") + check("(SELECT title='Original' AND body='original body' FROM public.notes WHERE id='{n}')"))
add("F037", "Fully blank drafts are permitted without countdown", note_insert(",is_draft", ",true").replace("'New title'", "NULL").replace("'new body'", "''") + ";" +
    check("(SELECT is_draft AND title IS NULL AND body='' AND blank_body_expires_at IS NULL FROM public.notes WHERE id='{extra}')"))
add("F038", "Title-only notes persist with a one-day deadline", "UPDATE public.notes SET body='' WHERE id='{n}';" +
    check("(SELECT title='Original' AND blank_body_expires_at = updated_at + interval '24 hours' FROM public.notes WHERE id='{n}')"))
add("F039", "Body-only notes persist", "UPDATE public.notes SET title=NULL WHERE id='{n}';" +
    check("(SELECT title IS NULL AND body='original body' AND deleted_at IS NULL FROM public.notes WHERE id='{n}')"))
add("F040", "Spaces and blank lines do not make saved content", reject("UPDATE public.notes SET title=E' \\t',body=E'\\n ' WHERE id='{n}'", "23514", constraint="notes_has_content"))

add("F049-F050", "Multiple users can omit email", "INSERT INTO public.users(id,username) VALUES ('{extra}','audit_null_one'),('{missing}','audit_null_two');" + check("(SELECT count(*)=2 FROM public.users WHERE id IN ('{extra}','{missing}') AND email IS NULL)"))
add("F051", "Case variants of an email are duplicates",
    "UPDATE public.users SET email='Mixed@Example.test' WHERE id='{a}';" +
    reject("UPDATE public.users SET email='mixed@example.TEST' WHERE id='{b}'", "23505", constraint="users_email_unique") +
    check("(SELECT email='Mixed@Example.test' FROM public.users WHERE id='{a}') AND (SELECT email IS NULL FROM public.users WHERE id='{b}')"))
add("email-insert-duplicate", "Email uniqueness also rejects a new user",
    "UPDATE public.users SET email='a@example.test' WHERE id='{a}';" +
    reject("INSERT INTO public.users (username,email) VALUES ('audit_new','A@example.test')", "23505", constraint="users_email_unique"))
for name, email in [("blank", "''"), ("spaces", "'  '"), ("leading", "' a@example.test'"), ("trailing", "'a@example.test '")]:
    add("email-" + name, "Direct SQL email must be nonblank and unpadded",
        reject(f"UPDATE public.users SET email={email} WHERE id='{{a}}'", "23514", constraint="users_email_clean"))
for name, username, state, constraint in [
    ("null", "NULL", "23502", None), ("upper", "'Upper'", "23514", "users_username_format"),
    ("empty", "''", "23514", "users_username_format"), ("twenty-one", "repeat('a',21)", "23514", "users_username_format"),
    ("punctuation", "'a-b'", "23514", "users_username_format")]:
    add("username-" + name, "Username is required lowercase ASCII with a 20-character cap",
        reject(f"UPDATE public.users SET username={username} WHERE id='{{a}}'", state, constraint=constraint, column="username" if name == "null" else None))
add("username-twenty", "Twenty-character username accepts and canonical lookup agrees",
    "UPDATE public.users SET username=repeat('z',20) WHERE id='{a}';" +
    check("(SELECT username=repeat('z',20) AND username_canonical=username FROM public.users WHERE id='{a}')"))
add("username-duplicate", "Duplicate username is rejected", reject("UPDATE public.users SET username='{name_a}' WHERE id='{b}'", "23505", constraint="users_username_unique"))
add("F059", "Canonical username cannot be supplied independently", reject("UPDATE public.users SET username_canonical='different' WHERE id='{a}'", "428C9"))
add("F061-user", "Successive user default IDs are distinct UUIDv4 values", "INSERT INTO public.users(username) VALUES ('audit_default'),('audit_default_next');" +
    check("(SELECT count(*)=2 AND count(DISTINCT id)=2 AND bool_and(id IS NOT NULL AND substring(id::text,15,1)='4' AND substring(id::text,20,1) IN ('8','9','a','b')) FROM public.users WHERE username IN ('audit_default','audit_default_next'))"))
add("F061-note", "Successive note default IDs are distinct independent UUIDv4 values", "INSERT INTO public.notes(user_id,title,body,device_created_at,device_edited_at) VALUES ('{a}','default','body',now(),now()),('{a}','default_next','body',now(),now());" +
    check("(SELECT count(*)=2 AND count(DISTINCT id)=2 AND bool_and(id IS NOT NULL AND id <> user_id AND substring(id::text,15,1)='4' AND substring(id::text,20,1) IN ('8','9','a','b')) FROM public.notes WHERE user_id='{a}' AND title IN ('default','default_next'))"))
for table in ["users", "notes"]:
    for name, bad_id in [("version", "11111111-1111-7111-8111-111111111111"), ("variant", "11111111-1111-4111-0111-111111111111")]:
        statement = ("INSERT INTO public.users(id,username) VALUES ('" + bad_id + "','audit_invalid')" if table == "users"
                     else note_insert().replace("'{extra}'", "'" + bad_id + "'"))
        add("uuid-" + table + "-" + name, "Explicit IDs must have UUIDv4 version and variant",
            reject(statement, "23514", constraint=table + "_id_uuidv4"))
add("F064", "Duplicate note ID rejects", reject(note_insert().replace("'{extra}'", "'{n}'"), "23505", constraint="notes_pkey"))
add("F065", "Owner is required", reject(note_insert().replace("'{a}'", "NULL"), "23502", column="user_id"))
add("F066", "Owner must exist", reject(note_insert().replace("'{a}'", "'{missing}'"), "23503", constraint="notes_user_id_fkey"))
add("F067", "Deleting one user cascades only their notes", "DELETE FROM public.users WHERE id='{a}';" +
    check("NOT EXISTS(SELECT 1 FROM public.notes WHERE user_id='{a}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{other}') AND EXISTS(SELECT 1 FROM public.users WHERE id='{b}')"))
for id, table, field, new, message in [
    ("F068", "notes", "user_id", "'{b}'", "Note ownership cannot be transferred"),
    ("F069", "users", "id", "'{extra}'", "ID and creation time cannot be changed"),
    ("F070", "notes", "id", "'{extra}'", "ID and creation time cannot be changed"),
    ("F078", "users", "created_at", "'1900-01-01 UTC'", "ID and creation time cannot be changed"),
    ("F079", "notes", "created_at", "'1900-01-01 UTC'", "ID and creation time cannot be changed"),
    ("F080", "notes", "device_created_at", "'1900-01-01 UTC'", "Device creation time cannot be changed")]:
    row = "missing" if id == "F069" else "a" if table == "users" else "n"
    independent_user = "INSERT INTO public.users(id,username) VALUES ('{missing}','audit_unreferenced');" if id == "F069" else ""
    add(id, "Immutable identity/creation fields cannot be changed",
        independent_user + reject(f"UPDATE public.{table} SET {field}={new} WHERE id='{{{row}}}'", "23514", message=message))

# SET ROLE proves the database boundary under an explicitly supplied actor, not login/auth.
APP = "SET LOCAL ROLE merlin_d6_app; SET LOCAL merlin.actor_id='{a}';"
add("F071", "App role sees only its actor's rows", APP + check("(SELECT count(*)=1 FROM public.notes) AND (SELECT count(*)=1 FROM public.users) AND NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')"))
add("F072", "App cannot edit another actor's note", APP + "UPDATE public.notes SET body='stolen' WHERE id='{other}';RESET ROLE;" +
    check("(SELECT body='other body' FROM public.notes WHERE id='{other}')"))
add("F073", "App cannot insert for another actor", APP + reject(note_insert().replace("'{a}'", "'{b}'"), "42501"))
add("F074", "Missing actor sees no protected rows", "SET LOCAL ROLE merlin_d6_app; SET LOCAL merlin.actor_id='';" + check("NOT EXISTS(SELECT 1 FROM public.notes) AND NOT EXISTS(SELECT 1 FROM public.users)"))
add("F075-role", "App cannot escalate to object owner", "SET LOCAL SESSION AUTHORIZATION merlin_d6_app;" +
    check("session_user='merlin_d6_app' AND current_user='merlin_d6_app' AND NOT pg_has_role('merlin_d6_app','merlin_d6_owner','MEMBER')") +
    reject("SET LOCAL ROLE merlin_d6_owner", "42501"))
for field, value in [("id", "'{extra}'"), ("user_id", "'{b}'"), ("created_at", "now()"), ("updated_at", "now()"), ("blank_body_expires_at", "now()")]:
    add("app-column-" + field, "Column grants forbid app changes to protected fields",
        APP + reject(f"UPDATE public.notes SET {field}={value} WHERE id='{{n}}'", "42501"))
add("app-own-edit", "App can edit its own content", APP + "UPDATE public.notes SET body='allowed' WHERE id='{n}';" + check("(SELECT body='allowed' FROM public.notes WHERE id='{n}')"))
add("app-saved-delete", "App cannot permanently delete a saved note", APP + "DELETE FROM public.notes WHERE id='{n}';RESET ROLE;" + check("EXISTS(SELECT 1 FROM public.notes WHERE id='{n}')"))
add("app-blank-draft-delete", "App can delete its own blank draft", note_insert(",is_draft", ",true").replace("'New title'", "NULL").replace("'new body'", "''") + ";" +
    APP + "DELETE FROM public.notes WHERE id='{extra}';RESET ROLE;" + check("NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{extra}')"))
add("F076", "Device cannot forge server-created time", note_insert(",created_at,updated_at", ",'1900-01-01 UTC','1900-01-01 UTC'") + ";" +
    check("(SELECT created_at BETWEEN now() AND clock_timestamp() AND updated_at=created_at FROM public.notes WHERE id='{extra}')"))
add("F077", "Initial server times are equal", note_insert() + ";INSERT INTO public.users(id,username) VALUES ('{missing}','z{name_a}');" + check("(SELECT created_at=updated_at FROM public.notes WHERE id='{extra}') AND (SELECT created_at=updated_at FROM public.users WHERE id='{missing}')"))
add("F081", "Content edits advance server edit time", "UPDATE public.notes SET body='changed' WHERE id='{n}';" + check("(SELECT updated_at>created_at AND body='changed' FROM public.notes WHERE id='{n}')"))
add("F082", "No-op save keeps Last Edited", "UPDATE public.notes SET body=body WHERE id='{n}';" + check("(SELECT updated_at=created_at FROM public.notes WHERE id='{n}')"))
add("F083", "Hiding a note keeps Last Edited", "UPDATE public.notes SET deleted_at=now() WHERE id='{n}';" + check("(SELECT deleted_at IS NOT NULL AND updated_at=created_at FROM public.notes WHERE id='{n}')"))
add("F084", "Restoring a note keeps Last Edited", "UPDATE public.notes SET deleted_at=now() WHERE id='{n}';UPDATE public.notes SET deleted_at=NULL WHERE id='{n}';" + check("(SELECT deleted_at IS NULL AND updated_at=created_at FROM public.notes WHERE id='{n}')"))
add("F085", "Manual server edit time is overridden for no-op", "UPDATE public.notes SET updated_at='1900-01-01 UTC' WHERE id='{n}';" + check("(SELECT updated_at=created_at FROM public.notes WHERE id='{n}')"))
add("F086", "Initial device edit time equals device creation", note_insert().replace("'2026-01-01 UTC','2026-01-01 UTC'", "'1900-01-01 UTC','2200-01-01 UTC'") + ";" + check("(SELECT device_edited_at=device_created_at FROM public.notes WHERE id='{extra}')"))
add("F087", "Device time cannot control expiry", "UPDATE public.notes SET body='',device_edited_at='1900-01-01 UTC' WHERE id='{n}';" + check("(SELECT blank_body_expires_at=updated_at+interval '24 hours' FROM public.notes WHERE id='{n}')"))
add("F088", "Device time cannot control retention", "UPDATE public.notes SET deleted_at='1900-01-01 UTC',device_edited_at='2200-01-01 UTC' WHERE id='{n}';" + check("(SELECT deleted_at BETWEEN now() AND clock_timestamp() FROM public.notes WHERE id='{n}')"))
add("F089", "Different timezone offsets preserve an instant", note_insert().replace("'2026-01-01 UTC','2026-01-01 UTC'", "'2026-01-01 01:00+01','2026-01-01 00:00+00'") + ";" + check("(SELECT device_created_at='2026-01-01 00:00+00'::timestamptz FROM public.notes WHERE id='{extra}')"))
add("F090", "Device-only metadata update does not fake a text edit", "UPDATE public.notes SET device_edited_at='2200-01-01 UTC' WHERE id='{n}';" + check("(SELECT device_edited_at=device_created_at AND updated_at=created_at FROM public.notes WHERE id='{n}')"))

add("F092", "Title-only draft has no countdown", note_insert(",is_draft", ",true").replace("'new body'", "''") + ";" + check("(SELECT blank_body_expires_at IS NULL FROM public.notes WHERE id='{extra}')"))
add("F093", "Adding real body clears countdown", "UPDATE public.notes SET body='' WHERE id='{n}';UPDATE public.notes SET body='filled' WHERE id='{n}';" + check("(SELECT blank_body_expires_at IS NULL FROM public.notes WHERE id='{n}')"))
add("F094", "Returning to blank starts a new countdown", "UPDATE public.notes SET body='' WHERE id='{n}';" +
    "DO $restart$ DECLARE before_time timestamptz; BEGIN SELECT blank_body_expires_at INTO before_time FROM public.notes WHERE id='{n}';" +
    "UPDATE public.notes SET body='filled' WHERE id='{n}';" + require("(SELECT blank_body_expires_at IS NULL FROM public.notes WHERE id='{n}')", "Filled body retained countdown") +
    "UPDATE public.notes SET body='' WHERE id='{n}';" + require("(SELECT blank_body_expires_at>before_time AND blank_body_expires_at=statement_timestamp()+interval '24 hours' FROM public.notes WHERE id='{n}')", "Blank body did not restart deadline") + "END $restart$;")
for id, assignment in [("F095", "body=body"), ("F096", "title='new title'"), ("F097", "blank_body_expires_at='2200-01-01 UTC'"), ("F098", "blank_body_expires_at=NULL")]:
    add(id, "A saved blank-body deadline cannot be extended or removed", "UPDATE public.notes SET body='' WHERE id='{n}';" +
        "DO $deadline$ DECLARE before_time timestamptz; BEGIN SELECT blank_body_expires_at INTO before_time FROM public.notes WHERE id='{n}';" +
        "UPDATE public.notes SET " + assignment + " WHERE id='{n}';" + require("(SELECT blank_body_expires_at=before_time FROM public.notes WHERE id='{n}')", "Deadline changed") + "END $deadline$;")
add("F099", "Saved notes cannot become drafts", reject("UPDATE public.notes SET is_draft=true WHERE id='{n}'", "23514", message="Saved notes cannot become drafts"))
add("F100", "Worker cannot expire a future title-only note", "UPDATE public.notes SET body='' WHERE id='{n}';" + check("public.cleanup_expired_blank_notes(100)=0 AND EXISTS(SELECT 1 FROM public.notes WHERE id='{n}' AND deleted_at IS NULL)"))
add("F102", "Overdue title-only notes enter trash instead of disappearing", seed_history("body='',blank_body_expires_at=now()-interval '1 day'") + check("public.cleanup_expired_blank_notes(100)=1") + check("EXISTS(SELECT 1 FROM public.notes WHERE id='{n}' AND deleted_at IS NOT NULL)"))
add("F103", "Worker leaves filled notes alone", check("public.cleanup_expired_blank_notes(100)=0 AND (SELECT body='original body' AND deleted_at IS NULL FROM public.notes WHERE id='{n}')"))
add("F104", "Repeated expiry keeps first trash time", seed_history("body='',blank_body_expires_at=now()-interval '1 day'") + check("public.cleanup_expired_blank_notes(100)=1") +
    check("(SELECT deleted_at IS NOT NULL FROM public.notes WHERE id='{n}')", "First expiry did not trash the row") +
    "DO $again$ DECLARE first_time timestamptz; BEGIN SELECT deleted_at INTO first_time FROM public.notes WHERE id='{n}'; " + require("public.cleanup_expired_blank_notes(100)=0", "Repeated expiry selected trash") + require("(SELECT deleted_at=first_time FROM public.notes WHERE id='{n}')", "Expiry reset trash time") + "END $again$;")
add("F106", "New notes cannot be inserted into trash", reject(note_insert(",deleted_at", ",now()"), "23514", message="New notes cannot start in trash"))
add("F107", "Caller cannot forge deletion time", "UPDATE public.notes SET deleted_at='1900-01-01 UTC' WHERE id='{n}';" + check("(SELECT deleted_at BETWEEN now() AND clock_timestamp() FROM public.notes WHERE id='{n}')"))
add("F108", "Repeated hiding preserves first deletion time", "UPDATE public.notes SET deleted_at=now() WHERE id='{n}';" +
    "DO $hide$ DECLARE first_time timestamptz; BEGIN SELECT deleted_at INTO first_time FROM public.notes WHERE id='{n}';UPDATE public.notes SET deleted_at='2200-01-01 UTC' WHERE id='{n}';" + require("(SELECT deleted_at=first_time FROM public.notes WHERE id='{n}')", "Repeated hide changed trash time") + "END $hide$;")
add("F109", "Active view excludes trash", "UPDATE public.notes SET deleted_at=now() WHERE id='{n}';" + check("NOT EXISTS(SELECT 1 FROM public.active_notes WHERE id='{n}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{n}')"))
add("F110", "Fresh trash can be restored", "UPDATE public.notes SET deleted_at=now() WHERE id='{n}';UPDATE public.notes SET deleted_at=NULL WHERE id='{n}';" + check("EXISTS(SELECT 1 FROM public.active_notes WHERE id='{n}')"))
add("F112", "Restore after retention is rejected", seed_history("deleted_at=now()-interval '15 days'") + reject("UPDATE public.notes SET deleted_at=NULL WHERE id='{n}'", "23514", message="The restore period has ended"))
add("F113", "Fresh trash survives purge", seed_history("deleted_at=now()-interval '13 days'") + check("public.purge_deleted_notes(100)=0") + check("EXISTS(SELECT 1 FROM public.notes WHERE id='{n}')"))
add("F115", "Active rows survive purge", check("public.purge_deleted_notes(100)=0") + check("EXISTS(SELECT 1 FROM public.notes WHERE id='{n}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')"))
add("purge-overdue", "Overdue trash is removed", seed_history("deleted_at=now()-interval '15 days'") + check("public.purge_deleted_notes(100)=1") + check("NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{n}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')"))
add("F116", "Trashed body cannot be edited", "UPDATE public.notes SET deleted_at=now() WHERE id='{n}';" +
    reject("UPDATE public.notes SET body='edited in trash' WHERE id='{n}'", "23514", message="Restore the note before editing it"))
add("F117", "Trashed draft cannot be published", seed_history("is_draft=true,deleted_at=now()-interval '1 day'") +
    reject("UPDATE public.notes SET is_draft=false WHERE id='{n}'", "23514", message="Restore the note before editing it"))
add("F118", "Restored title-only note gets a new countdown", seed_history("body='',blank_body_expires_at=now()-interval '2 days',deleted_at=now()-interval '1 day'") + "DO $restore$ BEGIN UPDATE public.notes SET deleted_at=NULL WHERE id='{n}';" + require("(SELECT deleted_at IS NULL AND blank_body_expires_at=statement_timestamp()+interval '24 hours' FROM public.notes WHERE id='{n}')", "Restored deadline is not exactly 24 hours") + " END $restore$;")
for function in ["cleanup_expired_blank_notes", "purge_deleted_notes"]:
    for size in ["NULL", "0", "1001"]:
        add("sql-batch-" + function + "-" + size, "SQL cleanup refuses invalid batch sizes", reject(f"PERFORM public.{function}({size})", "P0001", message="Batch size must be between 1 and 1000"))

# Worker role can operate only on due rows and cannot delete recent trash.
add("maintenance-fresh-delete", "Maintenance cannot delete recent trash", "UPDATE public.notes SET deleted_at=now() WHERE id='{n}';SET LOCAL ROLE merlin_d6_maintenance;DELETE FROM public.notes WHERE id='{n}';RESET ROLE;" + check("EXISTS(SELECT 1 FROM public.notes WHERE id='{n}')"))
add("maintenance-active-read", "Maintenance cannot read non-due active content", "SET LOCAL ROLE merlin_d6_maintenance;" + check("NOT EXISTS(SELECT 1 FROM public.notes)"))
add("maintenance-overdue-purge", "Maintenance can purge only due trash", seed_history("deleted_at=now()-interval '15 days'") + "SET LOCAL ROLE merlin_d6_maintenance;" + check("public.purge_deleted_notes(100)=1") + "RESET ROLE;" + check("NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{n}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')"))
add("maintenance-expiry", "Maintenance can expire due rows", seed_history("body='',blank_body_expires_at=now()-interval '1 day'") + "SET LOCAL ROLE merlin_d6_maintenance;" + check("public.cleanup_expired_blank_notes(100)=1") + "RESET ROLE;" + check("(SELECT deleted_at IS NOT NULL FROM public.notes WHERE id='{n}')"))


add("F045-nbsp", "Python and SQL agree that nonbreaking-space-only body is blank",
    reject("UPDATE public.notes SET title=NULL,body=U&'\\00A0' WHERE id='{n}'", "23514", constraint="notes_has_content"))
add("F053-nbsp", "Direct SQL rejects nonbreaking-space padding on email",
    reject("UPDATE public.users SET email=U&'\\00A0a@example.test\\00A0' WHERE id='{a}'", "23514", constraint="users_email_clean"))
add("F091", "New title-only note starts exactly one day after server creation",
    note_insert().replace("'new body'", "''") + ";" +
    check("(SELECT blank_body_expires_at=created_at+interval '24 hours' AND deleted_at IS NULL FROM public.notes WHERE id='{extra}')"))
add("F101", "Expiry includes the exact server-statement deadline", "DO $at_due$ BEGIN " +
    "PERFORM set_config('session_replication_role','replica',true); UPDATE public.notes SET body='',blank_body_expires_at=statement_timestamp() WHERE id='{n}';" +
    "PERFORM set_config('session_replication_role','origin',true);" +
    require("public.cleanup_expired_blank_notes(100)=1", "Exact deadline was not expired") +
    require("EXISTS(SELECT 1 FROM public.notes WHERE id='{n}' AND deleted_at IS NOT NULL)", "Due note did not enter trash") + "END $at_due$;")
add("F114", "Purge includes the exact retention boundary", "DO $at_purge$ BEGIN " +
    "PERFORM set_config('session_replication_role','replica',true); UPDATE public.notes SET deleted_at=statement_timestamp()-interval '14 days' WHERE id='{n}';" +
    "PERFORM set_config('session_replication_role','origin',true);" + require("public.purge_deleted_notes(100)=1", "Exact retention boundary was not purged") +
    require("NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{n}')", "Due trash remains") + "END $at_purge$;")


add("app-own-insert", "App can insert for its own actor", APP + note_insert() + ";" +
    check("(SELECT user_id='{a}' AND title='New title' AND body='new body' FROM public.notes WHERE id='{extra}')"))
add("app-crossuser-delete", "App cannot delete another user's account or note", APP +
    "DELETE FROM public.notes WHERE id='{other}';DELETE FROM public.users WHERE id='{b}';RESET ROLE;" +
    check("EXISTS(SELECT 1 FROM public.users WHERE id='{b}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')"))
add("app-unset-actor", "Unset actor fails closed", "SET LOCAL ROLE merlin_d6_app;" +
    check("NOT EXISTS(SELECT 1 FROM public.users) AND NOT EXISTS(SELECT 1 FROM public.notes)"))
add("app-active-view", "Active view preserves the actor boundary", APP +
    check("(SELECT count(*)=1 FROM public.active_notes) AND NOT EXISTS(SELECT 1 FROM public.active_notes WHERE id='{other}')"))
for field, placeholder in [("body", "'new body'"), ("device_created_at", "'2026-01-01 UTC','2026-01-01 UTC'"), ("is_draft", None)]:
    if field == "is_draft":
        statement = note_insert(",is_draft", ",NULL")
    elif field == "device_created_at":
        statement = note_insert().replace(placeholder, "NULL,'2026-01-01 UTC'")
    else:
        statement = note_insert().replace(placeholder, "NULL")
    add("required-" + field, "Required note data cannot be NULL", reject(statement, "23502", column=field))
add("permission-groups", "All permission groups lack administrative or login powers",
    check("(SELECT count(*)=3 AND bool_and(NOT rolcanlogin AND NOT rolsuper AND NOT rolcreatedb AND NOT rolcreaterole AND NOT rolreplication AND NOT rolbypassrls) FROM pg_roles WHERE rolname IN ('merlin_d6_owner','merlin_d6_app','merlin_d6_maintenance')) AND (SELECT rolcanlogin AND NOT rolinherit AND NOT rolsuper AND NOT rolcreatedb AND NOT rolcreaterole AND NOT rolreplication AND NOT rolbypassrls AND NOT pg_has_role('merlin_api','merlin_d6_app','MEMBER') FROM pg_roles WHERE rolname='merlin_api')"))
add("rls-forced", "Both tables have forced row policies",
    check("(SELECT count(*)=2 AND bool_and(relrowsecurity AND relforcerowsecurity) FROM pg_class WHERE oid IN ('public.users'::regclass,'public.notes'::regclass))"))
add("app-no-cleanup-grant", "App cannot execute maintenance functions", APP + reject("PERFORM public.cleanup_expired_blank_notes(100)", "42501"))
add("app-no-purge-grant", "App cannot execute purge", APP + reject("PERFORM public.purge_deleted_notes(100)", "42501"))
add("app-no-schema-create", "App cannot create public schema objects", APP + reject("CREATE TABLE public.audit_forbidden(id integer)", "42501"))
for name, keys, descending in [
    ("created", ["user_id", "created_at"], 1),
    ("edited", ["user_id", "updated_at", "id"], 1),
    ("device", ["user_id", "device_edited_at", "id"], 1),
    ("draft", ["user_id", "is_draft", "updated_at", "id"], 2),
]:
    expected_keys = "ARRAY[" + ",".join("'" + key + "'" for key in keys) + "]::text[]"
    options = " AND ".join(f"i.indoption[{position}]={3 if position == descending else 0}" for position in range(len(keys)))
    predicate = ("regexp_replace(pg_get_expr(i.indpred,i.indrelid),'[()[:space:]]','','g')='deleted_atISNULL'"
                 if name == "draft" else "i.indpred IS NULL")
    add("index-" + name, "Timeline index has valid owner/order keys and intended predicate",
        check("EXISTS(SELECT 1 FROM pg_index i JOIN pg_class ic ON ic.oid=i.indexrelid "
              "JOIN pg_am am ON am.oid=ic.relam WHERE i.indrelid='public.notes'::regclass "
              f"AND i.indisvalid AND i.indisready AND am.amname='btree' AND i.indnkeyatts={len(keys)} AND i.indnatts={len(keys)} "
              "AND ARRAY(SELECT a.attname::text FROM unnest(i.indkey) WITH ORDINALITY AS k(attnum,position) "
              "JOIN pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=k.attnum ORDER BY k.position)=" +
              expected_keys + " AND " + options + " AND " + predicate + ")"))


add("app-delete-account-cascade", "Deleting one's own account removes saved notes too", APP +
    "DELETE FROM public.users WHERE id='{a}';RESET ROLE;" +
    check("NOT EXISTS(SELECT 1 FROM public.users WHERE id='{a}') AND NOT EXISTS(SELECT 1 FROM public.notes WHERE user_id='{a}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')"))


# Batch-one aliases use the identical oldest-row cases below; their LIMIT
# and ordering mutations both remain in the audit catalogue.
for function in ["cleanup_expired_blank_notes", "purge_deleted_notes"]:
    for size in [1000]:
        expiry = function == "cleanup_expired_blank_notes"
        first_history = "body='',blank_body_expires_at=now()-interval '2 days'" if expiry else "deleted_at=now()-interval '16 days'"
        second_history = "body='',blank_body_expires_at=now()-interval '1 day'" if expiry else "deleted_at=now()-interval '15 days'"
        first_state = "(SELECT deleted_at IS NOT NULL FROM public.notes WHERE id='{n}')" if expiry else "NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{n}')"
        second_state = ("(SELECT deleted_at IS " + ("NULL" if size == 1 else "NOT NULL") + " FROM public.notes WHERE id='{other}')"
                        if expiry else ("EXISTS" if size == 1 else "NOT EXISTS") + "(SELECT 1 FROM public.notes WHERE id='{other}')")
        add(f"sql-valid-batch-{function}-{size}", "SQL accepts both valid batch boundaries and changes the exact eligible rows",
            seed_history(first_history) + seed_history(second_history).replace("WHERE id='{n}'", "WHERE id='{other}'") +
            check(f"public.{function}({size})={min(size, 2)}") + check(first_state + " AND " + second_state))
add("expiry-batch-one", "Expiry processes the oldest due row and respects batch one",
    seed_history("body='',blank_body_expires_at=now()-interval '2 days'") +
    seed_history("body='',blank_body_expires_at=now()-interval '1 day'").replace("WHERE id='{n}'", "WHERE id='{other}'") +
    check("public.cleanup_expired_blank_notes(1)=1") +
    check("(SELECT deleted_at IS NOT NULL FROM public.notes WHERE id='{n}') AND (SELECT deleted_at IS NULL FROM public.notes WHERE id='{other}')"))
add("purge-batch-one", "Purge processes the oldest trash and respects batch one",
    seed_history("deleted_at=now()-interval '16 days'") +
    seed_history("deleted_at=now()-interval '15 days'").replace("WHERE id='{n}'", "WHERE id='{other}'") +
    check("public.purge_deleted_notes(1)=1") +
    check("NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{n}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')"))
add("note-body-default", "Omitted body defaults to empty text and gets a saved countdown",
    "INSERT INTO public.notes(id,user_id,title,device_created_at,device_edited_at) VALUES ('{extra}','{a}','Title',now(),now());" +
    check("(SELECT body='' AND NOT is_draft AND blank_body_expires_at=created_at+interval '24 hours' FROM public.notes WHERE id='{extra}')"))
add("user-id-duplicate", "A duplicate user ID rejects even with a different username",
    reject("INSERT INTO public.users(id,username) VALUES ('{a}','audit_id_duplicate')", "23505", constraint="users_pkey"))
add("user-clock-forged", "User server clocks also override device-forged insert values",
    "INSERT INTO public.users(id,username,created_at,updated_at) VALUES ('{extra}','audit_clock','1900-01-01 UTC','2200-01-01 UTC');" +
    check("(SELECT created_at BETWEEN now() AND clock_timestamp() AND updated_at=created_at FROM public.users WHERE id='{extra}')"))


# Follow the confirmed Unicode mismatch into every affected current behavior.
# Five older NBSP checks are consolidated into their parity-U+00A0 successors
# below. Those retain the same inputs, roles and rejection diagnostics, with
# additional body-preservation and other-owner assertions where appropriate.


# Every current Python whitespace class must also reject a fully blank saved SQL row.
# NBSP is already tested above; the remaining 28 inputs are separate compatibility cases.
for codepoint in [*range(0x09, 0x0E), *range(0x1C, 0x20), 0x20, 0x85,
                  0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029, 0x202F, 0x205F, 0x3000]:
    statement = "UPDATE public.notes SET title=NULL,body=U&'\\" + f"{codepoint:04X}" + "' WHERE id='{n}'"
    add(f"blank-body-U+{codepoint:04X}", "Unicode whitespace alone cannot be saved as note content",
        reject(statement, "23514", constraint="notes_has_content"))


# Test every affected SQL path, not only the saved-content constraint. Each path
# has a separate case so an early failure cannot hide later policy/trigger bugs.
for codepoint in [*range(0x09, 0x0E), *range(0x1C, 0x20), 0x20, 0x85, 0xA0,
                  0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029, 0x202F, 0x205F, 0x3000]:
    space = "U&'\\" + f"{codepoint:04X}" + "'"
    prefix = f"parity-U+{codepoint:04X}-"
    add(prefix + "title", "All blank titles normalize to NULL",
        f"UPDATE public.notes SET title={space} WHERE id='{{n}}';" +
        check("(SELECT title IS NULL AND body='original body' FROM public.notes WHERE id='{n}')"))
    add(prefix + "countdown", "All blank saved bodies start the 24-hour countdown",
        f"UPDATE public.notes SET body={space} WHERE id='{{n}}';" +
        check(f"(SELECT body={space} AND blank_body_expires_at=updated_at+interval '24 hours' FROM public.notes WHERE id='{{n}}')"))
    for edge in ["leading", "trailing", "blank"]:
        email = {"leading": f"{space} || 'a@example.test'",
                 "trailing": f"'a@example.test' || {space}", "blank": space}[edge]
        add(prefix + "email-" + edge, "SQL rejects every blank/padded stored email",
            reject(f"UPDATE public.users SET email={email} WHERE id='{{a}}'", "23514", constraint="users_email_clean"))
    add(prefix + "draft-delete", "Owner can delete every whitespace-only draft",
        note_insert(",is_draft", ",true").replace("'New title'", "NULL").replace("'new body'", space) + ";" +
        APP + "DELETE FROM public.notes WHERE id='{extra}';RESET ROLE;" +
        check("NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{extra}') AND EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')"))
    # First establish a valid deadline normally. Fixture-only trigger bypass then
    # seeds historical whitespace; content/deadline CHECKs remain enabled.
    add(prefix + "maintenance", "Limited worker sees and expires every due blank body",
        "UPDATE public.notes SET body='' WHERE id='{n}';" +
        seed_history(f"body={space},blank_body_expires_at=now()-interval '1 day'") +
        "SET LOCAL ROLE merlin_d6_maintenance;" +
        check("EXISTS(SELECT 1 FROM public.notes WHERE id='{n}') AND NOT EXISTS(SELECT 1 FROM public.notes WHERE id='{other}')") +
        check("public.cleanup_expired_blank_notes(100)=1") + "RESET ROLE;" +
        check("(SELECT deleted_at IS NOT NULL FROM public.notes WHERE id='{n}') AND (SELECT deleted_at IS NULL FROM public.notes WHERE id='{other}')"))

for codepoint in [0x200B, 0xFEFF, 0x2060]:
    text = "U&'\\" + f"{codepoint:04X}" + "'"
    add(f"parity-nonwhitespace-U+{codepoint:04X}", "Invisible nonwhitespace remains real SQL content",
        f"UPDATE public.notes SET title={text},body={text} WHERE id='{{n}}';" +
        check(f"(SELECT title={text} AND body={text} AND blank_body_expires_at IS NULL FROM public.notes WHERE id='{{n}}')"))


@pytest.fixture(scope="module", autouse=True)
def verify_disposable_database():
    if os.environ.get("MERLIN_RUN_DB_TESTS") != "1":
        yield
        return
    global COMMAND
    if os.environ.get("MERLIN_FAST_DB_TESTS") == "1":
        from tools.database_test_session import container_command
        COMMAND = container_command(COMMAND[7:])
    result = subprocess.run(COMMAND, input="SELECT current_database(),system_identifier FROM pg_control_system();\n",
                            capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, "Disposable database identification failed; no test writes attempted"
    assert result.stdout.strip() == "merlin_d6|" + CLUSTER, "Refusing an unexpected database or cluster"
    counts = subprocess.run(COMMAND, input="SELECT (SELECT count(*) FROM public.users),(SELECT count(*) FROM public.notes);\n",
                            capture_output=True, text=True, timeout=20)
    assert counts.returncode == 0 and counts.stdout.strip() == "0|0", "Database must be empty before this synthetic-only suite"
    global SESSION
    if os.environ.get("MERLIN_FAST_DB_TESTS") == "1":
        from tools.database_test_session import DatabaseTestSession
        with DatabaseTestSession() as session:
            SESSION = session
            try:
                yield
            finally:
                SESSION = None
    else:
        yield
    final = subprocess.run(COMMAND, input="SELECT current_database(),system_identifier FROM pg_control_system();\n"
                           "SELECT (SELECT count(*) FROM public.users),(SELECT count(*) FROM public.notes);\n",
                           capture_output=True, text=True, timeout=20)
    assert final.returncode == 0 and final.stdout.splitlines() == ["merlin_d6|" + CLUSTER, "0|0"], \
        "Final identity/empty-table verification failed; preserve storage and investigate"


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.id)
def test_database_rule(case):
    values = {key: str(uuid.uuid4()) for key in ["a", "b", "n", "other", "extra", "missing"]}
    values.update(name_a="audit_a_" + uuid.uuid4().hex[:8], name_b="audit_b_" + uuid.uuid4().hex[:8])
    setup = """
BEGIN;
SET LOCAL lock_timeout='2s';
SET LOCAL statement_timeout='10s';
-- Assert identity inside this transaction before the first write, too.
DO $gate$ BEGIN
    IF current_database() <> 'merlin_d6' OR
       (SELECT system_identifier::text FROM pg_control_system()) <> '7694311451826794534'
    THEN RAISE EXCEPTION 'Refusing unexpected test target'; END IF;
END $gate$;
INSERT INTO public.users(id,username) VALUES ('{a}','{name_a}'),('{b}','{name_b}');
INSERT INTO public.notes(id,user_id,title,body,device_created_at,device_edited_at) VALUES
('{n}','{a}','Original','original body','2026-01-01 UTC','2026-01-01 UTC'),
('{other}','{b}','Other','other body','2026-01-01 UTC','2026-01-01 UTC');
"""
    # Output from a case may include counts; the final unique marker must be last.
    script = setup.format(**values) + case.sql.format(**values) + f"\nSELECT 'PASS:{case.id}';\nROLLBACK;\n"
    runner = SESSION.run if SESSION is not None else subprocess.run
    result = runner(COMMAND, input=script, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, f"{case.id}: {case.rule}\n{result.stderr}"
    assert result.stdout.splitlines()[-1:] == ["PASS:" + case.id], "Case did not reach its checked outcome"


def test_failed_second_write_rolls_back_first_write_after_reconnect():
    # This assertion specifically requires connection loss and a real reconnect.
    if SESSION is not None:
        SESSION.close()
        globals()["SESSION"] = None
    user_id, note_id, missing_id = [str(uuid.uuid4()) for _ in range(3)]
    username = "audit_abort_" + uuid.uuid4().hex[:8]
    # The second write is otherwise valid; its sole defect is a nonexistent owner.
    script = f"""\\set VERBOSITY verbose
BEGIN;
SET LOCAL lock_timeout='2s'; SET LOCAL statement_timeout='10s';
DO $gate$ BEGIN
IF current_database()<>'merlin_d6' OR
   (SELECT system_identifier::text FROM pg_control_system())<>'7694311451826794534'
THEN RAISE EXCEPTION 'Refusing unexpected test target'; END IF;
END $gate$;
INSERT INTO public.users(id,username) VALUES ('{user_id}','{username}');
INSERT INTO public.notes(id,user_id,title,body,device_created_at,device_edited_at)
VALUES ('{note_id}','{missing_id}','Valid','valid body',now(),now());
SELECT 'Unexpected success';
ROLLBACK;
"""
    failed = subprocess.run(COMMAND, input=script, capture_output=True, text=True, timeout=30)
    assert failed.returncode == 3
    assert "23503" in failed.stderr and "notes_user_id_fkey" in failed.stderr
    assert "Unexpected success" not in failed.stdout
    # ON_ERROR_STOP closes the failed session; PostgreSQL rolls its transaction back.
    query = ("SELECT current_database(),system_identifier FROM pg_control_system();\n" +
             f"SELECT (SELECT count(*) FROM public.users WHERE id='{user_id}')," +
             f"(SELECT count(*) FROM public.notes WHERE id='{note_id}');\n")
    reconnected = subprocess.run(COMMAND, input=query, capture_output=True, text=True, timeout=20)
    assert reconnected.returncode == 0
    assert reconnected.stdout.splitlines() == ["merlin_d6|" + CLUSTER, "0|0"]
