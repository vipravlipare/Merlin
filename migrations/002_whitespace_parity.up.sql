-- Repair Python/PostgreSQL whitespace parity on the disposable Day 6 cluster.
-- Apply with psql ON_ERROR_STOP=1. Never rerun migration 001 or use Sprint 0.
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

-- Use Python's exact strip definition for content and edge padding.
-- Non-STRICT: optional NULL text is handled explicitly rather than returning SQL NULL.
CREATE FUNCTION public.note_text_is_blank(value TEXT) RETURNS BOOLEAN
LANGUAGE plpython3u IMMUTABLE
AS $python$
return value is None or not value.strip()
$python$;
CREATE FUNCTION public.note_email_is_clean(value TEXT) RETURNS BOOLEAN
LANGUAGE plpython3u IMMUTABLE
AS $python$
return value is None or bool(value.strip()) and value == value.strip()
$python$;
ALTER FUNCTION public.note_text_is_blank(TEXT) OWNER TO merlin_d6_owner;
ALTER FUNCTION public.note_email_is_clean(TEXT) OWNER TO merlin_d6_owner;
REVOKE ALL ON FUNCTION public.note_text_is_blank(TEXT), public.note_email_is_clean(TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.note_text_is_blank(TEXT), public.note_email_is_clean(TEXT)
    TO merlin_d6_app, merlin_d6_maintenance;

ALTER TABLE public.users DROP CONSTRAINT users_email_clean;
ALTER TABLE public.users ADD CONSTRAINT users_email_clean CHECK (
    email IS NULL OR (public.note_email_is_clean(email))
);

ALTER TABLE public.notes DROP CONSTRAINT notes_title_nonblank;
ALTER TABLE public.notes ADD CONSTRAINT notes_title_nonblank CHECK (title IS NULL OR NOT public.note_text_is_blank(title));

ALTER TABLE public.notes DROP CONSTRAINT notes_has_content;
ALTER TABLE public.notes ADD CONSTRAINT notes_has_content CHECK (
        is_draft OR COALESCE(NOT public.note_text_is_blank(title), false) OR NOT public.note_text_is_blank(body)
    );

ALTER TABLE public.notes DROP CONSTRAINT notes_deadline_matches_body;
ALTER TABLE public.notes ADD CONSTRAINT notes_deadline_matches_body CHECK (
        ((is_draft OR NOT public.note_text_is_blank(body)) AND blank_body_expires_at IS NULL)
        OR (NOT is_draft AND public.note_text_is_blank(body) AND blank_body_expires_at IS NOT NULL)
    );

CREATE OR REPLACE FUNCTION public.manage_note_content() RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = pg_catalog, public
AS $$
BEGIN
    IF public.note_text_is_blank(NEW.title) THEN
        NEW.title := NULL;
    END IF;

    IF TG_OP = 'INSERT' THEN
        NEW.device_edited_at := NEW.device_created_at;
        IF NEW.is_draft OR NOT public.note_text_is_blank(NEW.body) THEN
            NEW.blank_body_expires_at := NULL;
        ELSE
            NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '24 hours';
        END IF;
    ELSE
        IF NOT OLD.is_draft AND NEW.is_draft THEN
            RAISE EXCEPTION 'Saved notes cannot become drafts' USING ERRCODE = '23514';
        END IF;
        IF NEW.is_draft OR NOT public.note_text_is_blank(NEW.body) THEN
            NEW.blank_body_expires_at := NULL;
        -- Publishing a draft or removing real body content starts a new countdown.
        ELSIF OLD.deleted_at IS NOT NULL AND NEW.deleted_at IS NULL THEN
            -- A restored title-only note gets a new day before expiry.
            NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '24 hours';
        ELSIF OLD.is_draft OR NOT public.note_text_is_blank(OLD.body) THEN
            NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '24 hours';
        ELSE
            -- Saving an already blank body must not extend its existing deadline.
            NEW.blank_body_expires_at := OLD.blank_body_expires_at;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION public.cleanup_expired_blank_notes(batch_size INTEGER DEFAULT 100) RETURNS BIGINT
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
          AND public.note_text_is_blank(body) AND NOT is_draft AND deleted_at IS NULL
        ORDER BY blank_body_expires_at, id
        LIMIT batch_size FOR UPDATE SKIP LOCKED
    )
    UPDATE public.notes AS n SET deleted_at = clock_timestamp() FROM due
    WHERE n.id = due.id
      AND n.blank_body_expires_at <= statement_timestamp()
      AND public.note_text_is_blank(n.body) AND NOT n.is_draft AND n.deleted_at IS NULL;
    -- Return how many rows this cycle changed.
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$;

DROP POLICY notes_app_delete_limit ON public.notes;
CREATE POLICY notes_app_delete_limit ON public.notes
    AS RESTRICTIVE FOR DELETE TO merlin_d6_app
    USING (is_draft AND COALESCE(public.note_text_is_blank(title), true) AND public.note_text_is_blank(body));

DROP POLICY notes_maintenance ON public.notes;
CREATE POLICY notes_maintenance ON public.notes
    FOR ALL TO merlin_d6_maintenance
    USING (
        deleted_at IS NOT NULL OR
        (NOT is_draft AND public.note_text_is_blank(body) AND blank_body_expires_at <= statement_timestamp())
    )
    WITH CHECK (deleted_at IS NOT NULL);
COMMIT;
