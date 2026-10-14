"""Committed-fixture reconnect and concurrency tests on the isolated Day 6 DB.

Unlike the rollback-only suite, these explicitly commit synthetic UUID rows so
two database sessions can see them. Teardown deletes only those users, cascading
only their notes. Schema mutations remain transaction-local and roll back.
Never run alongside the empty-database suite or another lifecycle audit.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import selectors
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.native_psql import run as native_run
spec = importlib.util.spec_from_file_location("database_case_audit", ROOT / "tools/audit_database_cases.py")
audit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)
module, _ = audit.load_cases()

GATE = """DO $gate$ BEGIN
IF current_database()<>'merlin_d6' OR (SELECT system_identifier::text FROM pg_control_system())<>'7694311451826794534'
THEN RAISE EXCEPTION 'Unexpected lifecycle target'; END IF; END $gate$;
"""


def sql(text):
    result = native_run(module.COMMAND, input=text, text=True, capture_output=True, timeout=20)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.splitlines()


def fixtures(mode, user, first, second):
    name = "life_" + uuid.uuid4().hex[:10]
    sql("BEGIN;" + GATE + f"INSERT INTO public.users(id,username) VALUES ('{user}','{name}');"
        f"INSERT INTO public.notes(id,user_id,title,body,device_created_at,device_edited_at) VALUES "
        f"('{first}','{user}','First','real body',now(),now()),('{second}','{user}','Second','real body',now(),now());"
        + (f"UPDATE public.notes SET body='' WHERE user_id='{user}';SET LOCAL session_replication_role=replica;"
           f"UPDATE public.notes SET blank_body_expires_at=now()-CASE WHEN id='{first}' THEN interval '2 days' ELSE interval '1 day' END WHERE user_id='{user}';" if mode == "expiry" else
           f"SET LOCAL session_replication_role=replica;UPDATE public.notes SET deleted_at=now()-CASE WHEN id='{first}' THEN interval '16 days' ELSE interval '15 days' END WHERE user_id='{user}';" if mode == "purge" else "")
        + "SET LOCAL session_replication_role=origin;COMMIT;")


def holder(first):
    process = subprocess.Popen(module.COMMAND, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.stdin.write("BEGIN;" + GATE + "SET LOCAL statement_timeout='10s';SET LOCAL idle_in_transaction_session_timeout='15s';"
                        f"SELECT id FROM public.notes WHERE id='{first}' FOR UPDATE;SELECT 'LOCK_READY';\n")
    process.stdin.flush()
    with selectors.DefaultSelector() as selector:
        selector.register(process.stdout, selectors.EVENT_READ)
        # One SQL output line combines row identity and readiness, avoiding a
        # second line hidden in Python's text buffer while select waits.
        if not selector.select(10):
            process.terminate();process.communicate(timeout=5)
            raise AssertionError("Holder never acknowledged its row lock")
        assert process.stdout.readline().strip() == first
        assert process.stdout.readline().strip() == "LOCK_READY"
    return process


def execute(case, faulty=False):
    audit.preservation(module)
    mode = "purge" if case == "purge-skips-locked" else "expiry" if case != "committed-reconnect-cascade" else "normal"
    user, first, second = (str(uuid.uuid4()) for _ in range(3))
    lock = None
    try:
        fixtures(mode, user, first, second)
        if case == "committed-reconnect-cascade":
            assert sql(GATE + f"SELECT count(*),bool_and(body='real body') FROM public.notes WHERE user_id='{user}';") == ['2|t']
            # Mutate only the deletion predicate, never committed schema. A
            # UUIDv4 user cannot have the all-zero UUID. The faulty no-op still
            # commits; the same fresh-connection oracle must catch its rows.
            target = '00000000-0000-0000-0000-000000000000' if faulty else user
            sql("BEGIN;" + GATE + f"DELETE FROM public.users WHERE id='{target}';COMMIT;")
            assert sql(GATE + f"SELECT count(*) FROM public.notes WHERE user_id='{user}';") == ['0']
        elif case == "second-operation-failure-rolls-back-cleanup":
            # Both statements run in the same actual PostgreSQL transaction.
            result = native_run(module.COMMAND, input="\\set VERBOSITY verbose\nBEGIN;" + GATE
                + "SET LOCAL ROLE merlin_d6_maintenance;SELECT public.cleanup_expired_blank_notes(1);"
                + ("COMMIT;BEGIN;" if faulty else "")
                + "SELECT public.purge_deleted_notes(0);ROLLBACK;", text=True, capture_output=True, timeout=20)
            assert result.returncode == 3 and 'P0001' in result.stderr and 'Batch size must be between 1 and 1000' in result.stderr
            assert sql(GATE + f"SELECT count(*) FROM public.notes WHERE user_id='{user}' AND deleted_at IS NOT NULL;") == ['0']
        else:
            name = "purge_deleted_notes" if mode == "purge" else "cleanup_expired_blank_notes"
            if case.endswith("skips-locked"):
                lock = holder(first)
                old, new = "FOR UPDATE SKIP LOCKED", "FOR UPDATE"
            else:
                old, new = "LIMIT batch_size FOR UPDATE SKIP LOCKED", "FOR UPDATE SKIP LOCKED"
            fault = audit.edit_function(name + "(integer)", old, new) if faulty else ""
            check = f"SELECT public.{name}(1);"
            if mode == "expiry":
                check += f"SELECT count(*) FROM public.notes WHERE user_id='{user}' AND deleted_at IS NOT NULL;"
            else:
                check += f"SELECT count(*) FROM public.notes WHERE user_id='{user}';"
            if lock:
                check += (f"SELECT (SELECT deleted_at IS NULL FROM public.notes WHERE id='{first}'),"
                          f"(SELECT deleted_at IS NULL FROM public.notes WHERE id='{second}');" if mode == "expiry" else
                          f"SELECT EXISTS(SELECT 1 FROM public.notes WHERE id='{first}'),EXISTS(SELECT 1 FROM public.notes WHERE id='{second}');")
            lines = sql("BEGIN;" + GATE + fault + "SET LOCAL lock_timeout='1s';SET LOCAL statement_timeout='3s';"
                        "SET LOCAL ROLE merlin_d6_maintenance;" + check + "ROLLBACK;")
            assert lines == (['1','1','t|f'] if lock else ['1','1']), f"Wrong batch effect: {lines}"
        return {"outcome": "passed"}
    except AssertionError as error:
        return {"outcome": "failed", "failure": str(error)}
    finally:
        if lock:
            lock.stdin.write("ROLLBACK;\n");lock.stdin.flush();lock.communicate(timeout=5)
        if user:
            sql("BEGIN;" + GATE + f"DELETE FROM public.users WHERE id='{user}';COMMIT;")
        audit.preservation(module)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    original = audit.preservation(module)
    rows = []
    for case in ["committed-reconnect-cascade", "expiry-skips-locked", "purge-skips-locked", "expiry-batch-limit", "second-operation-failure-rolls-back-cleanup"]:
        baseline = execute(case)
        mutated = execute(case, True) if baseline['outcome'] == 'passed' else {"outcome": "unexecuted"}
        rows.append({"case": case, "baseline": baseline, "mutation": mutated,
                     "effectiveness": "DEMONSTRATED" if baseline['outcome'] == 'passed' and mutated['outcome'] == 'failed' else "NOT_DEMONSTRATED"})
        print(json.dumps(rows[-1]), flush=True)
    final = audit.preservation(module)
    args.out.write_text(json.dumps({"cases": rows,"preserved":original==final,"original_fingerprint":original,"final_fingerprint":final},indent=2)+'\n')
    if original != final or any(row['effectiveness'] != 'DEMONSTRATED' for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
