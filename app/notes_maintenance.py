"""Foreground scheduler restricted to the known disposable Day 6 cluster."""

import argparse
import getpass
import time

import psycopg

# These fixed settings protect Sprint 0; this worker is for disposable storage only.
EXPECTED_CLUSTER = 7694311451826794534
TARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)


def verify_target(conn) -> None:
    """Fail closed before writes; never accept another database or cluster."""
    # Read the cluster fingerprint before allowing any cleanup writes.
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")
        identity = cur.fetchone()
    try:
        database, identifier = identity
        identifier = int(identifier)
    except (ValueError, TypeError):
        raise RuntimeError("Refusing malformed Day 6 database identity") from None
    if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER:
        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")


def run_once(password: str, batch_size: int = 100) -> tuple[int, int]:
    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)
    if type(batch_size) is not int:
        raise ValueError("Batch size must be an integer")
    if not 1 <= batch_size <= 1000:
        raise ValueError("Batch size must be between 1 and 1000")
    # This context commits on success and rolls back both cleanups if either fails.
    with psycopg.connect(**TARGET, password=password) as conn:
        verify_target(conn)
        with conn.cursor() as cur:
            # Stop a cycle rather than waiting indefinitely for locks or slow queries.
            cur.execute("SET LOCAL lock_timeout = '2s'")
            cur.execute("SET LOCAL statement_timeout = '10s'")
            # %s binds a value safely; never build SQL by joining user input.
            # First remove expired title-only notes, then purge old soft deletions.
            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))
            expired = cur.fetchone()[0]
            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))
            purged = cur.fetchone()[0]
    return expired, purged


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")
    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")
    args = parser.parse_args()
    if args.interval < 10:
        parser.error("Interval must be at least 10 seconds")
    # Prompt without echoing the password; do not store it in the source file.
    password = getpass.getpass("Disposable merlin_d6 password: ")
    try:
        # The scheduler runs only while this foreground process remains open.
        while True:
            expired, purged = run_once(password)
            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")
            # --once performs one cycle; otherwise pause before the next cycle.
            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Maintenance stopped")
    # Avoid printing connection details or credentials in database errors.
    except (psycopg.Error, RuntimeError):
        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")


if __name__ == "__main__":
    main()
