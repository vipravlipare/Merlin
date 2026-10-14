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

-- Restore the previous semantics; this restores the known whitespace defect too.
ALTER TABLE public.users DROP CONSTRAINT users_email_clean;
ALTER TABLE public.users ADD CONSTRAINT users_email_clean CHECK (
    email IS NULL OR (email ~ '[^[:space:]]' AND email !~ '^[[:space:]]|[[:space:]]$')
);

ALTER TABLE public.notes DROP CONSTRAINT notes_title_nonblank;
ALTER TABLE public.notes ADD CONSTRAINT notes_title_nonblank CHECK (title IS NULL OR title ~ '[^[:space:]]');

ALTER TABLE public.notes DROP CONSTRAINT notes_has_content;
ALTER TABLE public.notes ADD CONSTRAINT notes_has_content CHECK (
        is_draft OR COALESCE(title ~ '[^[:space:]]', false) OR body ~ '[^[:space:]]'
    );

ALTER TABLE public.notes DROP CONSTRAINT notes_deadline_matches_body;
ALTER TABLE public.notes ADD CONSTRAINT notes_deadline_matches_body CHECK (
        ((is_draft OR body ~ '[^[:space:]]') AND blank_body_expires_at IS NULL)
        OR (NOT is_draft AND body !~ '[^[:space:]]' AND blank_body_expires_at IS NOT NULL)
    );

CREATE OR REPLACE FUNCTION public.manage_note_content() RETURNS TRIGGER
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

DROP POLICY notes_app_delete_limit ON public.notes;
CREATE POLICY notes_app_delete_limit ON public.notes
    AS RESTRICTIVE FOR DELETE TO merlin_d6_app
    USING (is_draft AND COALESCE(title !~ '[^[:space:]]', true) AND body !~ '[^[:space:]]');

DROP POLICY notes_maintenance ON public.notes;
CREATE POLICY notes_maintenance ON public.notes
    FOR ALL TO merlin_d6_maintenance
    USING (
        deleted_at IS NOT NULL OR
        (NOT is_draft AND body !~ '[^[:space:]]' AND blank_body_expires_at <= statement_timestamp())
    )
    WITH CHECK (deleted_at IS NOT NULL);
DROP FUNCTION public.note_email_is_clean(TEXT);
DROP FUNCTION public.note_text_is_blank(TEXT);
COMMIT;
