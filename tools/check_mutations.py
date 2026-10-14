"""Check known behavioral faults in memory; application files and databases stay untouched."""

import pathlib, subprocess, sys, re, argparse, json, os, tempfile
from concurrent.futures import ThreadPoolExecutor
root=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
n='app/note_rules.py'; m='app/notes_maintenance.py'
cases=[
('emoji-weight-one',n,'4 if emoji.is_emoji(part) else 1','1 if emoji.is_emoji(part) else 1'),
('codepoint-instead-of-grapheme',n,'_GRAPHEMES.findall(value)','value'),
('title-bound-relaxed',n,'title_length > 175','title_length > 176'),
('title-bound-too-strict',n,'title_length > 175','title_length >= 175'),
('body-bound-relaxed',n,'weighted_length(body) > 7000','weighted_length(body) > 7001'),
('body-bound-too-strict',n,'weighted_length(body) > 7000','weighted_length(body) >= 7000'),
('body-stripped',n,'body = "" if body is None else body','body = "" if body is None else body.strip()'),
('real-title-stripped',n,'return ValidatedNote(title, body,','return ValidatedNote(None if title is None else title.strip(), body,'),
('email-lowercased',n,'return value.strip() or None','return value.strip().lower() or None'),
('blank-title-stored-empty',n,'if not title.strip():\n            title = None','if not title.strip():\n            title = ""'),
('draft-delete-protection-removed',n,'not is_draft and title is None and not body.strip()','title is None and not body.strip()'),
('nul-check-removed',n,'if "\\x00" in value:','if False:'),
('target-check-skipped',m,'        verify_target(conn)\n','        pass\n'),
('identity-or-changed-to-and',m,'database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER','database != "merlin_d6" and int(identifier) != EXPECTED_CLUSTER'),
('target-port-original-db',m,'port=55432','port=5432'),
('batch1001-allowed',m,'1 <= batch_size <= 1000','1 <= batch_size <= 1001'),
('lock-timeout-removed',m,'            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n',''),
('wrong-expiry-function',m,'SELECT public.cleanup_expired_blank_notes(%s)','SELECT public.wrong_cleanup(%s)'),
('once-flag-ignored',m,'if args.once:','if False:'),
('custom-interval-ignored',m,'time.sleep(args.interval)','time.sleep(60)'),
('cli-error-secret-leaked',m,'raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")','raise SystemExit("Maintenance failed: " + password)'),
('strict-batch-guard-removed',m,'if type(batch_size) is not int:','if False:'),
('strict-draft-guard-removed',n,'if not isinstance(is_draft, bool):','if False:'),
('utf8-guard-removed',n,'value.encode("utf-8")','pass'),
('unexpected-extra-sql',m,'            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))','            cur.execute("SELECT 42")\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))')]
# Each additional fault changes an observable rule, not formatting or comments.
cases += [
('email-padding-retained',n,'return value.strip() or None','return value or None'),
('optional-email-empty-string',n,'if value is None:\n        return None','if value is None:\n        return ""'),
('empty-email-empty-string',n,'return value.strip() or None','return value.strip()'),
('none-body-not-normalized',n,'body = "" if body is None else body','body = body'),
('draft-title-bypasses-limit',n,'elif title_length > 175:','elif not is_draft and title_length > 175:'),
('draft-body-bypasses-limit',n,'if weighted_length(body) > 7000:','if not is_draft and weighted_length(body) > 7000:'),
('save-default-is-draft',n,'is_draft: bool = False','is_draft: bool = True'),
('text-type-guard-disabled',n,'if not isinstance(value, str):','if False:'),
('valid-unicode-rejected-ascii',n,'value.encode("utf-8")','value.encode("ascii")'),
('nul-only-at-start',n,'if "\\x00" in value:','if value.startswith("\\x00"):') ,
('valid-body-erased',n,'return ValidatedNote(title, body,','return ValidatedNote(title, "",'),
('valid-title-erased',n,'return ValidatedNote(title, body,','return ValidatedNote(None, body,'),
('blank-save-never-deletes',n,'not is_draft and title is None and not body.strip()','False'),
('target-host-public',m,'host="127.0.0.1"','host="0.0.0.0"'),
('target-database-original',m,'dbname="merlin_d6"','dbname="merlin_db"'),
('target-user-original',m,'user="merlin_d6"','user="merlin"'),
('connection-timeout-unbounded',m,'connect_timeout=3','connect_timeout=0'),
('batch-zero-allowed',m,'1 <= batch_size <= 1000','0 <= batch_size <= 1000'),
('batch1000-rejected',m,'1 <= batch_size <= 1000','1 <= batch_size <= 999'),
('statement-timeout-removed',m,'            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n',''),
('purge-parameter-altered',m,'cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))','cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size - 1,))'),
('cleanup-counts-swapped',m,'return expired, purged','return purged, expired'),
('early-explicit-commit',m,'            expired = cur.fetchone()[0]','            expired = cur.fetchone()[0]\n            conn.commit()'),
('default-interval-altered',m,'default=60','default=59'),
('nine-second-interval-allowed',m,'args.interval < 10','args.interval < 9'),
('ten-second-interval-rejected',m,'args.interval < 10','args.interval < 11'),
('runtime-error-not-sanitized',m,'except (psycopg.Error, RuntimeError):','except psycopg.Error:'),
('output-counts-swapped',m,'Expired title-only notes: {expired}; purged deleted notes: {purged}','Expired title-only notes: {purged}; purged deleted notes: {expired}'),
('interrupt-message-omitted',m,'print("Maintenance stopped")','pass'),
]

# Generic validation errors must not echo private input.
cases.append(('nul-error-echoes-input',n,'raise ValueError("PostgreSQL text cannot contain NUL")',
              'raise ValueError("PostgreSQL text cannot contain NUL: " + value)'))

def script(case, basetemp=None):
 name,file,old,new=case
 source=(root/file).read_text()
 if source.count(old)!=1:return None
 source=source.replace(old,new,1)
 module=file[:-3].replace('/','.')
 arguments=['tests/test_note_rules_and_maintenance.py','-q']
 if basetemp:arguments.append('--basetemp='+str(basetemp))
 return f'import importlib,pytest; m=importlib.import_module({module!r}); exec(compile({source!r},{file!r},"exec"),m.__dict__); raise SystemExit(pytest.main({arguments!r}))'

def outcome(case, code, stdout):
 name=case[0]
 if code is None:return dict(defect=name,status='TIMEOUT')
 match=re.search(r'(\d+) failed',stdout)
 status='DETECTED' if code==1 and match and 'ERROR collecting' not in stdout else ('SURVIVED' if code==0 else 'INVALID')
 return dict(defect=name,status=status,failed_cases=int(match[1]) if match else 0, tests=re.findall(r'^FAILED (\S+)',stdout,re.MULTILINE))

def run(case):
 source=script(case)
 if source is None:return dict(defect=case[0],status='INVALID',reason='Source match count changed')
 try:r=subprocess.run([sys.executable,'-c',source],cwd=root,capture_output=True,text=True,timeout=30)
 except subprocess.TimeoutExpired:return outcome(case,None,'')
 return outcome(case,r.returncode,r.stdout)

def fast_run():
 from tools.isolated_python import fork_jobs
 with tempfile.TemporaryDirectory(prefix='merlin-legacy-faults-') as directory:
  jobs=[]
  for index,case in enumerate(cases):
   folder=pathlib.Path(directory)/str(index);folder.mkdir()
   code=script(case,folder/'pytest')
   if code is None:raise RuntimeError('Source match count changed: '+case[0])
   jobs.append({'code':code,'argv':[], 'stdout':str(folder/'stdout'),'stderr':str(folder/'stderr')})
  return [outcome(case,code,stdout) for case,(code,stdout,stderr) in
          zip(cases,fork_jobs(jobs,workers=min(8,len(os.sched_getaffinity(0))),timeout=30))]

if __name__=='__main__':
 # A failing baseline cannot prove that an injected fault was detected.
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--report', type=pathlib.Path, help='Write detailed mutation evidence as JSON')
 args=parser.parse_args()
 baseline=subprocess.run([sys.executable,'-m','pytest','tests/test_note_rules_and_maintenance.py','-q'],cwd=root)
 if baseline.returncode:raise SystemExit('Baseline must pass before mutation checks')
 if os.environ.get("MERLIN_FAST_PYTHON_TESTS")=="1":results=fast_run()
 else:
  with ThreadPoolExecutor(max_workers=min(8, len(os.sched_getaffinity(0)))) as pool:results=list(pool.map(run,cases))
 for row in results:print(f"{row['defect']}: {row['status']} ({row.get('failed_cases',0)} failing cases)")
 if args.report:args.report.write_text(json.dumps(results,indent=2)+'\n')
 print(f"Detected {sum(row['status']=='DETECTED' for row in results)}/{len(results)} injected faults")
 raise SystemExit(any(row['status']!='DETECTED' for row in results))
