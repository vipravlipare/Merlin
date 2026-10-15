"""Commit migration undo/reapplication only in a guarded disposable copy.

Capture an actual fresh pre-001 baseline; never infer the source's lost history.
Original migration files and the source database remain unchanged.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools import audit_database_cases as audit
from tools.database_sandboxes import DatabaseSandboxes
from tools.database_test_session import database_target


def normalize(value,roles):
    if isinstance(value,list):return [normalize(item,roles) for item in value]
    if isinstance(value,dict):return {key:normalize(item,roles) for key,item in value.items()}
    if isinstance(value,int) and not isinstance(value,bool) and str(value) in roles:return roles[str(value)]
    if isinstance(value,str):
        value=re.sub(r'RI_ConstraintTrigger_([ac])_\d+',r'RI_ConstraintTrigger_\1_GENERATED',value)
        for oid,name in roles.items():value=re.sub(r'(?<![0-9])'+oid+r'(?![0-9])',name,value)
    return value


def canonical_schema(schema, roles):
    """Ignore inventory row order while retaining ordered schema arrays."""
    return sorted(normalize(schema, roles), key=lambda item: json.dumps(item, sort_keys=True))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if sys.flags.optimize:parser.error('Verification requires enabled assertions')
    os.chdir(ROOT)
    if os.environ.get('MERLIN_DB_SANDBOX'):raise RuntimeError('Nested disposable verification is forbidden')
    descriptor=os.open('/tmp/merlin-d6-test-suite.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    started=time.monotonic()
    result={'status':'FAIL','checks':[],'scope':'Fresh disposable database only; committed down/up with authentic captured pre-001 baseline'}
    with os.fdopen(descriptor,'w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        module,setup=audit.load_cases()
        original=audit.preservation(module)
        result['source_fingerprint']=original
        files={name:(ROOT/'migrations'/name).read_text() for name in ['001_users_notes.up.sql','001_users_notes.down.sql','002_whitespace_parity.up.sql','002_whitespace_parity.down.sql']}
        result['migration_sha256']={name:hashlib.sha256(source.encode()).hexdigest() for name,source in files.items()}
        args.out.parent.mkdir(parents=True,exist_ok=True)
        copies=DatabaseSandboxes(args.out.parent/('migration-roundtrip-targets-'+uuid.uuid4().hex))
        try:
            with copies:
                os.environ['MERLIN_DB_SANDBOX']=copies.manifests['migration']
                database_target.cache_clear()
                target=database_target()
                assert target['container']!=target['source'] and target['name']=='migration'
                result['target']=target
                def query(sql,database='merlin_d6'):
                    command=['docker','exec','-i',target['container'],'psql','-X','-qAt','-h',target['socket'],'-U','merlin_d6','-d',database,'-v','ON_ERROR_STOP=1']
                    answer=subprocess.run(command,input=sql,capture_output=True,text=True,timeout=45)
                    if answer.returncode:raise RuntimeError(answer.stderr[-2500:])
                    return answer.stdout.strip()
                def passed(name):
                    result['checks'].append({'case':name,'passed':True})
                    print(name+' PASS',flush=True)
                # This command can only address the already-verified private copy.
                # Ordinary DROP refuses active clients; no FORCE or CASCADE used.
                query('DROP DATABASE merlin_d6;','postgres')
                query('DROP ROLE merlin_d6_app,merlin_d6_maintenance,merlin_d6_owner;','postgres')
                query('CREATE DATABASE merlin_d6 OWNER merlin_d6 TEMPLATE template0;','postgres')
                query('CREATE EXTENSION plpython3u; CREATE TABLE public.roundtrip_sentinel(id integer PRIMARY KEY); INSERT INTO public.roundtrip_sentinel VALUES(73);')
                passed('fresh-database-and-external-prerequisite')
                def snapshot():
                    roles=json.loads(query("SELECT json_object_agg(oid::text,rolname)::text FROM pg_roles WHERE rolname LIKE 'merlin_d6%';"))
                    sql=audit.FINGERPRINT.replace('SELECT md5(jsonb_agg(row_data ORDER BY row_data::text)::text)','SELECT jsonb_agg(row_data ORDER BY row_data::text)::text')
                    # Baseline/undone states intentionally lack app relations
                    # and roles. Resolve absent names to NULL rather than error.
                    sql=re.sub(r"'([^']+)'::regclass",r"to_regclass('\1')",sql)
                    sql=re.sub(r"'([^']+)'::regrole",r"to_regrole('\1')",sql)
                    prerequisites=json.loads(query("SELECT jsonb_agg(jsonb_build_object('name',extname,'version',extversion,'owner',extowner) ORDER BY extname)::text FROM pg_extension;"))
                    return {'schema':canonical_schema(json.loads(query(sql)),roles),'extensions':prerequisites}
                baseline=snapshot()
                public_create=query("SELECT EXISTS(SELECT 1 FROM pg_namespace n,LATERAL aclexplode(n.nspacl) a WHERE n.nspname='public' AND a.grantee=0 AND a.privilege_type='CREATE');")
                assert public_create in {'t','f'}
                result['captured_pre_001_baseline']={'public_create':public_create=='t','source':'Actual query of fresh template0 database before first migration 001 application in this private container','schema_snapshot':baseline}
                query('BEGIN;\n'+files['001_users_notes.up.sql']+'\nCOMMIT;')
                query(files['002_whitespace_parity.up.sql'])
                installed=snapshot()
                passed('initial-up-001-and-002-committed')
                query(files['002_whitespace_parity.down.sql'])
                passed('down-002-committed')
                recorded="CREATE TEMP TABLE merlin_001_undo_baseline(public_create_before boolean,baseline_source text);INSERT INTO merlin_001_undo_baseline VALUES("+str(public_create=='t').lower()+",'actual fresh baseline recorded before first up; see roundtrip report');\n"
                query('\\set AUTOCOMMIT off\nBEGIN;\n'+recorded+files['001_users_notes.down.sql']+'\nCOMMIT;')
                assert snapshot()==baseline,'Committed undo failed to restore actual pre-001 state'
                assert query("SELECT count(*) FROM pg_roles WHERE rolname IN ('merlin_d6_app','merlin_d6_maintenance','merlin_d6_owner');")=='0'
                assert query("SELECT to_regclass('public.users') IS NULL AND to_regclass('public.notes') IS NULL AND to_regclass('public.active_notes') IS NULL;")=='t'
                assert query('SELECT id FROM public.roundtrip_sentinel;')=='73'
                passed('down-001-committed-and-verified-after-reconnect')
                query('BEGIN;\n'+files['001_users_notes.up.sql']+'\nCOMMIT;')
                query(files['002_whitespace_parity.up.sql'])
                assert snapshot()==installed,'Reapplied schema/permissions differ from initial installation'
                passed('up-001-and-002-committed-semantic-equivalence')
                checks=[]
                for case in module.CASES:
                    values={key:str(uuid.uuid4()) for key in ['a','b','n','other','extra','missing']}
                    values.update(name_a='audit_a_'+uuid.uuid4().hex[:8],name_b='audit_b_'+uuid.uuid4().hex[:8])
                    fixture=re.sub(r'^\s*BEGIN;','',setup,count=1)
                    assert not re.search(r'\bCOMMIT\b|\bROLLBACK\b',case.sql,re.I)
                    checks.append('SAVEPOINT case_check;\n'+fixture.format(**values)+case.sql.format(**values)+"\nSELECT 'CASE:"+case.id+"';\nROLLBACK TO SAVEPOINT case_check; RELEASE SAVEPOINT case_check;\n")
                output=query('BEGIN;\n'+''.join(checks)+'\nROLLBACK;')
                observed=[line[5:] for line in output.splitlines() if line.startswith('CASE:')]
                assert observed==[case.id for case in module.CASES]
                result['rebuilt_cases']=observed
                passed('all-rebuilt-database-cases-'+str(len(observed)))
                source_command=module.COMMAND
                module.COMMAND=['docker','exec','-i',target['container'],'psql','-X','-qAt','-h',target['socket'],'-U','merlin_d6','-d','merlin_d6','-v','ON_ERROR_STOP=1']
                try:
                    module.test_failed_second_write_rolls_back_first_write_after_reconnect()
                finally:
                    module.COMMAND=source_command
                result['rebuilt_case_count']=len(observed)+1
                passed('rebuilt-failed-write-and-real-reconnect')
                assert snapshot()==installed
                assert query('SELECT (SELECT count(*) FROM public.users),(SELECT count(*) FROM public.notes);')=='0|0'
                assert query('SELECT id FROM public.roundtrip_sentinel;')=='73'
                passed('reconnected-empty-tables-and-unrelated-data-preserved')
            os.environ.pop('MERLIN_DB_SANDBOX',None);database_target.cache_clear()
            result['source_preserved']=audit.preservation(module)==original
            assert result['source_preserved'] and copies.evidence['cleanup_passed']
            result['status']='PASS'
            passed('source-preservation-and-disposable-cleanup')
        except BaseException as error:
            result['failure']=str(error)
            raise
        finally:
            os.environ.pop('MERLIN_DB_SANDBOX',None);database_target.cache_clear()
            result['disposable_evidence']=copies.evidence
            result['seconds']=round(time.monotonic()-started,3)
            args.out.parent.mkdir(parents=True,exist_ok=True)
            args.out.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
