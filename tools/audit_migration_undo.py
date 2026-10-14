"""Rollback-only migration undo, safety-gate and injected-defect checks.

Only the fixed empty disposable Day 6 cluster is permitted. Synthetic baseline
rows test branching; they do not establish historical permissions or authorize
committed undo. Migration files are read unchanged; 002 wrappers are removed
only in memory after an exact wrapper check. Nothing is committed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.native_psql import run as native_run
sys.path.insert(0, str(ROOT))

def roundtrips():
    import json,re,subprocess,uuid
    from pathlib import Path
    from tools import audit_database_cases as audit
    m,setup=audit.load_cases();original=audit.preservation(m)
    down=Path('migrations/001_users_notes.down.sql').read_text()
    assert not re.search(r'^COMMIT;|^ROLLBACK;',down,re.M|re.I)
    def body(path):
     s=Path(path).read_text()
     assert len(re.findall(r'^BEGIN;|^COMMIT;',s,re.M))==2
     return re.sub(r'^COMMIT;\s*\Z','',re.sub(r'^BEGIN;\n','',s,count=1,flags=re.M),count=1,flags=re.M)
    fingerprint=audit.FINGERPRINT.replace('SELECT md5(jsonb_agg(row_data ORDER BY row_data::text)::text)',"SELECT 'SCHEMA:' || jsonb_agg(row_data ORDER BY row_data::text)::text")
    roles="SELECT 'ROLES:' || json_object_agg(oid::text,rolname)::text FROM pg_roles WHERE rolname LIKE 'merlin_d6%';\n"
    checks=[]
    for case in m.CASES:
     vals={k:str(uuid.uuid4()) for k in ['a','b','n','other','extra','missing']}
     vals.update(name_a='rev_a_'+uuid.uuid4().hex[:8],name_b='rev_b_'+uuid.uuid4().hex[:8])
     fixture=re.sub(r'^\s*BEGIN;','',setup,count=1)
     assert not re.search(r'\bCOMMIT\b|\bROLLBACK\b',case.sql,re.I)
     checks.append('SAVEPOINT case_check;\n'+fixture.format(**vals)+case.sql.format(**vals)+f"\nSELECT 'CASE:{case.id}';\nROLLBACK TO SAVEPOINT case_check; RELEASE SAVEPOINT case_check;\n")
    source_paths = [Path('migrations') / name for name in [
        '001_users_notes.up.sql', '001_users_notes.down.sql',
        '002_whitespace_parity.up.sql', '002_whitespace_parity.down.sql']]
    source_paths.extend([Path('tests/test_users_notes_database.py'),
                         Path('tools/audit_database_cases.py'),
                         Path('tools/audit_migration_undo.py')])
    def source_hashes():
        return {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
    expected_sources = source_hashes()
    expected_command = tuple(m.COMMAND)
    runtime = """SELECT 'RUNTIME:' || jsonb_build_object(
        'server_version',current_setting('server_version_num'),
        'database',current_database(),'session_user',session_user,'current_user',current_user,
        'database_locale',(SELECT jsonb_build_object('encoding',encoding,'collate',datcollate,'ctype',datctype,'collation_version',datcollversion) FROM pg_database WHERE datname=current_database()),
        'settings',(SELECT jsonb_object_agg(name,setting) FROM pg_settings WHERE name IN ('TimeZone','DateStyle','IntervalStyle','standard_conforming_strings','search_path','row_security','default_table_access_method','default_toast_compression','lc_time','lc_numeric','lc_monetary')),
        'extensions',(SELECT jsonb_agg(jsonb_build_object('name',extname,'version',extversion) ORDER BY extname) FROM pg_extension),
        'pinned_unicode_probe',public.note_weighted_length('é😀')=5,
        'empty',(SELECT count(*)=0 FROM public.users) AND (SELECT count(*)=0 FROM public.notes)
    )::text;
"""
    reference_schema = reference_runtime = None
    reference_schema_digest = reference_runtime_digest = None
    rows=[]
    for value in [False,True]:
     assert source_hashes() == expected_sources, 'Migration or case source changed between branches'
     assert tuple(m.COMMAND) == expected_command, 'Roundtrip runtime target changed between branches' 
     base=f"CREATE TEMP TABLE merlin_001_undo_baseline(public_create_before boolean,baseline_source text); INSERT INTO merlin_001_undo_baseline VALUES({str(value).lower()},'synthetic rollback-only review; historical baseline unknown');\n"
     post="""DO $check$ BEGIN
     IF NOT EXISTS(SELECT 1 FROM pg_extension WHERE extname='plpython3u') OR
        to_regnamespace('public') IS NULL OR NOT EXISTS(SELECT 1 FROM pg_roles WHERE rolname='merlin_d6' AND rolcanlogin)
     THEN RAISE EXCEPTION 'Prerequisite/schema/login removed'; END IF;
     IF (EXISTS(SELECT 1 FROM pg_namespace n, LATERAL aclexplode(n.nspacl) a WHERE n.nspname='public' AND a.grantee=0 AND a.privilege_type='CREATE'))
     IS DISTINCT FROM (SELECT public_create_before FROM pg_temp.merlin_001_undo_baseline)
     THEN RAISE EXCEPTION 'Wrong PUBLIC CREATE restoration'; END IF;
     IF to_regclass('public.review_sentinel') IS NULL THEN RAISE EXCEPTION 'Unrelated object removed'; END IF;
     END $check$;
    """
     script='\\set AUTOCOMMIT off\nBEGIN;\n'+roles+fingerprint+runtime+"CREATE TABLE public.review_sentinel(id integer);\n"+body('migrations/002_whitespace_parity.down.sql')+base+down+post+"SELECT 'DOWN_COMPLETE';\n"+Path('migrations/001_users_notes.up.sql').read_text()+body('migrations/002_whitespace_parity.up.sql')+roles+fingerprint+runtime+(''.join(checks) if not value else '')+"DROP TABLE public.review_sentinel;\nROLLBACK;\nSELECT 'ROUNDTRIP_COMPLETE';\nROLLBACK;\n"
     r=native_run(m.COMMAND,input=script,text=True,capture_output=True,timeout=45)
     row={'baseline_public_create':value,'exit':r.returncode,'stderr':r.stderr,'case_count':len([x for x in r.stdout.splitlines() if x.startswith('CASE:')]),'down_completed':'DOWN_COMPLETE' in r.stdout,'roundtrip_completed':'ROUNDTRIP_COMPLETE' in r.stdout}
     schemas=[json.loads(x[7:]) for x in r.stdout.splitlines() if x.startswith('SCHEMA:')]
     mappings=[json.loads(x[6:]) for x in r.stdout.splitlines() if x.startswith('ROLES:')]
     runtimes=[json.loads(x[8:]) for x in r.stdout.splitlines() if x.startswith('RUNTIME:')]
     def norm(x,mapping):
      if isinstance(x,list):return [norm(v,mapping) for v in x]
      if isinstance(x,dict):return {k:norm(v,mapping) for k,v in x.items()}
      if isinstance(x,int) and not isinstance(x,bool) and str(x) in mapping:return mapping[str(x)]
      if isinstance(x,str):
       x=re.sub(r'RI_ConstraintTrigger_([ac])_\d+',r'RI_ConstraintTrigger_\1_GENERATED',x)
       for oid,name in mapping.items():x=re.sub(r'(?<![0-9])'+oid+r'(?![0-9])',name,x)
      return x
     def canonical_schema(schema,mapping):
      # Only the outer inventory is unordered. Preserve every nested array order.
      return sorted(norm(schema,mapping),key=lambda item:json.dumps(item,sort_keys=True))
     row['semantic_schema_match']=len(schemas)==2 and len(mappings)==2 and canonical_schema(schemas[0],mappings[0])==canonical_schema(schemas[1],mappings[1])
     row['preserved']=audit.preservation(m)==original
     assert source_hashes() == expected_sources, 'Roundtrip sources changed during execution'
     assert len(schemas)==2 and len(mappings)==2 and len(runtimes)==2, 'Missing schema or runtime equivalence evidence'
     rebuilt = canonical_schema(schemas[1],mappings[1])
     same_runtime = runtimes[0]==runtimes[1] and runtimes[1]['empty'] and runtimes[1]['pinned_unicode_probe']
     schema_digest = hashlib.sha256(json.dumps(rebuilt,sort_keys=True).encode()).hexdigest()
     runtime_digest = hashlib.sha256(json.dumps(runtimes[1],sort_keys=True).encode()).hexdigest()
     if not value:
      assert row['exit']==0 and row['case_count']==len(m.CASES) and row['semantic_schema_match'] and row['preserved'] and same_runtime
      reference_schema, reference_runtime = rebuilt, runtimes[1]
      reference_schema_digest, reference_runtime_digest = schema_digest, runtime_digest
     row['replay_mode']='executed' if not value else 'equivalent_rebuild'
     row['equivalence_witness']={
         'validated':row['semantic_schema_match'] and same_runtime and rebuilt==reference_schema and runtimes[1]==reference_runtime,
         'reference_baseline_public_create':False,'reference_case_count':len(m.CASES),
         'same_rebuilt_schema':rebuilt==reference_schema,'same_runtime':same_runtime and runtimes[1]==reference_runtime,
         'source_sha256':expected_sources,'same_source_sha256':source_hashes()==expected_sources,
         'runtime_target_sha256':hashlib.sha256(json.dumps(expected_command).encode()).hexdigest(),
         'schema_sha256':schema_digest,'reference_schema_sha256':reference_schema_digest,
         'runtime_sha256':runtime_digest,'reference_runtime_sha256':reference_runtime_digest}
     assert row['equivalence_witness']['validated'], 'Rebuilt branch differs; full replay cannot be reused'
     rows.append(row)
     print(json.dumps({k:v for k,v in row.items() if k!='stderr'}),flush=True)
     if r.returncode:print(r.stderr,flush=True)
     if not row['semantic_schema_match'] and len(schemas)==2:
      Path('/tmp/merlin-review-before.json').write_text(json.dumps(norm(schemas[0],mappings[0]),indent=2,sort_keys=True))
      Path('/tmp/merlin-review-after.json').write_text(json.dumps(norm(schemas[1],mappings[1]),indent=2,sort_keys=True))

    assert all(x['exit']==0 and x['down_completed'] and x['roundtrip_completed'] and x['case_count']==(0 if x['baseline_public_create'] else len(m.CASES)) and x['semantic_schema_match'] and x['preserved'] and x['equivalence_witness']['validated'] for x in rows)

    return rows


def gate_checks():
    import json,re,subprocess
    from pathlib import Path
    from tools import audit_database_cases as audit
    module,_=audit.load_cases()
    original=audit.preservation(module)
    source=Path('migrations/001_users_notes.down.sql').read_text()
    down2=Path('migrations/002_whitespace_parity.down.sql').read_text()
    assert len(re.findall(r'^BEGIN;|^COMMIT;',down2,re.M))==2
    down2=re.sub(r'^BEGIN;\n','',down2,count=1,flags=re.M)
    down2=re.sub(r'^COMMIT;\s*\Z','',down2,count=1,flags=re.M)
    base="CREATE TEMP TABLE merlin_001_undo_baseline(public_create_before boolean,baseline_source text); INSERT INTO merlin_001_undo_baseline VALUES(false,'synthetic rollback-only gate test; not original baseline');\n"
    rows=[]
    cases=[
     ('autocommit-refused','',source,'AUTOCOMMIT must be off',True),
     ('migration002-present','',source,'undo migration 002 first',False),
     ('missing-baseline',down2,source,'recorded pre-001 permission baseline required',False),
     ('valid-gate',down2+base,source,None,False),
     ('wrong-cluster',down2+base,source.replace('7694311451826794534','0'),'unexpected database or cluster',False),
     ('nonempty-target',down2+base+"INSERT INTO public.users(username) VALUES('gate_test');\n",source,'users and notes must be empty',False),
     ('missing-view',down2+base+'DROP VIEW public.active_notes;\n',source,'migration 001 objects missing',False),
     ('missing-function',down2+base+'DROP FUNCTION public.cleanup_expired_blank_notes(integer);\n',source,'migration 001 function missing',False),
     ('role-changed',down2+base+'ALTER ROLE merlin_d6_app LOGIN;\n',source,'permission groups missing or changed',False),
     ('membership-changed',down2+base+'GRANT merlin_d6_owner TO merlin_d6_app;\n',source,'unexpected permission-group membership',False),
     ('empty-baseline',down2+'CREATE TEMP TABLE merlin_001_undo_baseline(public_create_before boolean,baseline_source text);\n',source,'permission baseline must contain one row',False),
     ('duplicate-baseline',down2+base+"INSERT INTO merlin_001_undo_baseline VALUES(false,'duplicate');\n",source,'permission baseline must contain one row',False),
     ('blank-baseline-source',down2+base+"UPDATE merlin_001_undo_baseline SET baseline_source='';\n",source,'permission baseline is incomplete',False),
     ('null-baseline-value',down2+base+'UPDATE merlin_001_undo_baseline SET public_create_before=NULL;\n',source,'permission baseline is incomplete',False),
    ]
    for name,setup,candidate,error,autocommit in cases:
        script=('\\set AUTOCOMMIT on\n' if autocommit else '\\set AUTOCOMMIT off\nBEGIN;\n')+setup+candidate+"\nSELECT 'GATE_COMPLETE';\nROLLBACK;\n"
        result=native_run(module.COMMAND,input=script,text=True,capture_output=True,timeout=30)
        ok=(result.returncode==0 and 'GATE_COMPLETE' in result.stdout if error is None else result.returncode!=0 and error in result.stderr and 'GATE_COMPLETE' not in result.stdout)
        rows.append({'case':name,'passed':ok,'exit':result.returncode,'stderr':result.stderr.strip()})
        print(name,'PASS' if ok else 'FAIL',flush=True)
        if not ok: print(result.stdout,result.stderr)
        assert audit.preservation(module)==original,'Installed state not restored'

    assert all(row['passed'] for row in rows)
    print('ALL GATE CHECKS PASS; original fingerprint and empty target preserved')

    return rows


def concurrency_checks():
    import re,subprocess,selectors
    from pathlib import Path
    from tools import audit_database_cases as audit
    m,_=audit.load_cases();original=audit.preservation(m)
    s=Path('migrations/001_users_notes.down.sql').read_text()
    d=Path('migrations/002_whitespace_parity.down.sql').read_text()
    assert len(re.findall(r'^BEGIN;|^COMMIT;',d,re.M))==2
    d=re.sub(r'^BEGIN;\n','',d,count=1,flags=re.M);d=re.sub(r'^COMMIT;\s*\Z','',d,count=1,flags=re.M)
    b="CREATE TEMP TABLE merlin_001_undo_baseline(public_create_before boolean,baseline_source text); INSERT INTO merlin_001_undo_baseline VALUES(false,'synthetic rollback-only test');\n"
    def start(text):
     p=subprocess.Popen(m.COMMAND,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
     try:
      p.stdin.write(text+"\nSELECT 'READY';\n");p.stdin.flush()
      with selectors.DefaultSelector() as selector:
       selector.register(p.stdout,selectors.EVENT_READ)
       if not selector.select(timeout=30):raise RuntimeError('Concurrent session readiness timed out')
       if p.stdout.readline().strip()!='READY':raise RuntimeError('Concurrent session failed before readiness')
      return p
     except BaseException:
      p.terminate()
      try:p.communicate(timeout=15)
      except subprocess.TimeoutExpired:p.kill();p.communicate()
      raise
    def close(p):
     try:
      p.stdin.write('ROLLBACK;\n');p.stdin.flush();p.communicate(timeout=15)
     except BaseException:
      p.terminate()
      try:p.communicate(timeout=15)
      except subprocess.TimeoutExpired:p.kill();p.communicate()
      raise
    other=start('BEGIN;')
    try:
     r=native_run(m.COMMAND,input='\\set AUTOCOMMIT off\nBEGIN;\n'+d+b+s+'\nROLLBACK;\n',text=True,capture_output=True,timeout=20)
     assert r.returncode!=0 and 'another database client is connected' in r.stderr,r.stderr
     print('other-client-refused PASS',flush=True)
    finally: close(other)
    assert audit.preservation(m)==original
    holder=start('\\set AUTOCOMMIT off\nBEGIN;\n'+d+b+s)
    try:
     r=native_run(m.COMMAND,input="\\set VERBOSITY verbose\nBEGIN;SET LOCAL lock_timeout='200ms';INSERT INTO public.users(username) VALUES('concurrent_gate');ROLLBACK;\n",text=True,capture_output=True,timeout=15)
     assert r.returncode!=0 and '55P03' in r.stderr,r.stderr
     print('table-lock-blocks-concurrent-insert PASS',flush=True)
    finally: close(holder)
    assert audit.preservation(m)==original
    command=m.COMMAND.copy();command[command.index('-d')+1]='postgres'
    r=native_run(command,input='\\set AUTOCOMMIT off\n'+s+'\nROLLBACK;\n',text=True,capture_output=True,timeout=20)
    assert r.returncode!=0 and 'unexpected database or cluster' in r.stderr,r.stderr
    print('wrong-database-refused PASS',flush=True)
    assert audit.preservation(m)==original
    print('PRESERVED: original fingerprint, identity, empty tables')

    return {'checks': ['other-client-refused', 'table-lock-blocks-concurrent-insert', 'wrong-database-refused'], 'preserved': True}


def repair_checks():
    import json,re,subprocess
    from pathlib import Path
    from tools import audit_database_cases as audit
    m,_=audit.load_cases();original=audit.preservation(m)
    s=Path('migrations/001_users_notes.down.sql').read_text();d=Path('migrations/002_whitespace_parity.down.sql').read_text()
    assert len(re.findall(r'^BEGIN;|^COMMIT;',d,re.M))==2
    d=re.sub(r'^BEGIN;\n','',d,count=1,flags=re.M);d=re.sub(r'^COMMIT;\s*\Z','',d,count=1,flags=re.M)
    b="CREATE TEMP TABLE merlin_001_undo_baseline(public_create_before boolean,baseline_source text);INSERT INTO merlin_001_undo_baseline VALUES(false,'synthetic rollback-only repair test');\n"
    changes=[
     ('extra-index','CREATE INDEX review_unexpected_idx ON public.notes(body);'),
     ('extra-trigger','CREATE TRIGGER review_extra BEFORE UPDATE ON public.notes FOR EACH ROW EXECUTE FUNCTION public.manage_note_content();'),
     ('extra-constraint','ALTER TABLE public.notes ADD CONSTRAINT review_extra CHECK(length(body)>=0);'),
     ('extra-policy','CREATE POLICY review_extra ON public.notes FOR SELECT TO merlin_d6_app USING(true);'),
     ('extra-column','ALTER TABLE public.notes ADD COLUMN review_extra text;'),
     ('extra-rule','CREATE RULE review_extra AS ON INSERT TO public.users DO INSTEAD NOTHING;'),
     ('missing-index','DROP INDEX public.users_username_canonical_idx;'),
     ('missing-trigger','DROP TRIGGER notes_content ON public.notes;'),
     ('missing-constraint','ALTER TABLE public.notes DROP CONSTRAINT notes_title_limit;'),
     ('missing-policy','DROP POLICY notes_own_account ON public.notes;'),
     ('missing-column','DROP VIEW public.active_notes; ALTER TABLE public.notes DROP COLUMN device_created_at; CREATE VIEW public.active_notes WITH (security_invoker=true) AS SELECT * FROM public.notes; ALTER VIEW public.active_notes OWNER TO merlin_d6_owner;'),
    ]
    rows=[]
    def execute(name,setup,candidate,expected):
     r=native_run(m.COMMAND,input='\\set AUTOCOMMIT off\nBEGIN;\n'+d+b+setup+'\n'+candidate+"\nSELECT 'DOWN_FINISHED';ROLLBACK;\n",text=True,capture_output=True,timeout=20)
     ok=r.returncode!=0 and expected in r.stderr and 'DOWN_FINISHED' not in r.stdout
     preserved=audit.preservation(m)==original
     row={'case':name,'passed':ok,'exit':r.returncode,'stderr':r.stderr.strip(),'preserved':preserved};rows.append(row)
     print(name,'PASS' if ok and preserved else 'FAIL',flush=True)
     assert preserved
    for name,change in changes:execute(name,change,s,'unexpected or missing table-owned artifact')
    anchor='DO $undo_postchecks$'
    for name,change,error in [
     ('wrong-public-create','GRANT CREATE ON SCHEMA public TO PUBLIC;','PUBLIC CREATE does not match baseline'),
     ('lost-public-usage','REVOKE USAGE ON SCHEMA public FROM PUBLIC;','unrelated schema grants changed'),
     ('changed-schema-owner','ALTER SCHEMA public OWNER TO merlin_d6;','public schema changed'),
     ('lost-extension','DROP EXTENSION plpython3u;','PL/Python prerequisite changed'),
     ('changed-login','ALTER ROLE merlin_d6 NOLOGIN;','connection login changed'),
    ]:execute(name,'',s.replace(anchor,change+'\n'+anchor,1),error)
    # The original bad expectation must still fail if the new inventory gate is disabled.
    fault=s.replace('IF EXISTS (\n        WITH expected','IF FALSE AND EXISTS (\n        WITH expected',1)
    r=native_run(m.COMMAND,input='\\set AUTOCOMMIT off\nBEGIN;\n'+d+b+changes[0][1]+'\n'+fault+"\nSELECT 'DOWN_FINISHED';ROLLBACK;\n",text=True,capture_output=True,timeout=20)
    assert r.returncode==0 and 'DOWN_FINISHED' in r.stdout, r.stderr
    assert audit.preservation(m)==original
    rows.append({'case':'inventory-guard-removal-detected','passed':True,'explanation':'Disabled gate admits extra index, violating refusal assertion; no live fault retained','preserved':True})
    print('inventory-guard-removal-detected PASS',flush=True)

    assert all(row['passed'] for row in rows)

    return rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error("Run without -O: migration verification requires enabled assertions")
    os.chdir(ROOT)
    import re
    for filename in ["001_users_notes.up.sql", "001_users_notes.down.sql"]:
        source = (ROOT / "migrations" / filename).read_text()
        if re.search(r"^\s*(COMMIT|ROLLBACK)\s*;", source, re.M | re.I):
            raise RuntimeError("Unexpected transaction boundary in " + filename)
    from tools import audit_database_cases as audit
    module, _ = audit.load_cases()
    original = audit.preservation(module)
    result = {"source_sha256": hashlib.sha256((ROOT / "migrations/001_users_notes.down.sql").read_bytes()).hexdigest(), "phases": {}, "original_fingerprint": original}
    try:
        for name, check in [("roundtrips", roundtrips), ("gates", gate_checks),
                            ("concurrency", concurrency_checks), ("repairs", repair_checks)]:
            print("MIGRATION PHASE: " + name, flush=True)
            result["phases"][name] = check()
        result["status"] = "PASS"
    except Exception:
        result["status"] = "FAIL"
        raise
    finally:
        try:
            result["final_fingerprint"] = audit.preservation(module)
            result["preserved"] = original == result["final_fingerprint"]
        except Exception:
            result["preserved"] = False
            result["status"] = "FAIL"
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2) + "\n")
        if not result["preserved"]:
            raise RuntimeError("Migration audit preservation failed; stop and investigate")

if __name__ == "__main__":
    main()
