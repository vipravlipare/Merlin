-- Password credentials and rotating refresh-token storage for MER-12.
-- Apply only after migrations 001 and 002, on a fresh isolated test database.
BEGIN;
SET LOCAL lock_timeout = '2s';
SET LOCAL statement_timeout = '10s';
DO $gate$
BEGIN
    IF current_database() <> 'merlin_d6' OR
       (SELECT system_identifier::text FROM pg_control_system()) <> '7694311451826794534'
    THEN RAISE EXCEPTION 'Refusing unexpected migration target'; END IF;
END;
$gate$;

-- This NOLOGIN role may read credentials only through the exact-name lookup
-- function below. It cannot create objects or bypass row-level security.
CREATE ROLE merlin_d6_auth_lookup NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
    NOREPLICATION NOBYPASSRLS;
-- Operators provision this dedicated login password out of band.
CREATE ROLE merlin_api LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE
    NOREPLICATION NOBYPASSRLS;
GRANT USAGE ON SCHEMA public TO merlin_api;

CREATE TABLE public.auth_credentials (
    user_id UUID PRIMARY KEY REFERENCES public.users(id) ON DELETE CASCADE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT statement_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT statement_timestamp(),
    CONSTRAINT auth_password_hash_argon2id CHECK (
        password_hash LIKE '$argon2id$%' AND octet_length(password_hash) BETWEEN 40 AND 512
    )
);

-- One row per device session family. The absolute expiry cannot be extended;
-- idle expiry can move only within that fixed 90-day boundary.
CREATE TABLE public.auth_refresh_families (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    device_label TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT statement_timestamp(),
    idle_expires_at TIMESTAMPTZ NOT NULL,
    absolute_expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    CONSTRAINT auth_family_device_label_limit CHECK (
        device_label IS NULL OR octet_length(device_label) <= 120
    ),
    CONSTRAINT auth_family_expiry_order CHECK (
        created_at < idle_expires_at AND idle_expires_at <= absolute_expires_at
        AND absolute_expires_at <= created_at + INTERVAL '90 days'
    ),
    CONSTRAINT auth_family_revocation_not_before_creation CHECK (
        revoked_at IS NULL OR revoked_at >= created_at
    )
);
CREATE INDEX auth_refresh_families_user_active_idx
    ON public.auth_refresh_families (user_id, created_at DESC)
    WHERE revoked_at IS NULL;

-- Store only SHA-256 digests of high-entropy opaque refresh secrets. Consumed
-- rows stay available so reuse can revoke the whole device family.
CREATE TABLE public.auth_refresh_tokens (
    token_hash BYTEA PRIMARY KEY,
    family_id UUID NOT NULL REFERENCES public.auth_refresh_families(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT statement_timestamp(),
    expires_at TIMESTAMPTZ NOT NULL,
    consumed_at TIMESTAMPTZ,
    replaced_by_hash BYTEA REFERENCES public.auth_refresh_tokens(token_hash),
    CONSTRAINT auth_refresh_hash_length CHECK (octet_length(token_hash) = 32),
    CONSTRAINT auth_refresh_replacement_hash_length CHECK (
        replaced_by_hash IS NULL OR
        (octet_length(replaced_by_hash) = 32 AND replaced_by_hash <> token_hash)
    ),
    CONSTRAINT auth_refresh_expiry_after_creation CHECK (expires_at > created_at)
);
CREATE INDEX auth_refresh_tokens_family_created_idx
    ON public.auth_refresh_tokens (family_id, created_at DESC);
CREATE UNIQUE INDEX auth_refresh_tokens_single_predecessor_idx
    ON public.auth_refresh_tokens (replaced_by_hash)
    WHERE replaced_by_hash IS NOT NULL;

-- The schema owner is a NOLOGIN role. The application role never owns tables.
ALTER TABLE public.auth_credentials OWNER TO merlin_d6_owner;
ALTER TABLE public.auth_refresh_families OWNER TO merlin_d6_owner;
ALTER TABLE public.auth_refresh_tokens OWNER TO merlin_d6_owner;

-- A refresh can extend idle expiry to 30 days from now, but never past the
-- family's original 90-day maximum. Tokens cannot outlive their family.
CREATE FUNCTION public.validate_auth_refresh_family() RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = pg_catalog, public
AS $$
BEGIN
    IF NEW.idle_expires_at > statement_timestamp() + INTERVAL '30 days'
       OR NEW.idle_expires_at > NEW.absolute_expires_at
       OR NEW.absolute_expires_at > NEW.created_at + INTERVAL '90 days'
    THEN RAISE EXCEPTION 'Invalid authentication session expiry' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER auth_refresh_family_expiry
    BEFORE INSERT OR UPDATE OF idle_expires_at, absolute_expires_at
    ON public.auth_refresh_families
    FOR EACH ROW EXECUTE FUNCTION public.validate_auth_refresh_family();

CREATE FUNCTION public.validate_auth_refresh_token() RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = pg_catalog, public
AS $$
DECLARE family public.auth_refresh_families%ROWTYPE;
BEGIN
    SELECT * INTO family FROM public.auth_refresh_families WHERE id = NEW.family_id FOR UPDATE;
    IF NOT FOUND OR family.revoked_at IS NOT NULL
       OR family.idle_expires_at <= statement_timestamp()
       OR family.absolute_expires_at <= statement_timestamp()
       OR NEW.expires_at > family.idle_expires_at
       OR NEW.expires_at > family.absolute_expires_at
    THEN RAISE EXCEPTION 'Invalid authentication refresh token' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'UPDATE' THEN
        IF OLD.consumed_at IS NOT NULL OR NEW.consumed_at IS NULL
           OR NEW.consumed_at < OLD.created_at
           OR NEW.consumed_at > statement_timestamp()
        THEN RAISE EXCEPTION 'Invalid refresh-token rotation' USING ERRCODE = '23514';
        END IF;
        IF NEW.replaced_by_hash IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM public.auth_refresh_tokens AS successor
            WHERE successor.token_hash = NEW.replaced_by_hash
              AND successor.family_id = NEW.family_id
              AND successor.created_at > OLD.created_at
        ) THEN RAISE EXCEPTION 'Invalid refresh-token replacement' USING ERRCODE = '23514';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER auth_refresh_token_bounds
    BEFORE INSERT OR UPDATE
    ON public.auth_refresh_tokens
    FOR EACH ROW EXECUTE FUNCTION public.validate_auth_refresh_token();

ALTER TABLE public.auth_credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.auth_credentials FORCE ROW LEVEL SECURITY;
ALTER TABLE public.auth_refresh_families ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.auth_refresh_families FORCE ROW LEVEL SECURITY;
ALTER TABLE public.auth_refresh_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.auth_refresh_tokens FORCE ROW LEVEL SECURITY;

-- The no-login lookup role sees rows only while executing its restricted
-- SECURITY DEFINER lookup. It receives no direct table grants.
CREATE POLICY auth_lookup_users ON public.users
    FOR SELECT TO merlin_d6_auth_lookup USING (true);
CREATE POLICY auth_lookup_credentials ON public.auth_credentials
    FOR SELECT TO merlin_d6_auth_lookup USING (true);

CREATE POLICY auth_credentials_owner ON public.auth_credentials
    FOR ALL TO merlin_d6_app
    USING (user_id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID)
    WITH CHECK (user_id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID);
CREATE POLICY auth_refresh_families_owner ON public.auth_refresh_families
    FOR ALL TO merlin_api
    USING (user_id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID)
    WITH CHECK (user_id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID);
CREATE POLICY auth_refresh_tokens_owner ON public.auth_refresh_tokens
    FOR ALL TO merlin_api
    USING (EXISTS (
        SELECT 1 FROM public.auth_refresh_families f
        WHERE f.id = family_id
          AND f.user_id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID
    ))
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.auth_refresh_families f
        WHERE f.id = family_id
          AND f.user_id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID
    ));

ALTER FUNCTION public.validate_auth_refresh_family() OWNER TO merlin_d6_owner;
ALTER FUNCTION public.validate_auth_refresh_token() OWNER TO merlin_d6_owner;
REVOKE ALL ON FUNCTION public.validate_auth_refresh_family(),
    public.validate_auth_refresh_token() FROM PUBLIC;

-- Login gets exactly one account's stored hash, never a table-wide read.
-- The caller must still enforce rate limits and verify the password in Python.
CREATE FUNCTION public.lookup_auth_credential(p_username TEXT)
RETURNS TABLE(user_id UUID, password_hash TEXT)
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = pg_catalog, public
AS $$
    SELECT u.id, c.password_hash
    FROM public.users AS u
    JOIN public.auth_credentials AS c ON c.user_id = u.id
    WHERE u.username_canonical = lower(p_username)
    LIMIT 1
$$;
ALTER FUNCTION public.lookup_auth_credential(TEXT) OWNER TO merlin_d6_auth_lookup;
GRANT SELECT (id, username_canonical) ON public.users TO merlin_d6_auth_lookup;
GRANT SELECT ON public.auth_credentials TO merlin_d6_auth_lookup;
REVOKE ALL ON public.auth_credentials, public.auth_refresh_families,
    public.auth_refresh_tokens FROM PUBLIC;
REVOKE ALL ON FUNCTION public.lookup_auth_credential(TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.lookup_auth_credential(TEXT) TO merlin_api;

GRANT SELECT ON public.auth_refresh_families, public.auth_refresh_tokens TO merlin_api;
GRANT INSERT (user_id, device_label, idle_expires_at, absolute_expires_at)
    ON public.auth_refresh_families TO merlin_api;
GRANT UPDATE (idle_expires_at, revoked_at) ON public.auth_refresh_families TO merlin_api;
GRANT INSERT (token_hash, family_id, expires_at) ON public.auth_refresh_tokens TO merlin_api;
GRANT UPDATE (consumed_at, replaced_by_hash) ON public.auth_refresh_tokens TO merlin_api;

COMMIT;
