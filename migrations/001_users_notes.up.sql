-- PostgreSQL 17: username accounts and user-owned notes.
-- Run once in a transaction, only against the isolated Day 6 database.
-- PostgreSQL 17 generates UUIDv4 IDs natively with gen_random_uuid().
-- Unapplied draft: restore email/title/body alongside username accounts.
-- Backend validator and foreground scheduler are implemented separately; not deployed.

-- RULES TO REVIEW
-- Deleted notes stay in trash for 14 days. Restore must happen before that ends.
-- The database chooses deletion time; phones cannot choose it.
-- Only text edits change Last Edited. Hiding/restoring does not.
-- The database chooses the blank-body deadline; input cannot override it.
-- Python checks title 175/body 7000; an emoji counts as 4.
-- Exact database text checks need PL/Python and the pinned packages before migration.
-- Limited permission groups are defined below.
-- Tests against PostgreSQL are still pending. Do not use preserved Sprint 0 storage.

-- STOP HERE unless the disposable server has PL/Python and the pinned packages.
-- This file does not install an extension, change Docker or add database passwords.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'plpython3u') THEN
        RAISE EXCEPTION 'Prerequisite missing: plpython3u on the disposable server';
    END IF;
END;
$$;

-- Match the Python helper exactly, including displayed emoji sequences.
CREATE FUNCTION public.note_weighted_length(value TEXT) RETURNS INTEGER
LANGUAGE plpython3u IMMUTABLE STRICT
AS $python$
from importlib.metadata import version
import emoji
import regex
if version('emoji') != '2.16.0' or version('regex') != '2026.9.29':
    plpy.error('Database Unicode packages must match the pinned application versions')
return sum(4 if emoji.is_emoji(part) else 1 for part in regex.findall(r"\X", value))
$python$;

-- Fail now if the database Python cannot load the required packages.
SELECT public.note_weighted_length('check');

-- These are permission groups, not login accounts. Create them only in isolation.
-- Existing names cause this migration to stop; do not silently change existing roles.
CREATE ROLE merlin_d6_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
CREATE ROLE merlin_d6_app NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
CREATE ROLE merlin_d6_maintenance NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;

-- Table definitions describe stored data; CHECK/UNIQUE enforce database rules.
-- NOT NULL means required. DEFAULT supplies a value when an insert omits it.
CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- Random UUIDv4.
    username TEXT COLLATE "C" NOT NULL,
    -- GENERATED keeps this lookup name in sync; callers must not supply it.
    username_canonical TEXT COLLATE "C"
        GENERATED ALWAYS AS (lower(username)) STORED NOT NULL,
    email TEXT, -- Optional; preserve display casing.
    created_at TIMESTAMPTZ NOT NULL DEFAULT statement_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT statement_timestamp(),

    -- Check UUID version 4 and the RFC variant; this does not generate an ID.
    CONSTRAINT users_id_uuidv4 CHECK (
        substring(id::TEXT FROM 15 FOR 1) = '4'
        AND substring(id::TEXT FROM 20 FOR 1) IN ('8', '9', 'a', 'b')
    ),

    -- Accept 1-20 lowercase ASCII letters, digits or underscores.
    CONSTRAINT users_username_format CHECK (username ~ '^[a-z0-9_]{1,20}$'),
    CONSTRAINT users_username_unique UNIQUE (username),
    -- Backend trims input and maps blank email to NULL before writing.
    CONSTRAINT users_email_clean CHECK (
        email IS NULL OR (email ~ '[^[:space:]]' AND email !~ '^[[:space:]]|[[:space:]]$')
    )
);

-- Supports direct canonical-name lookups; generated values cannot drift.
-- With lowercase-only names this repeats the username index's logical key.
CREATE INDEX users_username_canonical_idx ON public.users (username_canonical);

-- Case-insensitive uniqueness; several accounts may have NULL email.
CREATE UNIQUE INDEX users_email_unique ON public.users (lower(email));

CREATE TABLE public.notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- Independent random UUIDv4.
    -- The owner must exist; deleting that account permanently deletes its notes.
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    title TEXT, -- Optional, non-unique; blank titles become NULL.
    body TEXT NOT NULL DEFAULT '', -- Preserve whitespace in actual writing.
    created_at TIMESTAMPTZ NOT NULL DEFAULT statement_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT statement_timestamp(),
    device_created_at TIMESTAMPTZ NOT NULL, -- Client supplies its original instant.
    device_edited_at TIMESTAMPTZ NOT NULL, -- Client edit time; may move backward.
    blank_body_expires_at TIMESTAMPTZ, -- Server deadline, managed by trigger.
    deleted_at TIMESTAMPTZ DEFAULT NULL, -- Trigger chooses when trash retention starts.
    is_draft BOOLEAN NOT NULL DEFAULT FALSE, -- Drafts may be fully blank.

    CONSTRAINT notes_id_uuidv4 CHECK (
        substring(id::TEXT FROM 15 FOR 1) = '4'
        AND substring(id::TEXT FROM 20 FOR 1) IN ('8', '9', 'a', 'b')
    ),
    CONSTRAINT notes_title_nonblank CHECK (title IS NULL OR title ~ '[^[:space:]]'),
    -- A rejected write does not delete an existing note: backend handles blank saves.
    CONSTRAINT notes_has_content CHECK (
        is_draft OR COALESCE(title ~ '[^[:space:]]', false) OR body ~ '[^[:space:]]'
    ),
    -- Drafts/contentful notes have no countdown; saved blank bodies require one.
    CONSTRAINT notes_deadline_matches_body CHECK (
        ((is_draft OR body ~ '[^[:space:]]') AND blank_body_expires_at IS NULL)
        OR (NOT is_draft AND body !~ '[^[:space:]]' AND blank_body_expires_at IS NOT NULL)
    ),
    CONSTRAINT notes_title_limit CHECK (public.note_weighted_length(COALESCE(title, '')) <= 175),
    CONSTRAINT notes_body_limit CHECK (public.note_weighted_length(body) <= 7000)
    -- app/note_rules.py validates title <= 175, body <= 7000; each emoji weighs 4.
    -- Database checks use the same pinned Unicode rule for direct SQL writes.
    -- char_length() and UTF-8 byte counts do not implement that product rule.
);

-- Fast newest-first timeline within one account.
CREATE INDEX notes_user_created_idx ON public.notes (user_id, created_at DESC);

-- Original rewrite timeline, plus the earlier latest-edit timeline with tie-breaker.
CREATE INDEX notes_user_updated_idx
    ON public.notes (user_id, updated_at DESC, id);
CREATE INDEX notes_user_device_updated_idx
    ON public.notes (user_id, device_edited_at DESC, id);
CREATE INDEX notes_blank_body_expiry_idx
    ON public.notes (blank_body_expires_at) WHERE blank_body_expires_at IS NOT NULL;

-- Backend lists must filter deleted_at IS NULL and select draft/saved state.
CREATE INDEX notes_user_draft_updated_idx
    ON public.notes (user_id, is_draft, updated_at DESC, id)
    WHERE deleted_at IS NULL;
-- Supports bounded worker purges of soft-deleted rows older than 14 days.
CREATE INDEX notes_deleted_at_idx ON public.notes (deleted_at)
    WHERE deleted_at IS NOT NULL;
-- DELETE still takes row/table locks; purge in bounded batches in the future worker.
-- Username indexes aid lookup; they do not implement rate limits or DDoS protection.

-- Server times support reliable ordering; client times support device display.
-- NEW is the proposed row; OLD is the previous row, available only on UPDATE.
-- A BEFORE trigger can adjust NEW before PostgreSQL stores or checks the row.
CREATE FUNCTION public.manage_users_notes_timestamps() RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = pg_catalog, public
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.created_at := statement_timestamp();
        NEW.updated_at := NEW.created_at;
    ELSE
        IF NEW.id IS DISTINCT FROM OLD.id
           OR NEW.created_at IS DISTINCT FROM OLD.created_at THEN
            RAISE EXCEPTION 'ID and creation time cannot be changed'
                USING ERRCODE = '23514';
        END IF;

        IF TG_TABLE_NAME = 'notes' THEN
            IF NEW.device_created_at IS DISTINCT FROM OLD.device_created_at THEN
                RAISE EXCEPTION 'Device creation time cannot be changed'
                    USING ERRCODE = '23514';
            END IF;
            IF NEW.user_id IS DISTINCT FROM OLD.user_id THEN
                RAISE EXCEPTION 'Note ownership cannot be transferred'
                    USING ERRCODE = '23514';
            END IF;
        END IF;

        -- Notes advance only for content edits; reads and no-op saves keep edit time.
        IF TG_TABLE_NAME = 'notes' THEN
            IF NEW.title IS DISTINCT FROM OLD.title OR NEW.body IS DISTINCT FROM OLD.body THEN
                NEW.updated_at := statement_timestamp();
                -- Backend must explicitly supply device_edited_at on every content edit.
            ELSE
                NEW.updated_at := OLD.updated_at;
                NEW.device_edited_at := OLD.device_edited_at;
            END IF;
        ELSE
            NEW.updated_at := statement_timestamp();
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

-- Normalize blank titles and manage the server-controlled 24-hour countdown.
CREATE FUNCTION public.manage_note_content() RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = pg_catalog, public
AS $$
BEGIN
    IF NEW.title !~ '[^[:space:]]' THEN
        NEW.title := NULL;
    END IF;

    IF TG_OP = 'INSERT' THEN
        NEW.device_edited_at := NEW.device_created_at;
        IF NEW.is_draft OR NEW.body ~ '[^[:space:]]' THEN
            NEW.blank_body_expires_at := NULL;
        ELSE
            NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '24 hours';
        END IF;
    ELSE
        IF NOT OLD.is_draft AND NEW.is_draft THEN
            RAISE EXCEPTION 'Saved notes cannot become drafts' USING ERRCODE = '23514';
        END IF;
        IF NEW.is_draft OR NEW.body ~ '[^[:space:]]' THEN
            NEW.blank_body_expires_at := NULL;
        -- Publishing a draft or removing real body content starts a new countdown.
        ELSIF OLD.deleted_at IS NOT NULL AND NEW.deleted_at IS NULL THEN
            -- A restored title-only note gets a new day before expiry.
            NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '24 hours';
        ELSIF OLD.is_draft OR OLD.body ~ '[^[:space:]]' THEN
            NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '24 hours';
        ELSE
            -- Saving an already blank body must not extend its existing deadline.
            NEW.blank_body_expires_at := OLD.blank_body_expires_at;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

-- Choose deletion time here, not on the phone. Repeated hiding keeps the old time.
CREATE FUNCTION public.manage_note_deletion() RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = pg_catalog, public
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.deleted_at IS NOT NULL THEN
            RAISE EXCEPTION 'New notes cannot start in trash' USING ERRCODE = '23514';
        END IF;
    ELSIF OLD.deleted_at IS NULL THEN
        IF NEW.deleted_at IS NOT NULL THEN
            NEW.deleted_at := clock_timestamp();
        END IF;
    ELSIF NEW.deleted_at IS NULL THEN
        -- Restoring after the deadline is forbidden, even before the worker runs.
        IF clock_timestamp() >= OLD.deleted_at + INTERVAL '14 days' THEN
            RAISE EXCEPTION 'The restore period has ended' USING ERRCODE = '23514';
        END IF;
    ELSE
        -- Restore a trashed note before editing its text or draft state.
        IF NEW.title IS DISTINCT FROM OLD.title OR NEW.body IS DISTINCT FROM OLD.body
           OR NEW.is_draft IS DISTINCT FROM OLD.is_draft THEN
            RAISE EXCEPTION 'Restore the note before editing it' USING ERRCODE = '23514';
        END IF;
        NEW.deleted_at := OLD.deleted_at;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER notes_deletion
    BEFORE INSERT OR UPDATE ON public.notes
    FOR EACH ROW EXECUTE FUNCTION public.manage_note_deletion();

-- Same-event triggers run alphabetically: normalization precedes timestamp checks.
CREATE TRIGGER notes_content
    BEFORE INSERT OR UPDATE ON public.notes
    FOR EACH ROW EXECUTE FUNCTION public.manage_note_content();

CREATE TRIGGER users_timestamps
    BEFORE INSERT OR UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION public.manage_users_notes_timestamps();

CREATE TRIGGER notes_timestamps
    BEFORE INSERT OR UPDATE ON public.notes
    FOR EACH ROW EXECUTE FUNCTION public.manage_users_notes_timestamps();

-- Owner-only foundation: the trusted backend sets merlin.actor_id per transaction.
-- Never give app users SQL access: this setting is not proof of authentication.
-- Use the limited role grants below; superusers still bypass these policies.
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users FORCE ROW LEVEL SECURITY;
ALTER TABLE public.notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notes FORCE ROW LEVEL SECURITY;

-- USING limits existing rows; WITH CHECK limits newly inserted/updated rows.
CREATE POLICY users_own_account ON public.users
    FOR ALL TO merlin_d6_app
    USING (id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID)
    WITH CHECK (id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID);

CREATE POLICY notes_own_account ON public.notes
    FOR ALL TO merlin_d6_app
    USING (user_id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID)
    WITH CHECK (user_id = NULLIF(current_setting('merlin.actor_id', true), '')::UUID);

-- Move expired title-only notes to trash in small batches. Busy rows wait for another cycle.
CREATE FUNCTION public.cleanup_expired_blank_notes(batch_size INTEGER DEFAULT 100) RETURNS BIGINT
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, public
AS $$
DECLARE
    deleted_count BIGINT;
BEGIN
    IF batch_size IS NULL OR batch_size NOT BETWEEN 1 AND 1000 THEN
        RAISE EXCEPTION 'Batch size must be between 1 and 1000';
    END IF;
    -- due selects a small batch; SKIP LOCKED avoids waiting on busy rows.
    WITH due AS (
        SELECT id FROM public.notes
        WHERE blank_body_expires_at <= statement_timestamp()
          AND body !~ '[^[:space:]]' AND NOT is_draft AND deleted_at IS NULL
        ORDER BY blank_body_expires_at, id
        LIMIT batch_size FOR UPDATE SKIP LOCKED
    )
    UPDATE public.notes AS n SET deleted_at = clock_timestamp() FROM due
    WHERE n.id = due.id
      AND n.blank_body_expires_at <= statement_timestamp()
      AND n.body !~ '[^[:space:]]' AND NOT n.is_draft AND n.deleted_at IS NULL;
    -- Return how many rows this cycle changed.
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$;
-- Callers need explicit execution permission; the function grants no extra rights.
REVOKE ALL ON FUNCTION public.cleanup_expired_blank_notes(INTEGER) FROM PUBLIC;

-- Purge soft-deleted notes after 14 days; active notes cannot match this predicate.
CREATE FUNCTION public.purge_deleted_notes(batch_size INTEGER DEFAULT 100) RETURNS BIGINT
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog, public
AS $$
DECLARE
    deleted_count BIGINT;
BEGIN
    IF batch_size IS NULL OR batch_size NOT BETWEEN 1 AND 1000 THEN
        RAISE EXCEPTION 'Batch size must be between 1 and 1000';
    END IF;
    -- due selects a small batch; SKIP LOCKED avoids waiting on busy rows.
    WITH due AS (
        SELECT id FROM public.notes
        WHERE deleted_at <= statement_timestamp() - INTERVAL '14 days'
        ORDER BY deleted_at, id
        LIMIT batch_size FOR UPDATE SKIP LOCKED
    )
    DELETE FROM public.notes AS n USING due
    WHERE n.id = due.id AND n.deleted_at <= statement_timestamp() - INTERVAL '14 days';
    -- Return the actual number deleted, not the number merely selected.
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$;
-- Callers need explicit execution permission; the function grants no extra rights.
REVOKE ALL ON FUNCTION public.purge_deleted_notes(INTEGER) FROM PUBLIC;

-- Foreground scheduler: app/notes_maintenance.py; not installed as a service or started.
-- Ordinary app users must not receive direct SQL access or privilege bypass.
-- Title-only expiry now enters trash; the purge removes it after 14 more days.
-- Normal lists must use active_notes; the notes table also holds owner-visible trash.
-- Review the revised design and test this migration before production use.

-- Direct DELETE also has limits, even when a caller skips the cleanup functions.
CREATE POLICY notes_maintenance_delete_limit ON public.notes
    AS RESTRICTIVE FOR DELETE TO merlin_d6_maintenance
    USING (deleted_at <= statement_timestamp() - INTERVAL '14 days');
CREATE POLICY notes_app_delete_limit ON public.notes
    AS RESTRICTIVE FOR DELETE TO merlin_d6_app
    USING (is_draft AND COALESCE(title !~ '[^[:space:]]', true) AND body !~ '[^[:space:]]');

-- The worker can see only due expiry rows or trashed notes, never every active note.
CREATE POLICY notes_maintenance ON public.notes
    FOR ALL TO merlin_d6_maintenance
    USING (
        deleted_at IS NOT NULL OR
        (NOT is_draft AND body !~ '[^[:space:]]' AND blank_body_expires_at <= statement_timestamp())
    )
    WITH CHECK (deleted_at IS NOT NULL);

-- Normal lists read this view. Trash is a separate, owner-checked operation.
CREATE VIEW public.active_notes WITH (security_invoker = true) AS
    SELECT * FROM public.notes WHERE deleted_at IS NULL;

-- Keep object ownership away from application and maintenance logins.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA public TO merlin_d6_owner;
GRANT USAGE ON SCHEMA public TO merlin_d6_app, merlin_d6_maintenance;
ALTER TABLE public.users OWNER TO merlin_d6_owner;
ALTER TABLE public.notes OWNER TO merlin_d6_owner;
ALTER VIEW public.active_notes OWNER TO merlin_d6_owner;
ALTER FUNCTION public.note_weighted_length(TEXT) OWNER TO merlin_d6_owner;
ALTER FUNCTION public.manage_users_notes_timestamps() OWNER TO merlin_d6_owner;
ALTER FUNCTION public.manage_note_content() OWNER TO merlin_d6_owner;
ALTER FUNCTION public.manage_note_deletion() OWNER TO merlin_d6_owner;
ALTER FUNCTION public.cleanup_expired_blank_notes(INTEGER) OWNER TO merlin_d6_owner;
ALTER FUNCTION public.purge_deleted_notes(INTEGER) OWNER TO merlin_d6_owner;

REVOKE ALL ON public.users, public.notes, public.active_notes FROM PUBLIC;
REVOKE ALL ON FUNCTION public.note_weighted_length(TEXT),
    public.manage_users_notes_timestamps(), public.manage_note_content(),
    public.manage_note_deletion(), public.cleanup_expired_blank_notes(INTEGER),
    public.purge_deleted_notes(INTEGER) FROM PUBLIC;

-- Column grants stop direct changes to IDs, owners and database-managed clocks.
GRANT SELECT ON public.users, public.notes, public.active_notes TO merlin_d6_app;
GRANT INSERT (id, username, email) ON public.users TO merlin_d6_app;
GRANT UPDATE (username, email) ON public.users TO merlin_d6_app;
GRANT DELETE ON public.users, public.notes TO merlin_d6_app;
-- RLS limits note DELETE to blank drafts; saved notes must enter trash instead.
GRANT INSERT (id, user_id, title, body, device_created_at, device_edited_at, is_draft)
    ON public.notes TO merlin_d6_app;
GRANT UPDATE (title, body, device_edited_at, is_draft, deleted_at)
    ON public.notes TO merlin_d6_app;
GRANT EXECUTE ON FUNCTION public.note_weighted_length(TEXT) TO merlin_d6_app, merlin_d6_maintenance;
GRANT SELECT, DELETE ON public.notes TO merlin_d6_maintenance;
GRANT UPDATE (deleted_at) ON public.notes TO merlin_d6_maintenance;
GRANT EXECUTE ON FUNCTION public.cleanup_expired_blank_notes(INTEGER),
    public.purge_deleted_notes(INTEGER) TO merlin_d6_maintenance;

-- Role grants are defined here; no login credentials or running service are created.
