-- Refuse rollback after credentials or device sessions exist. These rows are
-- account data; dropping them would silently destroy sign-in state.
BEGIN;
SET LOCAL lock_timeout = '2s';
SET LOCAL statement_timeout = '10s';
DO $gate$
BEGIN
    IF current_database() <> 'merlin_d6' OR
       (SELECT system_identifier::text FROM pg_control_system()) <> '7694311451826794534'
    THEN RAISE EXCEPTION 'Refusing unexpected migration target'; END IF;
    IF EXISTS (SELECT 1 FROM public.auth_credentials)
       OR EXISTS (SELECT 1 FROM public.auth_refresh_families)
       OR EXISTS (SELECT 1 FROM public.auth_refresh_tokens)
    THEN RAISE EXCEPTION 'Cannot remove authentication data'; END IF;
END;
$gate$;

DROP FUNCTION public.lookup_auth_credential(TEXT);
DROP TRIGGER auth_refresh_token_bounds ON public.auth_refresh_tokens;
DROP TRIGGER auth_refresh_family_expiry ON public.auth_refresh_families;
DROP FUNCTION public.validate_auth_refresh_token();
DROP FUNCTION public.validate_auth_refresh_family();
DROP POLICY auth_lookup_users ON public.users;
DROP POLICY auth_lookup_credentials ON public.auth_credentials;
DROP POLICY auth_credentials_owner ON public.auth_credentials;
DROP POLICY auth_refresh_families_owner ON public.auth_refresh_families;
DROP POLICY auth_refresh_tokens_owner ON public.auth_refresh_tokens;
-- Column grants outlive the auth tables, so remove them before dropping role.
REVOKE SELECT (id, username_canonical) ON public.users FROM merlin_d6_auth_lookup;
REVOKE ALL ON SCHEMA public FROM merlin_api;
DROP TABLE public.auth_refresh_tokens;
DROP TABLE public.auth_refresh_families;
DROP TABLE public.auth_credentials;
DROP ROLE merlin_d6_auth_lookup;
DROP ROLE merlin_api;
COMMIT;
