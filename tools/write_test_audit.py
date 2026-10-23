"""Render case-by-case evidence from completed, genuine audit runs."""
import argparse
from collections import Counter
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("/tmp"))
    parser.add_argument("--output", type=Path, default=ROOT / "docs/testing/case-effectiveness-evidence")
    args = parser.parse_args()
    names = {"python":"merlin-python-effectiveness-final.json", "sql":"merlin-sql-effectiveness-final.json",
             "lifecycle":"merlin-lifecycle-effectiveness.json"}
    data = {key: json.loads((args.input / name).read_text()) for key,name in names.items()}
    sql_rows = data['sql']['cases']
    assert all(row['effectiveness'] == 'DEMONSTRATED' for row in sql_rows)
    assert all(row['outcome'] == 'passed' and row['detects'] for row in data['python']['matrix'])
    assert all(row['effectiveness'] == 'DEMONSTRATED' for row in data['lifecycle']['cases'])
    assert data['sql']['preserved'] and data['lifecycle']['preserved']
    # Refuse stale evidence if current Python/product/test sources changed.
    for file,digest in data['python']['source_sha256'].items():
        # Report rendering can change after the run without changing tested
        # behavior. Require freshness for product code and actual test inputs.
        if file.startswith('tools/') and file not in {'tools/doctor.py','tools/prd_lint.py','tools/test_doctor.py','tools/audit_python_cases.py','tools/check_mutations.py'}:
            continue
        assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest() == digest, f'Stale evidence: {file}'
    assert hashlib.sha256((ROOT/'tests/test_users_notes_database.py').read_bytes()).hexdigest() == data['sql']['source_sha256']
    args.output.mkdir(parents=True,exist_ok=True)
    archive_names = {"python":"python-test-results", "sql":"database-test-results",
                     "lifecycle":"database-lifecycle-results"}
    for key,payload in data.items():
        (args.output/(archive_names[key]+'.json.gz')).write_bytes(gzip.compress((json.dumps(payload,ensure_ascii=True)+'\n').encode(),mtime=0))
    def esc(value): return str(value).replace('|','\\|').replace('\n',' ').replace('[','&lbrack;').replace(']','&rbrack;').replace('<','&lt;').replace('>','&gt;').replace('href=','href&#61;')
    catalog = ["# Injected fault catalogue", "", "Faults exist only in audit copies, memory or isolated transactions. A surviving experiment is not a passing product test. Invalid harness runs never count as fault detections.", ""]
    def table(filename,title,rows):
        text=[f'# {title}', '', 'Each row is an individually executed case. PASS means the current implementation passed its assertions; fault IDs name experiments in which that same case failed.', '', '| Case | Requirement / location | Baseline | Detected faults |', '|---|---|---|---|']
        text += ['| '+' | '.join(esc(cell) for cell in row)+' |' for row in rows]
        text += ['', '[Fault catalogue](fault-catalogue.md) · [Audit report](../case-effectiveness-audit.md)', '']
        (args.output/filename).write_text('\n'.join(text))
    from tools.audit_python_cases import faults
    recipes={name:(file,old,new) for name,file,old,new in faults()}
    py_ids={row['fault']:f'PY-M{index:03}' for index,row in enumerate(data['python']['faults'],1)}
    catalog += ['## Python', '', '| ID | Fault | Status | Source change |','|---|---|---|---|']
    for row in data['python']['faults']:
        file,old,new=recipes[row['fault']]
        if old.startswith('#!') or len(old)>1000:
            changes=[line for line in difflib.ndiff(old.splitlines(),new.splitlines()) if line.startswith(('- ','+ '))]
            change=' ; '.join(changes)
        else: change=old+' → '+new
        catalog.append('| '+' | '.join(esc(v) for v in [py_ids[row['fault']],row['fault'],row['status'],file+': '+change])+' |')
    table('python-cases.md','Python cases and individual subtests',[[row['case'],f"{row['file']}:{row['line']}"+(' (subtest)' if row.get('kind')=='subtest' else ''),'PASS',', '.join(py_ids[name] for name in row['detects'])] for row in data['python']['matrix']])
    sql_groups={}
    for row in sql_rows:
        for fault in row['faults']:
            identity=fault.get('sql',fault['name'])
            group=sql_groups.setdefault(identity,{'id':f'SQL-M{len(sql_groups)+1:03}','names':set(),'results':[]})
            group['names'].add(fault['name']);group['results'].append(fault['status'])
    catalog += ['', '## PostgreSQL', '', 'The same transaction-local schema fault was paired with several cases. Its status records all pair outcomes; it need not break unrelated behavior.', '', '| ID | Fault | Pair outcomes | Transaction-local SQL |','|---|---|---|---|']
    for identity,group in sql_groups.items():
        catalog.append('| '+' | '.join(esc(v) for v in [group['id'],', '.join(sorted(group['names'])),dict(Counter(group['results'])),identity])+' |')
    table('database-cases.md','PostgreSQL cases',[[row['case'],row['rule'],'PASS',', '.join(sql_groups[f.get('sql',f['name'])]['id'] for f in row['faults'] if f['status'].startswith('DETECTED'))] for row in sql_rows])
    lifecycle_rows=[]
    catalog += ['', '## PostgreSQL lifecycle', '', '| ID | Fault | Status |','|---|---|---|']
    descriptions=['Remove the note-owner foreign key during account deletion','Remove SKIP LOCKED from expiry cleanup','Remove SKIP LOCKED from retention purge','Remove the expiry batch limit','Commit the first cleanup before the second operation fails']
    for index,(row,description) in enumerate(zip(data['lifecycle']['cases'],descriptions),1):
        ident=f'LIFE-M{index:03}'
        catalog.append('| '+' | '.join(esc(v) for v in [ident,description,'DETECTED'])+' |')
        lifecycle_rows.append([row['case'],'tools/audit_database_lifecycle.py','PASS',ident])
    table('database-lifecycle-cases.md','Committed reconnect and two-session cases',lifecycle_rows)
    (args.output/'fault-catalogue.md').write_text('\n'.join(catalog)+'\n')
    summary={'python_observations':len(data['python']['matrix']),'python_subtests':sum(row.get('kind')=='subtest' for row in data['python']['matrix']),
             'python_faults':dict(Counter(row['status'] for row in data['python']['faults'])),
             'sql_cases':len(sql_rows),'sql_fault_pairs':dict(Counter(f['status'] for row in sql_rows for f in row['faults'])),
             'sql_distinct_faults':len(sql_groups),'lifecycle_cases':len(lifecycle_rows),'preserved':True}
    (args.output/'audit-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__': main()
