"""Run all tests and faults on verified independent disposable database copies.

No installation, application migration commit or historical-report rewrite.
A missing prerequisite or first failed stage returns nonzero. See the command
reference in docs/testing/test-suite-commands.md.
"""
import argparse
from contextlib import nullcontext
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import signal
import time

ROOT = Path(__file__).resolve().parents[1]
# Direct execution puts tools/, rather than the repository root, on sys.path.
sys.path.insert(0, str(ROOT))
PYTHON = ROOT / '.venv/bin/python'
from tools.database_sandboxes import DatabaseSandboxes
KNOWN_INVALID_IMPORT_FAULTS = {
    'ast-database_connectivity_probe-21-11', 'ast-notes_maintenance-76-42',
    'ast-doctor-229-52', 'ast-prd_lint-181-88',
}


def environment():
    env = dict(os.environ, PYTHONPATH=str(ROOT), MERLIN_RUN_DB_TESTS='1', MERLIN_FAST_DB_TESTS='1', MERLIN_FAST_PYTHON_TESTS='1', PYTHONOPTIMIZE='')
    # An inherited -k/-m/--ignore must not silently narrow a complete run.
    env.pop('PYTEST_ADDOPTS', None)
    # Only this runner may assign a freshly verified target to an individual lane.
    env.pop('MERLIN_DB_SANDBOX', None)
    env.pop('MERLIN_DB_SQL_SECOND',None)
    env.setdefault('MERLIN_SQL_SHARDS','2')
    browser_root = Path('/tmp/merlin-browser-audit')
    if not env.get('MERLIN_PLAYWRIGHT_MODULE'):
        env['MERLIN_PLAYWRIGHT_MODULE'] = str(browser_root / 'node_modules/playwright/index.mjs')
        env.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(browser_root / 'browsers'))
        env.setdefault('PLAYWRIGHT_HOST_PLATFORM_OVERRIDE', 'ubuntu24.04-x64')
        libraries = str(browser_root / 'runtime/usr/lib/x86_64-linux-gnu')
        env['LD_LIBRARY_PATH'] = libraries + (':' + env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
    return env


def stages(directory):
    py = str(PYTHON)
    return [
        ('python-tests', [py, '-m', 'pytest', '-q', 'tests', 'tools/test_doctor.py', '--tb=short']),
        ('quiz-tests', ['node', '--test', '--test-isolation=none', 'tests/quiz.test.js']),
        ('python-case-faults', [py, 'tools/audit_python_cases.py', '--out', str(directory / 'merlin-python-effectiveness-final.json')]),
        ('database-case-faults', [py, 'tools/audit_database_cases.py', '--out', str(directory / 'merlin-sql-effectiveness-final.json')]),
        ('quiz-case-faults', [py, 'tools/audit_quiz_cases.py', '--out', str(directory / 'merlin-quiz-effectiveness.json')]),
        ('browser-case-faults', ['node', 'tools/audit_quiz_browser.mjs', str(directory / 'merlin-browser-effectiveness.json')]),
        ('database-lifecycle-faults', [py, 'tools/audit_database_lifecycle.py', '--out', str(directory / 'merlin-lifecycle-effectiveness.json')]),
        ('migration-undo-faults', [py, 'tools/audit_migration_undo.py', '--out', str(directory / 'migration-undo-results.json')]),
        ('documentation', [py, 'tools/prd_lint.py', 'docs']),
        ('whitespace', ['git', 'diff', '--check']),
    ]


def preflight(env):
    if not PYTHON.is_file():
        raise RuntimeError('Missing .venv; follow the documented locked-environment setup')
    for name in ['node', 'docker', 'git']:
        if not shutil.which(name):
            raise RuntimeError('Required command missing: ' + name)
    probes = [
        [str(PYTHON), 'tools/verify_suite_execution.py'],
        [str(PYTHON), 'tools/verify_native_psql.py'],
        [str(PYTHON), '-c', "import sys,pytest,psycopg,emoji,regex; assert sys.version_info[:2]==(3,12); print('Python imports ready')"],
        ['node', '-e', "if(Number(process.versions.node.split('.')[0])!==24)process.exit(1)"],
        [str(PYTHON), '-c', 'from tools.database_test_session import DatabaseTestSession; s=DatabaseTestSession(); s.__enter__(); s.close(); print("Guarded reusable SQL transport ready")'],
        [str(PYTHON), '-c', 'from tools.audit_database_cases import load_cases,preservation; m,_=load_cases(); preservation(m); print("Disposable identity and empty tables verified")'],
        ['node', '--input-type=module', '-e', "import {pathToFileURL} from 'node:url'; const fs=await import('node:fs'); const path=await import('node:path'); const pkg=JSON.parse(fs.readFileSync(path.join(path.dirname(process.env.MERLIN_PLAYWRIGHT_MODULE),'package.json'),'utf8')); if(pkg.version!=='1.58.2') throw Error('Playwright differs from audited pin'); const {chromium}=await import(pathToFileURL(process.env.MERLIN_PLAYWRIGHT_MODULE).href); const b=await chromium.launch({headless:true}); try {if(b.version()!=='145.0.7632.6') throw Error('Browser differs from audited pin'); console.log('Chromium launch verified');} finally {await b.close();}"],
    ]
    probes.append([str(PYTHON), 'tools/verify_python_isolation.py'])
    probes.append([str(PYTHON), 'tools/run_ci.py', '--self-check'])
    def check_group(indexes):
        for index in indexes:
            command = probes[index]
            result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=45)
            if result.returncode:
                # Do not dump connection/configuration environment or private errors.
                safe_details = [line for line in result.stdout.splitlines()
                                if re.fullmatch(r'Native psql failed checks: [a-z0-9_, -]+', line)]
                detail = '; ' + safe_details[0] if safe_details else ''
                raise RuntimeError('Prerequisite check failed: ' + ('browser runtime' if command[0] == 'node' and '--input-type=module' in command else ' '.join(command[:3])) + '; see the command guide' + detail)
            if result.stdout.strip():
                print(result.stdout.strip(), flush=True)

    # Scheduling controls and runtime checks do not touch the database. Overlap
    # them with the unchanged, serial database controls. Finish every prerequisite
    # before starting baselines; a failed or timed-out prerequisite still aborts.
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [pool.submit(check_group, indexes) for indexes in
                [(0, 8), (1, 4, 5), (2, 3, 6, 7)]]
        for job in as_completed(jobs):
            job.result()


def validate(stage, directory):
    def read(name):
        return json.loads((directory / name).read_text())
    inventory = json.loads((ROOT / 'tests/suite-inventory.json').read_text())
    def complete(rows, key, expected):
        actual = [r[key] for r in rows]
        assert len(actual) == len(set(actual)) and set(actual) == set(expected), 'Incomplete or duplicate ' + stage + ' inventory'
    def current_hashes(hashes, expected):
        assert set(expected) <= set(hashes), 'Incomplete evidence source manifest'
        assert hashes and all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
                              for path, digest in hashes.items()), 'Evidence source changed'
    if stage == 'legacy-python-faults':
        rows = read('legacy-python-faults.json')
        from tools.check_mutations import cases
        complete(rows, 'defect', [case[0] for case in cases])
        assert rows and all(r['status'] == 'DETECTED' for r in rows), 'Legacy fault survived or was invalid'
    elif stage == 'python-case-faults':
        data = read('merlin-python-effectiveness-final.json')
        complete(data['matrix'], 'case', inventory['python_cases'])
        assert set(data['baseline']['cases']) == set(inventory['python_cases'])
        assert all(r['outcome'] == 'passed' for r in data['baseline']['cases'].values()), 'Python baseline outcomes contradict success'
        complete(data['faults'], 'fault', inventory['python_faults'])
        current_hashes(data['source_sha256'], [str(p.relative_to(ROOT)) for folder in ['app', 'tests', 'tools'] for p in (ROOT / folder).glob('*.py')])
        assert data['baseline']['exit'] == 0 and not data['baseline']['errors']
        assert data['matrix'] and all(r['outcome'] == 'passed' and r['detects'] for r in data['matrix']), 'Python case lacks fault detection'
        exclusions = []
        observed_aliases = {}
        for row in data['faults']:
            if row['status'] == 'ALIAS':
                assert row['fault'] in inventory['python_aliases']
                assert row['canonical_fault'] == inventory['python_aliases'][row['fault']]
                observed_aliases[row['fault']] = row['canonical_fault']
                continue
            if row['status'] == 'DETECTED':
                assert row['scope_manifest_matches'] is True, 'Mutation omitted a required dependent case'
                assert row['detected_by'] and set(row['detected_by']) <= set(inventory['python_cases'])
                assert all(row['cases'][case]['outcome'] == 'failed' for case in row['detected_by'])
                continue
            assert row['status'] == 'EXCLUDED_INVALID' and row['fault'] in KNOWN_INVALID_IMPORT_FAULTS, 'Unexpected invalid/surviving Python fault: ' + row['fault']
            exclusions.append(row['fault'])
        assert observed_aliases == inventory['python_aliases']
        assert set(exclusions) == KNOWN_INVALID_IMPORT_FAULTS
        for case in data['matrix']:
            expected_kills = {r['fault'] for r in data['faults'] if r['status'] == 'DETECTED' and case['case'] in r['detected_by']}
            assert set(case['detects']) == expected_kills, 'Python detection matrix contradicts fault outcomes'
        return {'excluded_invalid_import_faults': exclusions, 'fault_aliases': observed_aliases}
    elif stage in {'database-case-faults', 'timestamp-case-faults'}:
        data = read('merlin-sql-effectiveness-final.json' if stage == 'database-case-faults' else 'merlin-sql-F077-final.json')
        assert data['original_fingerprint'] == data['final_fingerprint'], 'SQL preservation evidence contradicts success'
        expected = inventory['sql_cases'] if stage == 'database-case-faults' else ['F077']
        complete(data['cases'], 'case', expected)
        assert data['source_sha256'] == hashlib.sha256((ROOT / 'tests/test_users_notes_database.py').read_bytes()).hexdigest()
        if stage == 'database-case-faults':
            actual_pairs = [[r['case'], f['name'], hashlib.sha256(f.get('sql', '').encode()).hexdigest(), f.get('before_seed', False)]
                            for r in data['cases'] for f in r['faults']]
            assert sorted(actual_pairs) == sorted(inventory['sql_pairs']), 'Incomplete SQL fault pair inventory'
            if (directory/'database-targets/sql-second.json').exists():
                from tools.run_sql_shards import merge, NAMES
                from tools.audit_database_cases import load_cases
                module, _ = load_cases()
                reports=[read('merlin-sql-shard-'+str(index)+'.json') for index in range(2)]
                targets=[read('database-targets/'+name+'.json') for name in NAMES]
                rebuilt=merge(reports,targets,[case.id for case in module.CASES],data['source_sha256'])
                assert data==rebuilt, 'Merged SQL evidence contradicts its independently preserved shards'
        assert data['preserved'] and data['cases'] and all(r['effectiveness'] == 'DEMONSTRATED' and r['baseline']['exit'] == 0 for r in data['cases'])
        faults = {}
        for row in data['cases']:
            for fault in row['faults']:
                assert fault['status'] not in {'INVALID', 'UNAPPLIED', 'TIMEOUT'}, 'Invalid database fault experiment'
                key = (fault['name'], fault.get('sql', ''), fault.get('before_seed', False))
                faults.setdefault(key, []).append(fault['status'])
        assert faults and all(any(s.startswith('DETECTED') for s in outcomes) for outcomes in faults.values()), 'Database fault survived the entire selected suite'
    elif stage == 'quiz-case-faults':
        data = read('merlin-quiz-effectiveness.json')
        complete(data['matrix'], 'case', inventory['quiz_cases'])
        complete(data['faults'], 'fault', inventory['quiz_faults'])
        current_hashes(data['source_sha256'], ['quizzes/sprint-0-quiz.html', 'tests/quiz.test.js'])
        assert set(data['baseline']['cases']) == set(inventory['quiz_cases'])
        assert data['baseline']['status'] == 'SURVIVED' and all(r == 'passed' for r in data['baseline']['cases'].values()), 'Quiz baseline outcomes contradict success'
        assert data['matrix'] and all(r['baseline'] == 'passed' and r['detects'] for r in data['matrix'])
        assert data['faults'] and all(r['status'] == 'DETECTED' for r in data['faults']), 'Quiz fault survived or was invalid'
        for case in data['matrix']:
            expected_kills = {r['fault'] for r in data['faults'] if r['cases'].get(case['case']) == 'failed'}
            assert set(case['detects']) == expected_kills, 'Quiz detection matrix contradicts fault outcomes'
    elif stage == 'browser-case-faults':
        data = read('merlin-browser-effectiveness.json')
        complete(data['cases'], 'case', inventory['browser_cases'])
        current_hashes(data['source_sha256'], ['quizzes/sprint-0-quiz.html', 'tools/audit_quiz_browser.mjs'])
        assert all(r['mutation']['outcome'] == 'failed' for r in data['cases'])
        assert data['cases'] and all(r['baseline']['outcome'] == 'passed' and r['mutation']['status'] == 'DETECTED' for r in data['cases'])
    elif stage == 'database-lifecycle-faults':
        data = read('merlin-lifecycle-effectiveness.json')
        complete(data['cases'], 'case', inventory['lifecycle_cases'])
        assert all(r['baseline']['outcome'] == 'passed' and r['mutation']['outcome'] == 'failed' for r in data['cases'])
        assert data['preserved'] and data['cases'] and all(r['effectiveness'] == 'DEMONSTRATED' for r in data['cases'])
    elif stage == 'migration-undo-faults':
        data = read('migration-undo-results.json')
        assert data['status'] == 'PASS' and data['preserved']
        phases = data['phases']
        assert set(phases) == {'roundtrips', 'gates', 'concurrency', 'repairs'}
        complete(phases['gates'], 'case', inventory['migration_gates'])
        complete(phases['repairs'], 'case', inventory['migration_repairs'])
        from tools.audit_database_cases import load_cases
        module, _ = load_cases()
        assert len(phases['roundtrips']) == 2
        assert {r['baseline_public_create'] for r in phases['roundtrips']} == {False, True}
        assert all(r['exit'] == 0 and
                   r['down_completed'] and r['roundtrip_completed'] and
                   r['semantic_schema_match'] and r['preserved'] for r in phases['roundtrips'])
        by_branch = {r['baseline_public_create']: r for r in phases['roundtrips']}
        assert by_branch[False]['case_count'] == len(module.CASES) and by_branch[False]['replay_mode'] == 'executed'
        assert by_branch[True]['case_count'] == 0 and by_branch[True]['replay_mode'] == 'equivalent_rebuild'
        witness_sources = ['migrations/001_users_notes.up.sql', 'migrations/001_users_notes.down.sql',
                           'migrations/002_whitespace_parity.up.sql', 'migrations/002_whitespace_parity.down.sql',
                           'tests/test_users_notes_database.py', 'tools/audit_database_cases.py', 'tools/audit_migration_undo.py']
        reference = by_branch[False]['equivalence_witness']
        arguments = module.COMMAND[module.COMMAND.index('psql'):]
        target_path = directory / 'database-targets/migration.json'
        if target_path.exists():
            from tools.database_sandboxes import validate_manifest
            target = validate_manifest(json.loads(target_path.read_text()))
            expected_command = ['docker', 'exec', '-i', target['container'],
                                'psql', '-h', target['socket'], *arguments[1:]]
        else:
            from tools.database_test_session import disposable_container
            expected_command = ['docker', 'exec', '-i', disposable_container(), *arguments]
        expected_target = hashlib.sha256(json.dumps(expected_command).encode()).hexdigest()
        for row in phases['roundtrips']:
            witness = row['equivalence_witness']
            assert all(witness[key] is True for key in ['validated','same_rebuilt_schema','same_runtime','same_source_sha256'])
            assert witness['reference_baseline_public_create'] is False and witness['reference_case_count'] == len(module.CASES)
            for dimension in ['schema', 'runtime']:
                key = dimension + '_sha256'
                assert re.fullmatch(r'[0-9a-f]{64}', witness[key])
                assert witness[key] == witness['reference_' + key] == reference[key]
            assert witness['runtime_target_sha256'] == expected_target
            assert set(witness['source_sha256']) == set(witness_sources)
            assert witness['source_sha256'] == reference['source_sha256']
            current_hashes(witness['source_sha256'], witness_sources)
        assert phases['gates'] and all(r['passed'] for r in phases['gates'])
        assert phases['repairs'] and all(r['passed'] and r['preserved'] for r in phases['repairs'])
        assert phases['concurrency']['preserved'] and set(phases['concurrency']['checks']) == {
            'other-client-refused', 'table-lock-blocks-concurrent-insert', 'wrong-database-refused'}
    return {}


def isolation_controls(directory, env):
    command=[str(PYTHON),'tools/verify_database_sandboxes.py',
                           '--targets',str(directory/'database-targets'),
                           '--out',str(directory/'database-isolation-controls.json')]
    try:
        result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=45)
    except subprocess.TimeoutExpired as error:
        output=error.stdout or b''
        (directory/'database-isolation-controls.log').write_text(output.decode() if isinstance(output,bytes) else output)
        raise
    (directory/'database-isolation-controls.log').write_text(result.stdout+result.stderr)
    if result.returncode:raise RuntimeError('Database isolation controls failed')
    controls=json.loads((directory/'database-isolation-controls.json').read_text())['checks']
    expected={'route-sql','route-lifecycle','route-migration','source-as-clone','source-volume-path',
              'wrong-source','wrong-container','crossed-socket','wrong-fingerprint',
              'public-manifest-refused','manifest-symlink-refused',
              'changed-runtime-content-invalidates-cache','missing-runtime-file-refused',
              'live-fault-isolated-from-other-copies-and-source','control-fault-rolled-back'}
    expected.update({'cpu-limit-changed','memory-limit-changed','external-network-refused',
                     'shared-source-volume-refused','published-port-refused','stale-desktop-port-refused'})
    if env.get('MERLIN_SQL_SHARDS','2')=='2':expected.add('route-sql-second')
    if len(controls)!=len(expected) or {row['case'] for row in controls}!=expected or not all(row['passed'] is True for row in controls):
        raise RuntimeError('Database isolation evidence is incomplete or failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='Print stages without running checks')
    parser.add_argument('--check', action='store_true', help='Verify prerequisites only; no fixtures or faults')
    parser.add_argument('--out-dir', type=Path, help='New or empty output directory; defaults to a unique /tmp folder')
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error("Run without -O: result validation requires enabled assertions")
    if args.list:
        for name, command in stages(Path('<run-directory>')):
            print(name + ': ' + ' '.join(command))
        return 0
    env = environment()
    # Prevent overlapping executions of this runner on the same disposable target.
    descriptor = os.open('/tmp/merlin-d6-test-suite.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, 'w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('Another complete test-suite runner holds the lock.', file=sys.stderr)
            return 1
        if args.check:
            try:
                preflight(env)
            except Exception as error:
                print(str(error), file=sys.stderr)
                return 1
            print('Prerequisites PASS; no test fixtures or fault experiments executed.')
            return 0
        directory = args.out_dir.expanduser().resolve() if args.out_dir else Path(tempfile.mkdtemp(prefix='merlin-test-suite-'))
        if directory.exists() and any(directory.iterdir()):
            print('Output directory must be new or empty.', file=sys.stderr)
            return 1
        directory.mkdir(parents=True, exist_ok=True)
        summary = {'started_utc': datetime.now(timezone.utc).isoformat(), 'stages': [], 'status': 'FAIL',
                   'execution': {'database_transport': 'guarded reusable libpq session',
                                 'python_fault_workers': min(8, max(1, int(env.get('MERLIN_PYTHON_FAULT_WORKERS','8'))), len(os.sched_getaffinity(0))),
                                 'schedule': 'independent Python and quiz lanes with isolated database lanes' if env.get('MERLIN_DB_ISOLATION','1')=='1' else 'independent Python and quiz lanes with serial database lane',
                                 'python_fault_scope': env.get('MERLIN_PYTHON_FAULT_SCOPE','dependent'),
                                 'sql_shards': 2 if env.get('MERLIN_DB_ISOLATION','1')=='1' and env.get('MERLIN_SQL_SHARDS','2')=='2' else 1}}
        print('Results: ' + str(directory), flush=True)
        try:
            plan = dict(stages(directory))
            entries = {name: {'stage': name, 'status': 'PENDING', 'exit': None} for name in plan}
            summary['stages'] = list(entries.values())
            guard = threading.RLock()
            stop = threading.Event()
            active = {}

            def save():
                with guard:
                    temporary = directory / 'summary.tmp'
                    temporary.write_text(json.dumps(summary, indent=2) + '\n')
                    temporary.replace(directory / 'summary.json')

            def terminate(process):
                if process is not None and process.poll() is None:
                    try: os.killpg(process.pid, signal.SIGINT)
                    except ProcessLookupError: pass
                    try: process.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        try: os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError: pass
                        process.wait()

            def run_stage(name, stage_env=None):
                if stop.is_set():
                    return
                entry = entries[name]
                started = time.monotonic()
                process = None
                with guard:
                    entry['status'] = 'RUNNING'
                    print('\nSTAGE: ' + name, flush=True)
                    save()
                try:
                    with (directory / (name + '.log')).open('w') as log:
                        process = subprocess.Popen(plan[name], cwd=ROOT, env=stage_env or env,
                                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                   text=True, start_new_session=True)
                        with guard:
                            active[name] = process
                        for line in process.stdout:
                            with guard:
                                print('[' + name + '] ' + line, end='', flush=True)
                            log.write(line)
                            log.flush()
                        code = process.wait()
                    entry['exit'] = code
                    if code:
                        raise RuntimeError('Stage failed: ' + name)
                    entry.update(validate(name, directory))
                    entry['status'] = 'PASS'
                except (Exception, KeyboardInterrupt) as error:
                    terminate(process)
                    entry['status'] = 'FAIL'
                    if process is not None:
                        entry['exit'] = process.returncode
                    with guard:
                        if 'failure' not in summary:
                            summary['failure'] = str(error) or 'Result validation failed: ' + name
                            summary['first_failed_stage'] = name
                        stop.set()
                        print(summary['failure'], file=sys.stderr, flush=True)
                finally:
                    with guard:
                        active.pop(name, None)
                        entry['seconds'] = round(time.monotonic() - started, 3)
                        save()

            def lane(names, stage_env=None):
                for name in names:
                    if stop.is_set():
                        break
                    run_stage(name, stage_env)

            def database_lanes(prepared=None):
                if env.get('MERLIN_DB_ISOLATION','1') != '1':
                    return lane(['migration-undo-faults','database-lifecycle-faults','database-case-faults'])
                started = time.monotonic()
                copies = prepared or DatabaseSandboxes(directory/'database-targets')
                try:
                    # Prepared copies are owned by the outer baseline/setup
                    # scope; that owner closes them after all lanes finish.
                    with nullcontext(copies) if prepared is not None else copies:
                        if stop.is_set():
                            return
                        phase=time.monotonic()
                        isolation_controls(directory,env)
                        copies.evidence['controls_seconds']=round(time.monotonic()-phase,3)
                        copies.evidence['controls_passed']=True
                        print('Independent database copies verified', flush=True)
                        def sql_lane():
                            selected=dict(env,MERLIN_DB_SANDBOX=copies.manifests['sql'])
                            if env.get('MERLIN_SQL_SHARDS','2')=='2' and plan['database-case-faults'][1]=='tools/audit_database_cases.py':
                                plan['database-case-faults']=[str(PYTHON),'tools/run_sql_shards.py',
                                    '--targets',str(directory/'database-targets'),'--out',str(directory/'merlin-sql-effectiveness-final.json')]
                            run_stage('database-case-faults',selected)
                        with ThreadPoolExecutor(max_workers=3) as database_pool:
                            jobs = [database_pool.submit(sql_lane)] + [database_pool.submit(lane, names, dict(env, MERLIN_DB_SANDBOX=copies.manifests[target]))
                                    for target,names in [('lifecycle',['database-lifecycle-faults']),
                                                         ('migration',['migration-undo-faults'])]]
                            for job in as_completed(jobs):
                                job.result()
                except Exception as error:
                    stop.set()
                    with guard:
                        summary.setdefault('failure',str(error))
                        summary.setdefault('first_failed_stage','database-isolation')
                    raise
                finally:
                    with guard:
                        copies.evidence['wall_seconds']=round(time.monotonic()-started,3)
                        summary['execution']['database_isolation']=copies.evidence
                        save()

            prepared = None
            setup_started = time.monotonic()
            # Baselines write only rollback-scoped source fixtures. PostgreSQL
            # basebackup+WAL supports concurrent clients; recovered copies must
            # still pass every identity, empty-table and fingerprint guard.
            # Preparation is not fault injection. All faults wait for BOTH
            # baseline completion and successful copy/isolation verification.
            with ThreadPoolExecutor(max_workers=1) as setup_pool:
                if env.get('MERLIN_DB_ISOLATION','1') == '1':
                    prepared = DatabaseSandboxes(directory/'database-targets')
                    setup_job = setup_pool.submit(prepared.__enter__)
                try:
                    # Copy startup has its own source-identity/storage gates.
                    # Overlap its fresh read-only backup with prerequisites;
                    # baseline and fault execution still require preflight PASS.
                    try:
                        preflight(env)
                    except Exception as error:
                        stop.set()
                        summary.setdefault('failure', str(error))
                        summary.setdefault('first_failed_stage', 'preflight')
                        raise
                    lane(['python-tests', 'quiz-tests'])
                    if prepared is not None:
                        try:
                            setup_job.result()
                        except Exception as error:
                            stop.set()
                            summary.setdefault('failure', str(error))
                            summary.setdefault('first_failed_stage', 'database-isolation')
                            raise
                    if not stop.is_set():
                        pool = ThreadPoolExecutor(max_workers=3)
                        try:
                            work = [pool.submit(lane, ['quiz-case-faults', 'browser-case-faults']),
                                    pool.submit(lane, ['python-case-faults']),
                                    pool.submit(database_lanes, prepared)]
                            for future in as_completed(work):
                                future.result()
                        except KeyboardInterrupt:
                            stop.set()
                            with guard:
                                summary.setdefault('failure', 'Interrupted; inspect fixtures before restarting')
                                processes = list(active.values())
                            for process in processes:
                                terminate(process)
                        finally:
                            pool.shutdown(wait=True)
                finally:
                    if prepared is not None:
                        # Join startup even on baseline failure/interruption.
                        # Never remove resources while creation is still active.
                        try:
                            setup_job.result()
                        finally:
                            try:
                                prepared.__exit__(None, None, None)
                            finally:
                                prepared.evidence['wall_seconds'] = round(time.monotonic()-setup_started, 3)
                                summary['execution']['database_isolation'] = prepared.evidence
                                save()
            lane(['documentation', 'whitespace'])
            if not all(entry['status'] == 'PASS' for entry in entries.values()):
                raise RuntimeError(summary.get('failure', 'Not every planned stage completed'))
            summary['status'] = 'PASS'
        except (Exception, KeyboardInterrupt) as error:
            summary.setdefault('failure', str(error) or ('Interrupted; verify disposable identity/empty rows before restarting' if isinstance(error, KeyboardInterrupt) else 'Result validation failed; inspect the last stage report'))
            print(summary['failure'], file=sys.stderr)
        finally:
            summary['finished_utc'] = datetime.now(timezone.utc).isoformat()
            (directory / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        print('FULL SUITE ' + summary['status'] + ': ' + str(directory / 'summary.json'), flush=True)
        return int(summary['status'] != 'PASS')


if __name__ == '__main__':
    raise SystemExit(main())
