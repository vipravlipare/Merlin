"""Measure real Python test outcomes and which source faults each case detects.

Faults are compiled into imported modules in fresh isolated child processes.
Product files are never rewritten. Linter CLI checks execute the actual temporary
script in isolated processes; ordinary baseline tests also verify real exec startup.
Timeouts, collection errors and unapplied mutations never count as detections.
"""

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

WORKER = r'''
import importlib,json,pathlib,sys,pytest,os,subprocess
root=pathlib.Path(sys.argv[1]); spec=json.loads(pathlib.Path(sys.argv[2]).read_text())
sys.path.insert(0,str(root));sys.path.insert(0,str(root/'tools'))
if spec['file']:
 source=pathlib.Path(spec['source']).read_text()
 names=[spec['file'][:-3].replace('/','.')]
 if spec['file']=='tools/doctor.py':names.append('doctor')
 for name in names:
  module=importlib.import_module(name)
  exec(compile(source,str(root/spec['file']),'exec'),module.__dict__)
cli_files=set()
original_run=subprocess.run
if os.environ.get('MERLIN_FAST_PYTHON_TESTS','1')=='1':
 from tools.isolated_python import run_script
 def cli_run(command,*args,**kwargs):
  if (not args and isinstance(command,list) and len(command)>=2 and command[0]==sys.executable
      and str(command[1]) in cli_files and set(kwargs)<= {'capture_output','text','timeout','cwd'}
      and kwargs.get('capture_output') is True and kwargs.get('text') is True and kwargs.get('timeout')):
   return run_script(command,**kwargs)
  return original_run(command,*args,**kwargs)
 subprocess.run=cli_run
class Record:
 def __init__(self):self.rows={};self.errors=[]
 def pytest_collection_modifyitems(self,items):
  for item in items:
   self.rows[item.nodeid]={'baseline':'collected','file':str(item.path.relative_to(root)),
     'function':item.originalname or item.name,'line':item.location[1]+1}
   if hasattr(item.module,'LINTER'):
    if spec['file']=='tools/prd_lint.py':item.module.LINTER=pathlib.Path(spec['source'])
    cli_files.add(str(item.module.LINTER))
 def pytest_runtest_logreport(self,report):
  if report.when=='call':
   row=self.rows[report.nodeid]
   if row.get('outcome')!='failed':row['outcome']=report.outcome
   if report.failed:row['failure']=str(report.longrepr)[-2400:]
   if hasattr(report,'context'):
    key=report.nodeid+'::subtest'+json.dumps(report.context.kwargs,sort_keys=True)
    self.rows[key]={**row,'kind':'subtest','outcome':report.outcome}
  elif report.failed:
   self.errors.append({'nodeid':report.nodeid,'stage':report.when,'failure':str(report.longrepr)[-1200:]})
 def pytest_collectreport(self,report):
  if report.failed:self.errors.append({'stage':'collection','failure':str(report.longrepr)[-1200:]})
record=Record()
code=pytest.main(spec.get('tests',['tests','tools/test_doctor.py'])+['--ignore=tests/test_users_notes_database.py','-q','--tb=short','--basetemp='+str(pathlib.Path(sys.argv[2]).parent/'pytest')],plugins=[record])
pathlib.Path(spec['output']).write_text(json.dumps({'exit':int(code),'cases':record.rows,'errors':record.errors},ensure_ascii=True,indent=2))
raise SystemExit(code)
'''


def faults():
    spec = importlib.util.spec_from_file_location("existing_faults", ROOT / "tools/check_mutations.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = [(name, file, old, new) for name, file, old, new in module.cases]
    p = "app/database_connectivity_probe.py"
    d = "tools/doctor.py"
    l = "tools/prd_lint.py"
    n = "app/note_rules.py"
    m = "app/notes_maintenance.py"
    rows += [
        ("probe-only-operational-errors", p, "except psycopg.Error:", "except psycopg.OperationalError:"),
        ("probe-leaks-error", p, 'print("DB Probe Failed: Connection or query failed.", file=sys.stderr)',
         'print("DB Probe Failed: " + password, file=sys.stderr)'),
        ("probe-wrong-failure-status", p, "sys.exit(1)", "sys.exit(0)"),
        ("probe-wrong-success-status", p, "sys.exit(0)", "sys.exit(1)"),
        ("probe-not-read-only", p, "conn.read_only = True", "conn.read_only = False"),
        ("probe-wrong-port", p, "port=55432", "port=5432"),
        ("probe-fetch-twice", p, "db_name, db_user = cur.fetchone()", "db_name, db_user = cur.fetchone(); cur.fetchone()"),
        ("probe-mask-programming-bug", p, "except psycopg.Error:", "except Exception:"),
        ("probe-extra-query", p, 'cur.execute("SELECT current_database(), current_user;")',
         'cur.execute("SELECT 42"); cur.execute("SELECT current_database(), current_user;")'),
        ("probe-error-on-stdout", p, "file=sys.stderr", "file=sys.stdout"),
        ("worker-malformed-identity-not-sanitized", m, 'raise RuntimeError("Refusing malformed Day 6 database identity") from None', "raise"),
        ("text-plain-weight-zero", n, "else 1 for part", "else 0 for part"),
        ("text-all-empty-rejected", n, "return sum(", 'if value == "": raise ValueError("Empty text rejected")\n    return sum('),
        ("text-drafts-all-delete", n, "not is_draft and title is None and not body.strip()", "is_draft or (title is None and not body.strip())"),
        ("text-all-emails-null", n, "return value.strip() or None", "return None"),
        ("text-whitespace-body-trimmed", n, 'body = "" if body is None else body', 'body = "" if body is None else body.strip()'),
        ("doctor-command-timeout-unbounded", d, "timeout=30,", "timeout=None,"),
        ("doctor-command-raises-on-errors", d, "check=False,", "check=True,"),
        ("doctor-command-does-not-capture", d, "capture_output=True", "capture_output=False"),
        ("doctor-command-ignores-cwd", d, "cwd=root", "cwd=None"),
        ("doctor-timeout-reports-success", d, "return subprocess.CompletedProcess(args, 127, '', '')", "return subprocess.CompletedProcess(args, 0, '', '')"),
        ("doctor-negative-auth-accepts-any-error", d, "negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()", "negative.returncode != 0"),
        ("doctor-negative-auth-accepts-success", d, "negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()", "negative.returncode == 0 or 'password authentication failed' in negative.stderr.lower()"),
        ("doctor-nested-inspection-guard-disabled", d, "ports = host.get('PortBindings', {})", "return health, host, mounts, labels\n            ports = host.get('PortBindings', {})"),
        ("doctor-malformed-manifest-crashes", d, "except (OSError, ValueError, KeyError, TypeError):", "except (OSError, ValueError, KeyError):"),
        ("doctor-missing-manifest-pin-crashes", d, "except (OSError, ValueError, KeyError, TypeError):", "except (OSError, ValueError, TypeError):"),
        ("doctor-all-python-pins-accepted", d, "python_ok = declared in", "python_ok = True or declared in"),
        ("doctor-unicode-port-crash", d, "bool(re.fullmatch(r'[0-9]{1,5}', str(bindings[0].get('HostPort', ''))))", "str(bindings[0].get('HostPort', '')).isdigit()"),
        ("worker-invalid-interval-falls-back", m, 'type=int, default=60', 'type=lambda value: int(value) if value.isdecimal() else 60, default=60'),
        ("worker-help-disabled", m, 'argparse.ArgumentParser(description=__doc__)', 'argparse.ArgumentParser(description=__doc__, add_help=False)'),
        ("worker-unknown-flags-ignored", m, 'args = parser.parse_args()', 'args, unknown = parser.parse_known_args()'),
        ("doctor-timeout-leaks-secret", d, "return subprocess.CompletedProcess(args, 127, '', '')", "print(str(args)); return subprocess.CompletedProcess(args, 127, '', '')"),
        ("doctor-static-runs-runtime", d, "if not self.static and available:", "if available:"),
        ("doctor-all-reports-pass", d, "status = 'PASS' if ok else 'WARN' if warn else 'FAIL'", "status = 'PASS'"),
        ("doctor-all-reports-fail", d, "status = 'PASS' if ok else 'WARN' if warn else 'FAIL'", "status = 'FAIL'"),
        ("doctor-no-failure-accounting", d, "self.failures += int(status == 'FAIL')", "self.failures += 0"),
        ("doctor-inspect-always-refuses", d, "return health, host, mounts, labels", "return None"),
        ("doctor-inspect-shape-guard-disabled", d, "if not (isinstance(health, str)", "if False and not (isinstance(health, str)"),
        ("doctor-requests-secret-environment", d, "{{json .State.Health.Status}}", "{{json .Config.Env}}"),
        ("doctor-service-auth-wrong-query", d, '''base + "'SELECT 1'"''', '''base + "'SELECT 2'"'''),
        ("doctor-service-password-not-negative", d, '${POSTGRES_PASSWORD}__doctor_wrong', '${POSTGRES_PASSWORD}'),
        ("doctor-host-password-not-negative", d, "password + '__doctor_wrong'", "password"),
        ("doctor-host-public-interface", d, "'-h', '127.0.0.1', '-p', pg_port", "'-h', '0.0.0.0', '-p', pg_port"),
        ("doctor-host-password-in-command", d, "'-Atqc', 'SELECT 1']", "'-Atqc', 'SELECT 1', password]"),
        ("doctor-cluster-expected-ignored", d, "self.expect_cluster is None or observed == self.expect_cluster", "True"),
        ("doctor-cluster-always-refuses", d, "valid and (self.expect_cluster is None or observed == self.expect_cluster)", "False"),
        ("doctor-cluster-assumes-original", d, "self.expect_cluster is None or observed == self.expect_cluster", "observed == '7691749973399031842'"),
        ("linter-empty-tree-passes", l, 'return 1\n', 'return 0\n'),
        ("linter-legacy-folder-not-expanded", l, 'return folder.parent', 'return folder'),
        ("linter-link-check-disabled", l, 'if not destination.exists():', 'if False:'),
        ("linter-existing-targets-rejected", l, 'if not destination.exists():', 'if True:'),
        ("linter-percent-encoding-not-decoded", l, 'unquote(parsed.path)', 'parsed.path'),
        ("linter-checks-code-examples", l, 'if fence is not None:\n            continue', 'if False:\n            continue'),
        ("linter-inline-examples-checked", l, 'line = re.sub(r"(`+).*?\\1", "", line)', 'line = line'),
        ("linter-code-limit-relaxed", l, 'MAX_CODE_LINES = 15', 'MAX_CODE_LINES = 16'),
        ("linter-code-limit-too-strict", l, 'MAX_CODE_LINES = 15', 'MAX_CODE_LINES = 14'),
    ]
    # Mutate comparisons and boolean operators at individual source locations.
    # Each changed program must compile; unsupported/equivalent faults are visible.
    for file in [p, m, n, d, l]:
        source = (ROOT / file).read_text()
        lines = source.splitlines(keepends=True)
        offsets = [0]
        for line in lines:
            offsets.append(offsets[-1] + len(line))
        for index, node in enumerate(ast.walk(ast.parse(source))):
            if not isinstance(node, (ast.Compare, ast.BoolOp)):
                continue
            segment = ast.get_source_segment(source, node)
            copy = ast.parse("(" + segment + ")", mode="eval")
            candidate = copy.body
            changed = False
            swaps = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE,
                     ast.LtE: ast.Gt, ast.Gt: ast.LtE, ast.GtE: ast.Lt,
                     ast.Is: ast.IsNot, ast.IsNot: ast.Is}
            if isinstance(candidate, ast.Compare) and len(candidate.ops) == 1 and type(candidate.ops[0]) in swaps:
                candidate.ops[0] = swaps[type(candidate.ops[0])]()
                changed = True
            elif isinstance(candidate, ast.BoolOp):
                candidate.op = ast.Or() if isinstance(candidate.op, ast.And) else ast.And()
                changed = True
            if changed:
                start = offsets[node.lineno - 1] + node.col_offset
                end = offsets[node.end_lineno - 1] + node.end_col_offset
                mutated = source[:start] + "(" + ast.unparse(copy) + ")" + source[end:]
                # Source columns are UTF-8 byte offsets. Keep ASCII-only segments
                # so character slicing cannot move a mutation to another location.
                if segment.isascii() and source[start:end] == segment:
                    rows.append((f"ast-{Path(file).stem}-{node.lineno}-{index}", file, source, mutated))
    return rows



def _import_guards(tree):
    return [ast.dump(node, include_attributes=False) for node in ast.walk(tree)
            if isinstance(node, ast.Compare) and isinstance(node.left, ast.Name)
            and node.left.id == "__name__" and len(node.comparators) == 1
            and isinstance(node.comparators[0], ast.Constant)
            and node.comparators[0].value == "__main__"]


def is_import_guard_reversal(original, mutated):
    """Identify reversed __main__ guards structurally, independent of fault IDs."""
    return _import_guards(ast.parse(original)) != _import_guards(ast.parse(mutated))


def canonical_faults(rows):
    """Keep one execution per complete faulty AST; preserve alias provenance."""
    prepared, aliases, excluded, invalid = [], [], [], []
    seen = {}
    originals = {}
    for name, file, old, new in rows:
        if file not in originals:
            original = (ROOT / file).read_text()
            originals[file] = (original, _import_guards(ast.parse(original)),
                               hashlib.sha256(original.encode()).hexdigest())
        original, original_guards, source_digest = originals[file]
        if old not in original:
            invalid.append({"fault": name, "file": file, "status": "UNAPPLIED", "reason": "Source text missing"})
            continue
        source = original.replace(old, new)
        try:
            tree = ast.parse(source)
            compile(tree, file, "exec")
        except SyntaxError as error:
            invalid.append({"fault": name, "file": file, "status": "INVALID", "reason": str(error)})
            continue
        if original_guards != _import_guards(tree):
            excluded.append({"fault": name, "file": file, "status": "EXCLUDED_INVALID",
                             "reason": "Import-guard reversal tests harness startup, not application behavior",
                             "detected_by": []})
            continue
        signature = (file, ast.dump(tree, include_attributes=False))
        # This semantic proof depends on the reviewed Doctor source: observed
        # is always str, so (expect_cluster is None and observed == None) is false.
        # Both source and complete faulty AST are pinned. A change executes the
        # fault normally, as does a partial selection without the canonical fault.
        if (name == "ast-doctor-208-1251" and file == "tools/doctor.py"
                and source_digest == "4cf276effb197aad39ce94f652e01a558ca39ad3bbebe8af5ce9ce4693fae26f"
                and hashlib.sha256(signature[1].encode()).hexdigest() ==
                    "9c29b5136b16ba15b3f21eb4fe528ee0f039b3f5f2fe92b4dd4091d171f07598"
                and "doctor-cluster-always-refuses" in seen.values()):
            aliases.append({"fault": name, "file": file, "status": "ALIAS",
                            "canonical_fault": "doctor-cluster-always-refuses", "detected_by": [],
                            "reason": "Reviewed str observed cannot equal None; conjunction always false",
                            "proof_source_sha256": source_digest,
                            "proof_mutated_ast_sha256": hashlib.sha256(signature[1].encode()).hexdigest()})
            continue
        if signature in seen:
            aliases.append({"fault": name, "file": file, "status": "ALIAS",
                            "canonical_fault": seen[signature], "detected_by": [],
                            "reason": "Identical complete-module AST; no duplicate execution"})
            continue
        seen[signature] = name
        prepared.append((name, file, source))
    return prepared, aliases, excluded, invalid


def request(name, file, source, directory, tests=None):
    work = Path(directory) / name
    work.mkdir()
    original = ROOT / file if file else None
    mutated = work / "source.py"
    mutated.write_text(source)
    output = work / "results.json"
    request = work / "request.json"
    payload = {"file": file, "source": str(mutated), "output": str(output)}
    if tests is not None:
        payload['tests'] = tests
    request.write_text(json.dumps(payload))
    return {'name': name, 'file': file, 'output': output,
            'argv': [str(ROOT), str(request)], 'code': WORKER,
            'stdout': work / 'stdout.log', 'stderr': work / 'stderr.log', 'tests': tests}


def outcome(job, code, stderr):
    name, file, output = job['name'], job['file'], job['output']
    if code is None:
        return {"fault": name, "file": file, "status": "TIMEOUT", "cases": {}}
    if not output.exists():
        return {"fault": name, "file": file, "status": "INVALID", "cases": {}, "reason": stderr[-1600:]}
    data = json.loads(output.read_text())
    expected = job.get('expected_cases')
    actual = {node for node, row in data['cases'].items() if row.get('kind') != 'subtest'}
    valid = not data["errors"] and code in (0, 1) and (expected is None or actual == expected)
    detected = [node for node, row in data["cases"].items() if row.get("outcome") == "failed"]
    return {"fault": name, "file": file, "status": ("DETECTED" if detected else "SURVIVED") if valid else "INVALID",
            "detected_by": detected, "selected_test_files": job.get("tests"), "scope_manifest_matches": expected is None or actual == expected, **data}


def execute(name, file, source, directory):
    job = request(name, file, source, directory)
    try:
        result = subprocess.run([sys.executable, '-c', WORKER, *job['argv']],
                                cwd=ROOT, stdin=subprocess.DEVNULL, start_new_session=True,
                                capture_output=True, text=True, timeout=45)
        return outcome(job, result.returncode, result.stderr)
    except subprocess.TimeoutExpired:
        return outcome(job, None, '')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--only", help="Run matching fault names only")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="merlin-python-audit-") as directory:
        baseline = execute("baseline", None, "", directory)
        if baseline.get("exit") != 0 or baseline.get("errors"):
            args.out.write_text(json.dumps({"baseline": baseline}, indent=2))
            raise SystemExit("Baseline failed; mutation detections would be unreliable")
        from tools.test_dependencies import scopes
        selected = scopes(baseline) if os.environ.get('MERLIN_PYTHON_FAULT_SCOPE','dependent') != 'all' else {}
        catalog = [row for row in faults() if not args.only or args.only in row[0]]
        prepared, aliases, excluded, invalid = canonical_faults(catalog)
        results = []
        if os.environ.get('MERLIN_FAST_PYTHON_TESTS', '1') == '1':
            from tools.isolated_python import fork_jobs
            jobs = [request(*row, directory, tests=selected.get(row[1])) for row in prepared]
            for job in jobs:
                job['expected_cases'] = {node for node, row in baseline['cases'].items()
                                         if row.get('kind') != 'subtest' and
                                         (job['tests'] is None or row['file'] in job['tests'])}
            stream = (outcome(job, code, stderr) for job, (code, stdout, stderr)
                      in zip(jobs, fork_jobs(jobs, workers=min(8, max(1, int(os.environ.get("MERLIN_PYTHON_FAULT_WORKERS", "8"))), len(os.sched_getaffinity(0))))))
            for result in stream:
                results.append(result)
                if len(results) % 20 == 0:
                    print(f"Executed {len(results)}/{len(prepared)} faults", flush=True)
        else:
            with ThreadPoolExecutor(max_workers=min(8, max(1, int(os.environ.get("MERLIN_PYTHON_FAULT_WORKERS", "8"))), len(os.sched_getaffinity(0)))) as pool:
                results = list(pool.map(lambda row: execute(*row, directory), prepared))
        matrix = []
        for node, row in baseline["cases"].items():
            kills = [r["fault"] for r in results if r["status"] == "DETECTED" and node in r.get("detected_by", [])]
            matrix.append({"case": node, **row, "detects": kills,
                           "effectiveness": "DEMONSTRATED" if kills else "NO_MATCHING_DETECTION"})
        fingerprints = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for folder in ["app", "tests", "tools"] for p in (ROOT / folder).glob("*.py")}
        payload = {"source_sha256": fingerprints, "baseline": baseline, "faults": results + invalid + aliases + excluded, "fault_aliases": aliases,
                   "excluded_invalid_diagnostics": excluded,
                   "executed_fault_ids": [row[0] for row in prepared],
                   "catalog_fault_ids": [row[0] for row in catalog], "matrix": matrix}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n")
        counts = {status: sum(r["status"] == status for r in results + invalid)
                  for status in ["DETECTED", "SURVIVED", "INVALID", "TIMEOUT", "UNAPPLIED"]}
        print(json.dumps({"cases": len(matrix), "demonstrated": sum(bool(r["detects"]) for r in matrix), "faults": counts, "aliases": len(aliases), "excluded_invalid": len(excluded)}))


if __name__ == "__main__":
    main()
