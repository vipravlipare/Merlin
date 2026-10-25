"""Check security properties that can be reviewed without touching a database."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
UP = (ROOT / "migrations/003_auth_foundation.up.sql").read_text()
DOWN = (ROOT / "migrations/003_auth_foundation.down.sql").read_text()
from tools.audit_database_cases import FINGERPRINT


def test_auth_migration_stores_only_argon2id_and_refresh_digests():
    assert re.search(r"password_hash\s+TEXT\s+NOT NULL", UP)
    assert "password_hash LIKE '$argon2id$%'" in UP
    assert re.search(r"token_hash\s+BYTEA\s+PRIMARY KEY", UP)
    assert "octet_length(token_hash) = 32" in UP
    assert not re.search(r"refresh_token\s+TEXT|token_value\s+TEXT|raw_token\s+TEXT", UP, re.I)


def test_auth_tables_force_rls_and_app_cannot_read_password_hash_table():
    for table in ("auth_credentials", "auth_refresh_families", "auth_refresh_tokens"):
        assert f"ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY" in UP
        assert f"ALTER TABLE public.{table} FORCE ROW LEVEL SECURITY" in UP
    assert "REVOKE ALL ON public.auth_credentials, public.auth_refresh_families," in UP
    assert "GRANT EXECUTE ON FUNCTION public.lookup_auth_credential(TEXT) TO merlin_api" in UP
    assert "GRANT SELECT ON public.auth_credentials TO merlin_d6_app" not in UP


def test_runtime_login_is_narrow_and_cannot_inherit_notes_role():
    assert re.search(
        r"CREATE ROLE merlin_api LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE\s+"
        r"NOREPLICATION NOBYPASSRLS;",
        UP,
    )
    assert "GRANT merlin_d6_app TO merlin_api;" not in UP
    assert "pg_has_role(current_user, 'merlin_d6_app', 'MEMBER')" in (ROOT / "app/runtime.py").read_text()
    assert "NOT pg_has_role(current_user, 'merlin_d6_app', 'MEMBER')" in (ROOT / "app/runtime.py").read_text()
    assert "DROP ROLE merlin_api;" in DOWN
    assert not re.search(r"CREATE ROLE merlin_api[^;]*\bPASSWORD\b", UP, re.I)


def test_runtime_auth_role_is_only_granted_refresh_table_permissions():
    for table in ("auth_refresh_families", "auth_refresh_tokens"):
        assert f"TO merlin_api" in UP
    assert "GRANT SELECT ON public.auth_refresh_families, public.auth_refresh_tokens TO merlin_api" in UP
    assert "GRANT SELECT ON public.notes TO merlin_api" not in UP
    assert "GRANT SELECT ON public.users TO merlin_api" not in UP
    assert "TO merlin_d6_app" not in UP[UP.index("GRANT SELECT ON public.auth_refresh_families"):]


def test_login_lookup_is_narrow_and_definer_search_path_is_fixed():
    assert "SECURITY DEFINER" in UP
    assert "SET search_path = pg_catalog, public" in UP
    assert "WHERE u.username_canonical = lower(p_username)" in UP
    assert "LIMIT 1" in UP
    assert "REVOKE ALL ON FUNCTION public.lookup_auth_credential(TEXT) FROM PUBLIC" in UP
    assert "GRANT EXECUTE ON FUNCTION public.lookup_auth_credential(TEXT) TO merlin_api" in UP


def test_refresh_windows_have_fixed_idle_and_absolute_caps():
    assert "NEW.idle_expires_at > statement_timestamp() + INTERVAL '30 days'" in UP
    assert "NEW.absolute_expires_at > NEW.created_at + INTERVAL '90 days'" in UP
    assert "NEW.expires_at > family.idle_expires_at" in UP
    assert "NEW.expires_at > family.absolute_expires_at" in UP
    assert "family.revoked_at IS NOT NULL" in UP
    assert "OLD.consumed_at IS NOT NULL OR NEW.consumed_at IS NULL" in UP
    assert "auth_refresh_tokens_single_predecessor_idx" in UP


def test_rollback_refuses_to_delete_authentication_data():
    assert "IF EXISTS (SELECT 1 FROM public.auth_credentials)" in DOWN
    assert "OR EXISTS (SELECT 1 FROM public.auth_refresh_families)" in DOWN
    assert "OR EXISTS (SELECT 1 FROM public.auth_refresh_tokens)" in DOWN
    assert "Cannot remove authentication data" in DOWN
    assert "CASCADE" not in DOWN


def test_database_fingerprint_supports_pre_and_post_auth_migration_states():
    for table in ("auth_credentials", "auth_refresh_families", "auth_refresh_tokens"):
        assert f"'{table}'::regclass" not in FINGERPRINT
        assert f"to_regclass('public.{table}')" in FINGERPRINT
    assert "'merlin_api'::regrole" not in FINGERPRINT
    assert "to_regrole('merlin_api')" in FINGERPRINT
