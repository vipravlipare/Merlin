"""Merge and validate deterministic Python fault-audit shards."""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def validate_catalog_partition(shards, expected_ids, count):
    """Require each inventory ID in its assigned shard exactly once."""
    if len(shards) != count:
        raise ValueError('Python fault shard count differs from the requested matrix')
    observed = []
    for index, report in enumerate(shards):
        metadata = report.get('shard', {})
        if metadata.get('index') != index or metadata.get('count') != count:
            raise ValueError('Python fault shard identity is missing or duplicated')
        assigned = [fault for position, fault in enumerate(sorted(expected_ids))
                    if position % count == index]
        catalog = report.get('catalog_fault_ids')
        if catalog != assigned:
            raise ValueError('Python fault shard has missing, extra, or misplaced inventory IDs')
        observed.extend(catalog)
    if len(observed) != len(set(observed)) or set(observed) != set(expected_ids):
        raise ValueError('Python fault shards do not cover the complete inventory exactly once')


def merge_reports(shards, inventory, source_root=ROOT):
    expected_ids = inventory['python_faults']
    count = len(shards)
    if not 1 <= count <= 8:
        raise ValueError('Python fault matrix must contain between 1 and 8 shards')
    shards = sorted(shards, key=lambda row: row.get('shard', {}).get('index', -1))
    validate_catalog_partition(shards, expected_ids, count)

    source_hashes = shards[0].get('source_sha256')
    baseline = shards[0].get('baseline')
    if not isinstance(source_hashes, dict) or not isinstance(baseline, dict):
        raise ValueError('Python fault shard lacks source or baseline evidence')
    expected_sources = {
        str(path.relative_to(source_root)):
        hashlib.sha256(path.read_bytes()).hexdigest()
        for folder in ('app', 'tests', 'tools')
        for path in (source_root / folder).glob('*.py')
    }
    witness = source_root / 'tests/python-fault-witnesses.json'
    expected_sources['tests/python-fault-witnesses.json'] = hashlib.sha256(witness.read_bytes()).hexdigest()

    all_rows = {}
    executed = []
    elapsed = []
    intervals = []
    for shard in shards:
        if shard.get('source_sha256') != source_hashes or shard.get('baseline') != baseline:
            raise ValueError('Python fault shards used different source or baseline evidence')
        metadata = shard['shard']
        seconds = metadata.get('elapsed_seconds')
        if (isinstance(seconds, bool) or not isinstance(seconds, (int, float))
                or not math.isfinite(seconds) or seconds < 0 or seconds > 60):
            raise ValueError('Python fault shard omitted or exceeded its 60-second budget')
        elapsed.append(float(seconds))
        try:
            started = datetime.fromisoformat(metadata['started_utc'])
            finished = datetime.fromisoformat(metadata['finished_utc'])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError('Python fault shard omitted valid UTC timing evidence') from error
        measured = (finished - started).total_seconds()
        if (started.tzinfo is None or finished.tzinfo is None or measured < 0
                or abs(measured - seconds) > 2.0):
            raise ValueError('Python fault shard timing fields contradict its elapsed time')
        intervals.append((started, finished))
        shard_rows = shard.get('faults', [])
        row_ids = [row.get('fault') for row in shard_rows]
        if (len(row_ids) != len(set(row_ids))
                or set(row_ids) != set(shard.get('catalog_fault_ids', []))):
            raise ValueError('Python fault shard rows do not match its assigned inventory')
        for row in shard_rows:
            if row.get('fault') in all_rows:
                raise ValueError('Python fault appears in more than one shard')
            all_rows[row['fault']] = row
        shard_executed = shard.get('executed_fault_ids', [])
        if len(shard_executed) != len(set(shard_executed)):
            raise ValueError('Python fault shard repeats an executed fault')
        executed.extend(shard_executed)

    if source_hashes != expected_sources:
        raise ValueError('Python fault shards do not match the checked-out source tree')
    if set(all_rows) != set(expected_ids):
        raise ValueError('Merged Python fault results differ from the reviewed inventory')

    executable = set(expected_ids) - set(inventory.get('python_aliases', {})) - {
        'ast-database_connectivity_probe-30-11', 'ast-notes_maintenance-76-42',
        'ast-doctor-229-52', 'ast-prd_lint-181-88',
    }
    if len(executed) != len(set(executed)) or set(executed) != executable:
        raise ValueError('Python fault shards did not execute every canonical mutation once')
    for fault in executable:
        row = all_rows[fault]
        if row.get('status') != 'DETECTED' or row.get('intended_detection') is not True:
            raise ValueError('Python fault lacks its intended test assertion: ' + fault)

    rows = [all_rows[fault] for fault in expected_ids]
    detections = {}
    aliases = []
    excluded = []
    for row in rows:
        if row.get('status') == 'ALIAS':
            aliases.append(row)
        elif row.get('status') == 'EXCLUDED_INVALID':
            excluded.append(row)
        elif row.get('status') != 'DETECTED':
            raise ValueError('Unexpected Python fault outcome: ' + str(row.get('status')))
        for case in row.get('detected_by', []):
            detections.setdefault(case, []).append(row['fault'])

    matrix = []
    for case, row in baseline.get('cases', {}).items():
        kills = detections.get(case, [])
        matrix.append({'case': case, **row, 'detects': kills,
                       'effectiveness': 'DEMONSTRATED' if kills else 'NO_MATCHING_DETECTION'})
    matrix_cases = [row['case'] for row in matrix]
    if len(matrix_cases) != len(inventory['python_cases']) or set(matrix_cases) != set(inventory['python_cases']):
        raise ValueError('Python fault shard baselines do not cover every reviewed test case')

    merged = {
        'source_sha256': source_hashes,
        'baseline': baseline,
        'faults': rows,
        'fault_aliases': aliases,
        'excluded_invalid_diagnostics': excluded,
        'executed_fault_ids': [fault for fault in expected_ids if fault in executable],
        'catalog_fault_ids': expected_ids,
        'matrix': matrix,
        'fault_shards': {'count': count, 'parallel_wall_seconds': max(elapsed),
                         'worker_seconds': elapsed,
                         'started_utc': min(start for start, _ in intervals).isoformat(),
                         'finished_utc': max(end for _, end in intervals).isoformat()},
    }
    return merged


def self_check():
    """Reject omitted, duplicated, and misassigned IDs in the shard layer."""
    ids = ['a', 'b', 'c', 'd']
    rows = [
        {'shard': {'index': 0, 'count': 2}, 'catalog_fault_ids': ['a', 'c']},
        {'shard': {'index': 1, 'count': 2}, 'catalog_fault_ids': ['b', 'd']},
    ]
    validate_catalog_partition(rows, ids, 2)
    for changed in [rows[:1],
                    [rows[0], {**rows[1], 'catalog_fault_ids': ['a', 'd']}],
                    [rows[0], {**rows[1], 'shard': {'index': 0, 'count': 2}}]]:
        try:
            validate_catalog_partition(changed, ids, 2)
        except ValueError:
            continue
        raise AssertionError('Invalid Python fault shard partition was accepted')
    return ['complete-partition-accepted', 'missing-shard-refused',
            'duplicate-or-misassigned-fault-refused', 'duplicate-shard-identity-refused']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--self-check', action='store_true')
    args = parser.parse_args()
    if args.self_check:
        print(json.dumps({'status': 'PASS', 'checks': self_check()}))
        return 0
    if not args.input_dir or not args.out:
        parser.error('--input-dir and --out are required unless --self-check is used')
    inventory = json.loads((ROOT / 'tests/suite-inventory.json').read_text())
    reports = [json.loads(path.read_text())
               for path in sorted(args.input_dir.glob('python-fault-shard-*/report.json'))]
    merged = merge_reports(reports, inventory)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(merged, ensure_ascii=True, separators=(',', ':')) + '\n')
    # Run the same exact full-inventory, baseline, witness, and fault-outcome
    # validator used by the cumulative suite before publishing merged evidence.
    from tools.run_test_suite import validate
    with tempfile.TemporaryDirectory(prefix='merlin-python-fault-merge-') as directory:
        folder = Path(directory)
        (folder / 'merlin-python-effectiveness-final.json').write_bytes(args.out.read_bytes())
        validate('python-case-faults', folder)
    print(json.dumps({'status': 'PASS', 'faults': len(merged['faults']),
                      'cases': len(merged['matrix']),
                      'parallel_wall_seconds': merged['fault_shards']['parallel_wall_seconds']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
