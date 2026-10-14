"""Verify native transport equivalence, fresh connections and server cancellation."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import signal
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.audit_database_cases import load_cases, preservation
from tools.native_psql import run, close
from tools.database_test_session import split_sql


def verify():
    module, _ = load_cases()
    original = preservation(module)
    checks = {}
    # The optimized transport must preserve PostgreSQL statement boundaries.
    lexer_cases = {
        'quoted-semicolon': ["SELECT 'a;b';", 'SELECT 2;'],
        'doubled-string-quote': ["SELECT 'a;''b';", 'SELECT 2;'],
        'quoted-identifier': ['SELECT "a;""b";', 'SELECT 2;'],
        'nested-block-comment': ['/* outer; /* inner; */ end; */ SELECT 1;', 'SELECT 2;'],
        'line-comment': ['-- ignored;\nSELECT 1;', 'SELECT 2;'],
        'dollar-body': ['DO $$ BEGIN PERFORM 1; END $$;', 'SELECT 2;'],
        'tagged-dollar-body': ['DO $body$ BEGIN PERFORM 1; END $body$;', 'SELECT 2;'],
        'escaped-string': ["SELECT E'a\\\';b';", 'SELECT 2;'],
    }
    for name, expected in lexer_cases.items():
        checks['lexer-'+name] = split_sql(''.join(expected)) == expected
    for name, broken in {'string':"SELECT 'open;", 'identifier':'SELECT "open;',
                         'dollar':'DO $body$ open;', 'block-comment':'/* open;'}.items():
        try: split_sql(broken)
        except ValueError: checks['lexer-unterminated-'+name] = True
        else: checks['lexer-unterminated-'+name] = False
    scripts = ["BEGIN;SELECT 'a;''b',NULL,42;ROLLBACK;",
               "\\set VERBOSITY verbose\nBEGIN;SELECT 1/0;SELECT 'never';ROLLBACK;",
               "\\set AUTOCOMMIT off\nBEGIN;SELECT current_database();ROLLBACK;",
               "BEGIN;SET LOCAL application_name='transport_case';SELECT current_setting('application_name');ROLLBACK;"]
    try:
        for index, script in enumerate(scripts):
            direct = subprocess.run(module.COMMAND, input=script, capture_output=True, text=True, timeout=10)
            fast = run(module.COMMAND, input=script, timeout=10)
            checks['native_equivalence_' + str(index)] = (direct.returncode, direct.stdout, direct.stderr) == (fast.returncode, fast.stdout, fast.stderr)
            expected_output = ["a;'b||42\n", '', 'merlin_d6\n', 'transport_case\n'][index]
            checks['native_expected_' + str(index)] = (fast.returncode == (3 if index == 1 else 0)
                                                       and fast.stdout == expected_output
                                                       and ('22012' in fast.stderr if index == 1 else not fast.stderr))
        # Force repeated communicate timeouts while input still exceeds pipe capacity.
        large_script = "BEGIN;SELECT pg_sleep(.15);\n--" + "x" * 400000 + "\nSELECT 1;ROLLBACK;"
        large = run(module.COMMAND, input=large_script, timeout=10)
        checks['large_script_complete'] = large.returncode == 0 and large.stdout.splitlines() == ['', '1']
        first = run(module.COMMAND, input='SELECT pg_backend_pid();', timeout=10)
        second = run(module.COMMAND, input='SELECT pg_backend_pid();', timeout=10)
        checks['fresh_connection'] = (first.returncode == second.returncode == 0
                                     and first.stdout.strip().isdigit()
                                     and second.stdout.strip().isdigit()
                                     and int(first.stdout) > 0 and int(second.stdout) > 0
                                     and first.stdout != second.stdout)
        try:
            run(module.COMMAND, input="BEGIN;SET application_name='merlin_timeout_control';SELECT pg_sleep(5);COMMIT;", timeout=.2)
        except subprocess.TimeoutExpired:
            checks['timeout_raised'] = True
        else:
            checks['timeout_raised'] = False
        remaining = run(module.COMMAND, input="SELECT count(*) FROM pg_stat_activity WHERE application_name='merlin_timeout_control';", timeout=10)
        checks['timeout_connection_closed'] = remaining.returncode == 0 and remaining.stdout.strip() == '0'
        try:
            run(['docker', 'exec', '-i', 'wrong', 'psql'], input='SELECT 1;')
        except ValueError:
            checks['wrong_container_rejected'] = True
        else:
            checks['wrong_container_rejected'] = False
        child_code = "from tools.audit_database_cases import load_cases; from tools.native_psql import run; m,_=load_cases(); run(m.COMMAND,input=\"BEGIN;SET application_name='merlin_interrupt_control';SELECT pg_sleep(5);COMMIT;\",timeout=10)"
        child = subprocess.Popen([sys.executable, '-c', child_code], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                active = run(module.COMMAND, input="SELECT count(*) FROM pg_stat_activity WHERE application_name='merlin_interrupt_control';", timeout=10)
                if active.stdout.strip() == '1':
                    break
                time.sleep(.01)
            else:
                raise RuntimeError('Interrupt control did not start its server query')
            child.send_signal(signal.SIGINT)
            child.wait(timeout=3)
            active = run(module.COMMAND, input="SELECT count(*) FROM pg_stat_activity WHERE application_name='merlin_interrupt_control';", timeout=10)
            checks['interrupt_connection_closed'] = child.returncode != 0 and active.stdout.strip() == '0'
        finally:
            if child.poll() is None:
                child.kill(); child.wait()
        checks['preserved'] = preservation(module) == original
        if not all(checks.values()):
            raise RuntimeError('Native psql verification failed: ' + str(checks))
        return checks
    finally:
        close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    checks = verify()
    if args.out:
        args.out.write_text(json.dumps(checks, indent=2) + '\n')
    print('Native psql equivalence, fresh connections, cancellation and preservation PASS')
