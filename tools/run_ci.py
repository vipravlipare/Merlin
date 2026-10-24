"""Verify cumulative work on fresh, owned CI storage without changing local guards.

Only exact identity literals are instantiated in a temporary source copy. The
original migrations, local clusters and checked-out files are never rewritten.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.ci_database import CiDatabase, self_check as check_database_guards

LOCAL_CLUSTER = '7694311451826794534'
LOCAL_PROJECT = 'merlin-d6-20261008105707'
# Counts make an edited/expanded guard require review instead of blind replacement.
IDENTITY_FILES = {
    'app/notes_maintenance.py': (1, 0),
    'tools/audit_database_lifecycle.py': (1, 0),
    'tools/audit_migration_undo.py': (1, 0),
    'tools/database_sandboxes.py': (1, 0),
    'tools/database_test_session.py': (3, 1),
    'tools/verify_database_sandboxes.py': (0, 1),
    'tests/test_note_rules_and_maintenance.py': (4, 0),
    'tests/test_users_notes_database.py': (3, 1),
    'migrations/001_users_notes.down.sql': (1, 0),
    'migrations/002_whitespace_parity.down.sql': (1, 0),
    'migrations/002_whitespace_parity.up.sql': (1, 0),
}

# This floor keeps the hosted workflow cumulative. Removing an old automated
# category now requires an explicit review of this contract and the inventory.
MINIMUM_CUMULATIVE_INVENTORY = {
    'python_cases': 821,
    'python_faults': 321,
    'sql_cases': 383,
    'sql_pairs': 607,
    'lifecycle_cases': 5,
    'migration_gates': 14,
    'migration_repairs': 17,
}
MER11_REQUIRED_FAULT_WITNESSES = {
    'notes-preview-not-truncated': 'tests/test_notes_repository.py::test_active_note_list_uses_body_prefix_when_title_is_missing',
    'notes-stored-title-discarded': 'tests/test_notes_repository.py::test_active_note_list_binds_each_actor_when_connection_is_reused',
    'notes-owner-filter-removed': 'tests/test_notes_repository.py::test_active_note_list_sets_owner_and_uses_read_only_active_query',
    'notes-trash-view-bypassed': 'tests/test_notes_repository.py::test_active_note_list_sets_owner_and_uses_read_only_active_query',
    'notes-ordering-reversed': 'tests/test_notes_repository.py::test_active_note_list_sets_owner_and_uses_read_only_active_query',
    'notes-actor-setting-session-wide': 'tests/test_notes_repository.py::test_active_note_list_binds_each_actor_when_connection_is_reused',
    'notes-read-write-enabled': 'tests/test_notes_repository.py::test_active_note_list_sets_owner_and_uses_read_only_active_query',
    'notes-missing-actor-accepted': 'tests/test_notes_repository.py::test_active_note_list_rejects_missing_actor_and_busy_connection_before_query',
    'notes-malformed-actor-accepted': 'tests/test_notes_repository.py::test_active_note_list_rejects_malformed_actor_before_query',
    'notes-owner-parameter-hardcoded': 'tests/test_notes_repository.py::test_active_note_list_binds_each_actor_when_connection_is_reused',
    'notes-active-transaction-accepted': 'tests/test_notes_repository.py::test_active_note_list_rejects_missing_actor_and_busy_connection_before_query',
}
MER11_REQUIRED_CASES = {
    'tests/test_notes_repository.py::test_weighted_prefix_keeps_complete_display_units',
    'tests/test_notes_repository.py::test_active_note_list_uses_body_prefix_when_title_is_missing',
    'tests/test_notes_repository.py::test_active_note_list_sets_owner_and_uses_read_only_active_query',
    'tests/test_notes_repository.py::test_active_note_list_rejects_missing_actor_and_busy_connection_before_query',
    'tests/test_notes_repository.py::test_active_note_list_rejects_malformed_actor_before_query',
    'tests/test_notes_repository.py::test_active_note_list_binds_each_actor_when_connection_is_reused',
}
REQUIRED_SUITE_STAGES = [
    'python-tests', 'python-case-faults', 'database-case-faults',
    'database-lifecycle-faults', 'migration-undo-faults', 'documentation',
    'whitespace',
]
MAX_CUMULATIVE_SUITE_SECONDS = 60.0


def validate_cumulative_inventory(inventory):
    """Refuse a hosted run that silently drops a retained test category."""
    for name, minimum in MINIMUM_CUMULATIVE_INVENTORY.items():
        if len(inventory.get(name, [])) < minimum:
            raise ValueError('Cumulative CI inventory below reviewed floor: ' + name)
    if not MER11_REQUIRED_CASES <= set(inventory.get('python_cases', [])):
        raise ValueError('MER-11 repository cases missing from cumulative CI inventory')
    if not set(MER11_REQUIRED_FAULT_WITNESSES) <= set(inventory.get('python_faults', [])):
        raise ValueError('MER-11 faults missing from cumulative CI inventory')


def validate_mer11_fault_report(report):
    """Require each Day 10 fault to fail at its named repository assertion."""
    rows = {row.get('fault'): row for row in report.get('faults', [])}
    for fault, expected_case in MER11_REQUIRED_FAULT_WITNESSES.items():
        row = rows.get(fault, {})
        if (row.get('status') != 'DETECTED' or row.get('intended_detection') is not True
                or row.get('expected_witness_case') != expected_case
                or expected_case not in row.get('detected_by', [])):
            raise ValueError('MER-11 fault lacks its intended test witness: ' + fault)


def validate_complete_suite_summary(payload):
    """Check every required stage, cleanup gate, and the full-suite time cap."""
    rows = payload.get('stages', [])
    if ([row.get('stage') for row in rows] != REQUIRED_SUITE_STAGES
            or not all(row.get('status') == 'PASS' and row.get('exit') == 0 for row in rows)):
        raise ValueError('Incomplete or failed cumulative suite stages')
    runtime = payload.get('runtime_seconds')
    limit = payload.get('runtime_limit_seconds')
    if (isinstance(runtime, bool) or not isinstance(runtime, (int, float))
            or not math.isfinite(runtime) or limit != MAX_CUMULATIVE_SUITE_SECONDS
            or runtime > MAX_CUMULATIVE_SUITE_SECONDS):
        raise ValueError('Cumulative suite exceeded or omitted its 60-second limit')
    isolation = payload.get('execution', {}).get('database_isolation', {})
    if (isolation.get('status') != 'PASS' or isolation.get('source_preserved') is not True
            or isolation.get('cleanup_passed') is not True):
        raise ValueError('Cumulative suite isolation, preservation, or cleanup failed')


def validate_suite_evidence_files(suite_dir):
    """Require inspectable case/fault outcomes in the hosted artifact."""
    required = [
        'summary.json', 'database-isolation-controls.json',
        'merlin-python-effectiveness-final.json',
        'merlin-sql-effectiveness-final.json', 'merlin-sql-shard-0.json',
        'merlin-sql-shard-1.json', 'merlin-lifecycle-effectiveness.json',
        'migration-undo-results.json',
    ]
    missing = [name for name in required if not (suite_dir / name).is_file()]
    if missing:
        raise ValueError('Cumulative suite evidence missing: ' + ', '.join(missing))
    return required


def refresh_adapted_witness_hashes(destination, proof):
    """Re-pin only CI-adapted sources inside the copied witness manifest."""
    manifest_path = destination / 'tests/python-fault-witnesses.json'
    if not manifest_path.is_file():
        return
    manifest = json.loads(manifest_path.read_text())
    adapted_sources = []
    for source in sorted(set(IDENTITY_FILES) & set(manifest.get('source_sha256', {}))):
        source_path = destination / source
        if not source_path.is_file():
            raise ValueError('Adapted witness source missing from CI copy: ' + source)
        digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if manifest['source_sha256'][source] != digest:
            manifest['source_sha256'][source] = digest
            adapted_sources.append(source)
    if not adapted_sources:
        return
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    manifest_row = next((row for row in proof
                         if row['file'] == 'tests/python-fault-witnesses.json'), None)
    if manifest_row is None:
        raise ValueError('Adapted witness manifest missing from CI source proof')
    manifest_row['executed_sha256'] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    manifest_row['identity_adapted'] = True
    manifest_row['adapted_witness_sources'] = adapted_sources


def cumulative_scope_self_check():
    """Prove CI rejects removed MER-11 coverage and over-limit suite results."""
    checks = []
    inventory = json.loads((ROOT / 'tests/suite-inventory.json').read_text())
    validate_cumulative_inventory(inventory)
    reduced = deepcopy(inventory)
    reduced['python_cases'].remove(next(iter(MER11_REQUIRED_CASES)))
    try:
        validate_cumulative_inventory(reduced)
    except ValueError:
        checks.append('removed-MER11-case-refused')
    else:
        raise AssertionError('CI accepted an omitted MER-11 case')

    valid_faults = {
        fault: {'fault': fault, 'status': 'DETECTED', 'intended_detection': True,
                'expected_witness_case': case, 'detected_by': [case]}
        for fault, case in MER11_REQUIRED_FAULT_WITNESSES.items()
    }
    validate_mer11_fault_report({'faults': list(valid_faults.values())})
    changed_faults = deepcopy(valid_faults)
    changed_faults['notes-owner-filter-removed']['status'] = 'SURVIVED'
    try:
        validate_mer11_fault_report({'faults': list(changed_faults.values())})
    except ValueError:
        checks.append('surviving-MER11-fault-refused')
    else:
        raise AssertionError('CI accepted a surviving MER-11 fault')
    changed_faults = deepcopy(valid_faults)
    changed_faults['notes-owner-filter-removed']['expected_witness_case'] = (
        'tests/test_notes_repository.py::test_weighted_prefix_keeps_complete_display_units')
    try:
        validate_mer11_fault_report({'faults': list(changed_faults.values())})
    except ValueError:
        checks.append('wrong-MER11-witness-refused')
    else:
        raise AssertionError('CI accepted an unrelated MER-11 witness')

    summary = {
        'stages': [{'stage': name, 'status': 'PASS', 'exit': 0}
                   for name in REQUIRED_SUITE_STAGES],
        'runtime_seconds': 60.0,
        'runtime_limit_seconds': 60.0,
        'execution': {'database_isolation': {
            'status': 'PASS', 'source_preserved': True, 'cleanup_passed': True}},
    }
    validate_complete_suite_summary(summary)
    summary['runtime_seconds'] = 60.001
    try:
        validate_complete_suite_summary(summary)
    except ValueError:
        checks.append('over-60-second-suite-refused')
    else:
        raise AssertionError('CI accepted a suite over the 60-second limit')
    summary['runtime_seconds'] = float('nan')
    try:
        validate_complete_suite_summary(summary)
    except ValueError:
        checks.append('invalid-suite-runtime-refused')
    else:
        raise AssertionError('CI accepted a non-finite suite runtime')

    with tempfile.TemporaryDirectory(prefix='merlin-ci-witness-hash-') as directory:
        destination = Path(directory)
        test_source = 'tests/test_note_rules_and_maintenance.py'
        test_path = destination / test_source
        test_path.parent.mkdir(parents=True)
        test_path.write_text('ADAPTED_ID = 8888888888888888888\n')
        old_manifest = json.dumps({'schema_version': 1,
                                   'source_sha256': {test_source: '0' * 64},
                                   'witnesses': {}}, indent=2) + '\n'
        manifest_path = destination / 'tests/python-fault-witnesses.json'
        manifest_path.write_text(old_manifest)
        proof = [{'file': 'tests/python-fault-witnesses.json',
                  'source_sha256': hashlib.sha256(old_manifest.encode()).hexdigest(),
                  'executed_sha256': hashlib.sha256(old_manifest.encode()).hexdigest(),
                  'identity_adapted': False}]
        refresh_adapted_witness_hashes(destination, proof)
        refreshed = json.loads(manifest_path.read_text())
        expected_hash = hashlib.sha256(test_path.read_bytes()).hexdigest()
        assert refreshed['source_sha256'][test_source] == expected_hash
        assert proof[0]['adapted_witness_sources'] == [test_source]
        assert proof[0]['executed_sha256'] == hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        checks.append('adapted-witness-hash-repinned-and-recorded')
    return checks


def instantiate_identity(name, raw, cluster, project):
    if name not in IDENTITY_FILES:
        raise ValueError('Unreviewed identity-adaptation file')
    if (not re.fullmatch(r'[1-9][0-9]{0,19}', cluster)
            or cluster in {LOCAL_CLUSTER, '7691749973399031842'}
            or not re.fullmatch(r'merlin-ci-[0-9a-f]{32}', project)):
        raise ValueError('Invalid independently owned CI identity')
    text = raw.decode('utf-8')
    if (text.count(LOCAL_CLUSTER), text.count(LOCAL_PROJECT)) != IDENTITY_FILES[name]:
        raise ValueError('Identity guard changed; review adaptation before running CI: ' + name)
    adapted = text.replace(LOCAL_CLUSTER, cluster).replace(LOCAL_PROJECT, project)
    if adapted.replace(cluster, LOCAL_CLUSTER).replace(project, LOCAL_PROJECT) != text:
        raise ValueError('Identity adaptation was not reversible')
    return adapted.encode('utf-8')


def copy_inputs(destination, cluster, project, *, include_untracked=False):
    command = ['git', 'ls-files', '-z']
    names = set(subprocess.check_output(command, cwd=ROOT).decode().split('\0'))
    if include_untracked:
        # Explicit working-tree verification includes deliberate deletions.
        # Normal hosted runs still refuse a missing tracked input.
        names.difference_update(subprocess.check_output(
            ['git', 'ls-files', '--deleted', '-z'], cwd=ROOT).decode().split('\0'))
        names.update(subprocess.check_output(
            ['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0'))
    proof = []
    for name in sorted(names - {''}):
        relative = Path(name)
        if (relative.is_absolute() or '..' in relative.parts or '.git' in relative.parts
                or (relative.name.startswith('.env') and relative.name != '.env.example')):
            raise ValueError('Private or unsafe source path refused')
        source = ROOT / relative
        if (source.is_symlink() or not source.is_file()
                or not source.resolve().is_relative_to(ROOT)
                or any((ROOT / Path(*relative.parts[:index])).is_symlink()
                       for index in range(1, len(relative.parts)))):
            raise ValueError('Source input must be a regular file: ' + name)
        raw = source.read_bytes()
        adapted = instantiate_identity(name, raw, cluster, project) if name in IDENTITY_FILES else raw
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(adapted)
        proof.append({'file': name, 'source_sha256': hashlib.sha256(raw).hexdigest(),
                      'executed_sha256': hashlib.sha256(adapted).hexdigest(),
                      'identity_adapted': raw != adapted})
    if set(IDENTITY_FILES) != {row['file'] for row in proof if row['identity_adapted']}:
        raise ValueError('Required identity source missing from CI input')
    refresh_adapted_witness_hashes(destination, proof)
    (destination / '.venv').symlink_to(ROOT / '.venv', target_is_directory=True)
    # Compose reads this while resolving -p/project labels. It never supplies an
    # actual password or publishes the separately created Unix-only CI database.
    private = destination / '.env'
    private.write_text('POSTGRES_USER=merlin_d6\nPOSTGRES_DB=merlin_d6\nPOSTGRES_PASSWORD=synthetic-ci-unused\n')
    private.chmod(0o600)
    subprocess.run(['git', 'init', '-q', str(destination)], check=True, capture_output=True)
    subprocess.run(['git', 'add', '-A'], cwd=destination, check=True, capture_output=True)
    return proof


def self_check():
    checks = []
    cluster = '8888888888888888888'
    project = 'merlin-ci-' + 'a' * 32
    raw = ("EXPECTED_CLUSTER = " + LOCAL_CLUSTER + "\n").encode()
    transformed = instantiate_identity('app/notes_maintenance.py', raw, cluster, project)
    assert transformed == b'EXPECTED_CLUSTER = 8888888888888888888\n'
    checks.append('literal-identity-only')
    for name, content, identity, owner in [
        ('unreviewed.py', raw, cluster, project),
        ('app/notes_maintenance.py', raw + raw, cluster, project),
        ('app/notes_maintenance.py', b'EXPECTED_CLUSTER = 0\n', cluster, project),
        ('app/notes_maintenance.py', raw, LOCAL_CLUSTER, project),
        ('app/notes_maintenance.py', raw, '7691749973399031842', project),
        ('app/notes_maintenance.py', raw, "1';SELECT 1", project),
        ('app/notes_maintenance.py', raw, cluster, LOCAL_PROJECT),
    ]:
        try:
            instantiate_identity(name, content, identity, owner)
        except ValueError:
            checks.append('refusal-' + str(len(checks)))
        else:
            raise AssertionError('Unsafe CI identity adaptation accepted')
    checks.extend(row['scenario'] for row in check_database_guards())
    with tempfile.TemporaryDirectory(prefix='merlin-ci-integrity-') as directory:
        original, copied = Path(directory) / 'original', Path(directory) / 'copy'
        original.mkdir()
        copied.mkdir()
        (original / 'sample.py').write_text('VALUE = 1\n')
        (copied / 'sample.py').write_text('VALUE = 2\n')
        proof = [{'file': 'sample.py', 'source_sha256': hashlib.sha256(b'VALUE = 1\n').hexdigest(),
                  'executed_sha256': hashlib.sha256(b'VALUE = 2\n').hexdigest()}]
        verify_inputs(proof, copied, original)
        checks.append('source-and-executed-integrity-positive')
        for target in [original, copied]:
            before = (target / 'sample.py').read_bytes()
            (target / 'sample.py').write_text('VALUE = 3\n')
            try:
                verify_inputs(proof, copied, original)
            except ValueError:
                checks.append('changed-original-refused' if target == original else 'changed-executed-refused')
            else:
                raise AssertionError('Changed CI input accepted')
            (target / 'sample.py').write_bytes(before)
        (copied / 'sample.py').unlink()
        (original / 'same-executed-bytes.py').write_text('VALUE = 2\n')
        (copied / 'sample.py').symlink_to(original / 'same-executed-bytes.py')
        try:
            verify_inputs(proof, copied, original)
        except ValueError:
            checks.append('redirected-executed-file-refused')
        else:
            raise AssertionError('Redirected CI input accepted')
    # Exercise real Git manifests in owned temporary directories. The opt-in
    # working-tree mode must omit deleted files; ordinary CI must refuse them.
    from unittest.mock import patch
    with tempfile.TemporaryDirectory(prefix='merlin-ci-deleted-input-') as directory:
        original = Path(directory) / 'original'
        original.mkdir()
        (original / '.gitignore').write_text('.env\n.venv\n')
        (original / 'retained.py').write_text('VALUE = 1\n')
        removed = original / 'personal-quiz.js'
        removed.write_text('// Synthetic deleted fixture.\n')
        subprocess.run(['git', 'init', '-q', str(original)], check=True, capture_output=True)
        subprocess.run(['git', 'add', '-A'], cwd=original, check=True, capture_output=True)
        removed.unlink()
        for include in [False, True]:
            copied = Path(directory) / str(include)
            copied.mkdir()
            with patch.dict(globals(), {'ROOT': original, 'IDENTITY_FILES': {}}):
                try:
                    proof = copy_inputs(copied, cluster, project, include_untracked=include)
                except ValueError as error:
                    assert not include and 'Source input must be a regular file' in str(error)
                else:
                    assert include and not (copied / removed.name).exists()
                    assert 'retained.py' in {row['file'] for row in proof}
            checks.append('deleted-working-input-omitted' if include else 'missing-hosted-input-refused')
    baseline = {'status': 'PASS', 'rebuilt_cases': ['synthetic-case'], 'rebuilt_case_count': 2,
                'source_preserved': True, 'migration_sha256': {'migration': 'a' * 64},
                'disposable_evidence': {'cleanup_passed': True, 'source_preserved': True},
                'captured_pre_001_baseline': {'public_create': False, 'schema_snapshot': {}},
                'checks': [{'case': name, 'passed': True} for name in migration_checks(1)]}
    validate_roundtrip(baseline, ['synthetic-case', RECONNECT], {'migration': 'a' * 64})
    checks.append('committed-roundtrip-evidence-positive')
    for field, value in [('rebuilt_cases', []), ('rebuilt_case_count', 1),
                         ('source_preserved', False), ('migration_sha256', {}),
                         ('checks', []), ('disposable_evidence', {'cleanup_passed': False})]:
        candidate = deepcopy(baseline)
        candidate[field] = value
        try:
            validate_roundtrip(candidate, ['synthetic-case', RECONNECT], {'migration': 'a' * 64})
        except ValueError:
            checks.append('roundtrip-refuses-' + field)
        else:
            raise AssertionError('Contradictory migration PASS accepted: ' + field)
    checks.extend(cumulative_scope_self_check())
    print('CI identity adaptation, isolation and refusal controls PASS', flush=True)
    return checks


RECONNECT = 'test_failed_second_write_rolls_back_first_write_after_reconnect'


def migration_checks(count):
    return ['fresh-database-and-external-prerequisite', 'initial-up-001-and-002-committed',
            'down-002-committed', 'down-001-committed-and-verified-after-reconnect',
            'up-001-and-002-committed-semantic-equivalence', 'all-rebuilt-database-cases-' + str(count),
            'rebuilt-failed-write-and-real-reconnect', 'reconnected-empty-tables-and-unrelated-data-preserved',
            'source-preservation-and-disposable-cleanup']


def validate_roundtrip(payload, cases, hashes):
    ordinary = [case for case in cases if case != RECONNECT]
    rows = payload.get('checks', [])
    evidence = payload.get('disposable_evidence', {})
    baseline = payload.get('captured_pre_001_baseline', {})
    if (payload.get('status') != 'PASS' or payload.get('rebuilt_cases') != ordinary
            or payload.get('rebuilt_case_count') != len(cases) or RECONNECT not in cases
            or payload.get('source_preserved') is not True
            or evidence.get('cleanup_passed') is not True or evidence.get('source_preserved') is not True
            or payload.get('migration_sha256') != hashes
            or type(baseline.get('public_create')) is not bool or 'schema_snapshot' not in baseline
            or [row.get('case') for row in rows] != migration_checks(len(ordinary))
            or not all(row.get('passed') is True for row in rows)):
        raise ValueError('Incomplete or contradictory committed migration evidence')


def verify_inputs(proof, copied, original=ROOT):
    """Check the parent-owned manifest, not a child's claim about its inputs."""
    for row in proof:
        for root, key in [(original, 'source_sha256'), (copied, 'executed_sha256')]:
            path = root / row['file']
            if (not path.is_file() or path.is_symlink()
                    or not path.resolve().is_relative_to(root.resolve())
                    or any((root / Path(*Path(row['file']).parts[:index])).is_symlink()
                           for index in range(1, len(Path(row['file']).parts)))
                    or hashlib.sha256(path.read_bytes()).hexdigest() != row[key]):
                raise ValueError('CI input changed or redirected during verification')


def execute(command, *, cwd, env, timeout):
    process = subprocess.Popen(command, cwd=cwd, env=env, start_new_session=True)
    try:
        code = process.wait(timeout=timeout)
        if code:
            raise RuntimeError('Required CI check failed: ' + Path(command[1]).name)
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGINT)
            try:
                process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', help='Immutable Docker image ID from the pinned CI Dockerfile')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--include-untracked', action='store_true', help='Explicit local pre-commit verification')
    parser.add_argument('--self-check', action='store_true')
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error('CI verification requires enabled assertions')
    if args.self_check:
        self_check()
        return 0
    if not args.image or not args.out:
        parser.error('--image and --out are required')
    if not args.include_untracked and subprocess.run(
            ['git', 'diff', '--quiet', 'HEAD'], cwd=ROOT).returncode:
        parser.error('Commit reviewed inputs first, or explicitly use --include-untracked for local verification')
    output = args.out.resolve()
    if output.exists() and any(output.iterdir()):
        parser.error('Output directory must be new or empty')
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    summary = {'status': 'FAIL', 'steps': [], 'source_commit': subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'includes_uncommitted_inputs': args.include_untracked}
    started = time.monotonic()
    database = CiDatabase(args.image)
    current_step = 'source-provisioning'
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    previous = signal.signal(signal.SIGTERM, interrupted)
    try:
        self_check()
        with tempfile.TemporaryDirectory(prefix='merlin-ci-inputs-') as directory:
            copied = Path(directory)
            with database:
                current_step = 'source-inputs'
                proof = copy_inputs(copied, database.cluster, database.project,
                                    include_untracked=args.include_untracked)
                (output / 'source-inputs.json').write_text(json.dumps(proof, indent=2) + '\n')
                inventory = json.loads((copied / 'tests/suite-inventory.json').read_text())
                validate_cumulative_inventory(inventory)
                summary['reviewed_inventory_counts'] = {
                    name: len(inventory[name]) for name in MINIMUM_CUMULATIVE_INVENTORY
                }
                current_step = 'migration-bootstrap'
                database.bootstrap(copied)
                summary['target'] = {'container': database.source, 'cluster': database.cluster,
                                     'project': database.project, 'network': 'none'}
                env = dict(os.environ, PYTHONPATH=str(copied))
                for key in ['MERLIN_DB_SANDBOX', 'MERLIN_DB_SQL_SECOND', 'PYTEST_ADDOPTS', 'PGPASSWORD']:
                    env.pop(key, None)
                env.update(MERLIN_FAST_DB_TESTS='1', MERLIN_RUN_DB_TESTS='1',
                           MERLIN_DB_ISOLATION='1', MERLIN_SQL_SHARDS='2',
                           MERLIN_PYTHON_FAULT_SCOPE='dependent',
                           MERLIN_PYTHON_FAULT_WORKERS='20', PYTHONOPTIMIZE='')
                python = str(ROOT / '.venv/bin/python')
                # First exercise the original Python sources, then all database
                # and fault cases in the verifiably identity-instantiated copy.
                verify_inputs(proof, copied)
                current_step = 'original-python-sources'
                execute([python, '-m', 'pytest', '-q', 'tests', 'tools/test_doctor.py',
                         '--ignore=tests/test_users_notes_database.py', '--tb=short'],
                        cwd=ROOT, env=dict(env, PYTHONPATH=str(ROOT)), timeout=180)
                summary['steps'].append({'name': 'original-python-sources', 'status': 'PASS'})
                for name, script, result in [
                    ('complete-suite', 'tools/run_test_suite.py', output / 'suite'),
                    ('committed-migration-roundtrip', 'tools/verify_migration_roundtrip.py', output / 'migration.json'),
                ]:
                    verify_inputs(proof, copied)
                    current_step = name
                    command = [python, script, '--out-dir' if name == 'complete-suite' else '--out', str(result)]
                    execute(command, cwd=copied, env=env, timeout=600)
                    payload = json.loads((result / 'summary.json' if name == 'complete-suite' else result).read_text())
                    if payload.get('status') != 'PASS':
                        raise RuntimeError('CI result validation failed: ' + name)
                    if name == 'complete-suite':
                        validate_complete_suite_summary(payload)
                        python_report = json.loads(
                            (result / 'merlin-python-effectiveness-final.json').read_text())
                        validate_mer11_fault_report(python_report)
                        evidence_files = validate_suite_evidence_files(result)
                        summary['suite_evidence_sha256'] = {
                            path: hashlib.sha256((result / path).read_bytes()).hexdigest()
                            for path in evidence_files
                        }
                    else:
                        inventory = json.loads((copied / 'tests/suite-inventory.json').read_text())
                        hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in (copied / 'migrations').glob('*.sql')}
                        validate_roundtrip(payload, inventory['sql_cases'], hashes)
                    summary['steps'].append({'name': name, 'status': 'PASS'})
                verify_inputs(proof, copied)
            summary['status'] = 'PASS'
    except (Exception, KeyboardInterrupt) as error:
        summary['failure_type'] = type(error).__name__
        summary['first_failed_step'] = current_step
        print('CI verification failed; inspect the first failed required stage.', file=sys.stderr)
    finally:
        signal.signal(signal.SIGTERM, previous)
        summary['seconds'] = round(time.monotonic() - started, 3)
        summary['cleanup_passed'] = database.cleanup_passed
        (output / 'ci-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return int(summary['status'] != 'PASS' or not summary['cleanup_passed'])


if __name__ == '__main__':
    raise SystemExit(main())
