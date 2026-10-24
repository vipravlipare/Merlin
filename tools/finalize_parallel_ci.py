"""Join verified Python fault shards with the isolated database CI component."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def timestamp(value):
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('CI timing evidence must include a UTC offset')
    return parsed


def parallel_wall_seconds(intervals):
    """Measure wall time from the first lane start to the last lane finish."""
    if not intervals:
        raise ValueError('Parallel CI timing requires at least one lane')
    starts = [timestamp(start) for start, _ in intervals]
    finishes = [timestamp(finish) for _, finish in intervals]
    if any(finish < start for start, finish in zip(starts, finishes)):
        raise ValueError('Parallel CI lane finished before it started')
    return (max(finishes) - min(starts)).total_seconds()


def self_check():
    """Check overlap, offset, missing-clock and reversed-clock handling."""
    lanes = [('2026-10-24T10:00:00+00:00', '2026-10-24T10:00:30+00:00'),
             ('2026-10-24T10:00:10+00:00', '2026-10-24T10:00:50+00:00')]
    assert parallel_wall_seconds(lanes) == 50
    for candidate in [
        [('2026-10-24T10:00:00', '2026-10-24T10:00:30+00:00')],
        [('2026-10-24T10:00:30+00:00', '2026-10-24T10:00:00+00:00')],
        [],
    ]:
        try:
            parallel_wall_seconds(candidate)
        except ValueError:
            continue
        raise AssertionError('Invalid parallel CI clock evidence was accepted')
    return ['overlap-measured-once', 'missing-offset-refused',
            'reversed-lane-refused', 'empty-lane-list-refused']


def finalize(database_dir, python_shard_dir, output_dir):
    from tools.merge_python_fault_shards import merge_reports
    from tools.run_ci import (
        MAX_CUMULATIVE_SUITE_SECONDS,
        MER11_REQUIRED_CASES,
        MER11_REQUIRED_FAULT_WITNESSES,
        REQUIRED_SUITE_STAGES,
        validate_complete_suite_summary,
        validate_cumulative_inventory,
        validate_database_component_summary,
        validate_mer11_fault_report,
        validate_suite_evidence_files,
    )

    database_dir = database_dir.resolve()
    output_dir = output_dir.resolve()
    component = json.loads((database_dir / 'ci-summary.json').read_text())
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if (component.get('status') != 'PASS_COMPONENT'
            or component.get('component') != 'database-and-baseline'
            or component.get('source_commit') != head
            or component.get('includes_uncommitted_inputs') is not False
            or component.get('cleanup_passed') is not True):
        raise ValueError('Database CI component is not a clean result for this exact commit')

    suite_dir = database_dir / 'suite'
    summary_path = suite_dir / 'summary.json'
    suite = json.loads(summary_path.read_text())
    validate_database_component_summary(suite)

    inventory = json.loads((ROOT / 'tests/suite-inventory.json').read_text())
    validate_cumulative_inventory(inventory)
    python_report = merge_reports(
        [json.loads(path.read_text())
         for path in sorted(python_shard_dir.glob('python-fault-shard-*/report.json'))],
        inventory,
    )
    validate_mer11_fault_report(python_report)
    reported_cases = {row.get('case') for row in python_report.get('matrix', [])}
    if not MER11_REQUIRED_CASES <= reported_cases:
        raise ValueError('Merged Python report omitted a required MER-11 case')

    fault_times = python_report['fault_shards']
    combined_runtime = parallel_wall_seconds([
        (suite['started_utc'], suite['finished_utc']),
        (fault_times['started_utc'], fault_times['finished_utc']),
    ])
    if combined_runtime < 0 or combined_runtime > MAX_CUMULATIVE_SUITE_SECONDS:
        raise ValueError('Parallel cumulative tests exceeded their 60-second wall-clock limit')

    python_stage = next(row for row in suite['stages']
                        if row['stage'] == 'python-case-faults')
    python_stage.update(status='PASS', exit=0,
                        seconds=fault_times['parallel_wall_seconds'],
                        external='validated-python-fault-shard-matrix',
                        fault_count=len(python_report['faults']),
                        case_count=len(python_report['matrix']))
    suite['status'] = 'PASS'
    suite['runtime_seconds'] = round(combined_runtime, 3)
    suite['runtime_limit_seconds'] = MAX_CUMULATIVE_SUITE_SECONDS
    suite['external_python_fault_shards'] = fault_times
    suite['execution']['python_fault_shards'] = fault_times['count']
    suite['execution']['python_fault_parallel_seconds'] = fault_times['parallel_wall_seconds']
    (suite_dir / 'merlin-python-effectiveness-final.json').write_text(
        json.dumps(python_report, ensure_ascii=True, separators=(',', ':')) + '\n')
    summary_path.write_text(json.dumps(suite, indent=2) + '\n')

    if [row.get('stage') for row in suite.get('stages', [])] != REQUIRED_SUITE_STAGES:
        raise ValueError('Final suite stage order differs from the cumulative contract')
    validate_complete_suite_summary(suite)
    evidence_files = validate_suite_evidence_files(suite_dir)
    hashes = {name: hashlib.sha256((suite_dir / name).read_bytes()).hexdigest()
              for name in evidence_files}

    component.update(status='PASS', component='complete-cumulative-suite',
                     parallel_suite_runtime_seconds=round(combined_runtime, 3),
                     python_fault_shards=fault_times['count'],
                     python_fault_report_sha256=hashlib.sha256(
                         (suite_dir / 'merlin-python-effectiveness-final.json').read_bytes()).hexdigest(),
                     python_fault_shard_sha256={
                         path.parent.name: hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in sorted(python_shard_dir.glob('python-fault-shard-*/report.json'))
                     },
                     suite_evidence_sha256=hashes)
    component['steps'].append({'name': 'python-fault-shard-merge-and-MER-11-validation',
                               'status': 'PASS', 'faults': len(python_report['faults']),
                               'cases': len(python_report['matrix'])})
    component['steps'] = [
        {**row, 'status': 'PASS'} if row.get('name') == 'complete-suite' else row
        for row in component['steps']
    ]
    if not any(row.get('name') == 'complete-suite' and row.get('status') == 'PASS'
               for row in component['steps']):
        raise ValueError('Database component omitted its full non-Python-fault suite result')
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'ci-summary.json').write_text(json.dumps(component, indent=2) + '\n')
    return {'status': 'PASS', 'source_commit': head,
            'parallel_suite_runtime_seconds': round(combined_runtime, 3),
            'python_faults': len(python_report['faults']),
            'python_cases': len(python_report['matrix']),
            'mer11_witness_faults': len(MER11_REQUIRED_FAULT_WITNESSES),
            'database_cleanup_passed': component['cleanup_passed']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database-dir', type=Path, required=True)
    parser.add_argument('--python-shards', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    result = finalize(args.database_dir, args.python_shards, args.out_dir)
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
