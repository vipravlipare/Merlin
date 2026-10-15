"""Exercise real suite scheduling against disposable, deliberately faulty jobs.

No database or browser access. Proves baseline-first scheduling, independent
target assignment, serial fallback, validation failure and cancellation cleanup.
These infrastructure checks are separate from application case counts.
"""
import argparse
import json
import hashlib
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
STUB = r'''
import json,os,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from tools import run_test_suite as suite
folder=Path(sys.argv[2]);mode=sys.argv[3]
original_open=os.open
def test_open(path,*args,**kwargs):
 if path=='/tmp/merlin-d6-test-suite.lock':path=folder/'test.lock'
 return original_open(path,*args,**kwargs)
os.open=test_open
def preflight(env):
 if mode=='prerequisite-failure':raise RuntimeError('Injected prerequisite failure')
suite.preflight=preflight
suite.isolation_controls=lambda directory,env:None
class Copies:
 def __init__(self,directory):
  self.manifests={name:name for name in ['sql','lifecycle','migration']};self.evidence={}
 def __enter__(self):
  (folder/'copies-start').write_text(str(time.monotonic()))
  time.sleep(1 if mode=='interrupt-setup' else .15)
  if mode=='setup-failure':raise RuntimeError('Injected isolation startup failure')
  (folder/'copies-ready').write_text(str(time.monotonic()))
  return self
 def __exit__(self,*unused):
  (folder/'copies-cleaned').write_text('yes');self.evidence['cleanup_passed']=True
suite.DatabaseSandboxes=Copies
if mode=='serial':os.environ['MERLIN_DB_ISOLATION']='0'
else:os.environ['MERLIN_DB_ISOLATION']='1'
names=[name for name,command in suite.stages(folder)]
def stages(directory):
 rows=[]
 for name in names:
  delay=1 if (mode=='interrupt' and name in ['quiz-case-faults','python-case-faults','migration-undo-faults','database-case-faults','database-lifecycle-faults']) or mode=='interrupt-setup' else .1
  code="import json,os,time;from pathlib import Path;p=Path("+repr(str(folder/'trace'))+");name="+repr(name)+";\ndef event(action):\n with p.open('a') as f:f.write(json.dumps({'stage':name,'action':action,'pid':os.getpid(),'time':time.monotonic(),'target':os.environ.get('MERLIN_DB_SANDBOX')})+'\\n')\nevent('start')\ntry:time.sleep("+repr(delay)+")\nfinally:event('end')"
  rows.append((name,[sys.executable,'-c',code]))
 return rows
suite.stages=stages
def validate(name,directory):
 if mode=='baseline-failure' and name=='python-tests':raise RuntimeError('Injected baseline failure')
 if mode=='failure' and name=='quiz-case-faults':raise RuntimeError('Injected zero-exit report failure')
 return {}
suite.validate=validate
sys.argv=['run_test_suite.py','--out-dir',str(folder/'results')]
raise SystemExit(suite.main())
'''


def check(mode, root):
    folder = root / mode; folder.mkdir()
    process = subprocess.Popen([sys.executable, '-c', STUB, str(ROOT), str(folder), mode],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    def trace():
        path = folder / 'trace'
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    try:
        if mode=='interrupt-setup':
            deadline=time.monotonic()+5
            while not (folder/'copies-start').exists() or not any(row['stage']=='python-tests' and row['action']=='start' for row in trace()):
                if time.monotonic()>deadline:raise RuntimeError('Preparation/baseline overlap did not start')
                time.sleep(.005)
            process.send_signal(signal.SIGINT)
        if mode == 'interrupt':
            deadline = time.monotonic() + 5
            while not {'quiz-case-faults','python-case-faults','migration-undo-faults','database-case-faults','database-lifecycle-faults'} <= {
                    row['stage'] for row in trace() if row['action']=='start'}:
                if time.monotonic() > deadline:raise RuntimeError('Coordinator did not start both independent lanes')
                time.sleep(.005)
            process.send_signal(signal.SIGINT)
        code = process.wait(timeout=15)
    finally:
        if process.poll() is None:
            process.kill(); process.wait()
    result = json.loads((folder / 'results/summary.json').read_text())
    events = trace(); stages = {row['stage']:row for row in result['stages']}
    intervals = {}
    for row in events:
        intervals.setdefault(row['stage'],{})[row['action']] = row['time']
    assert code == (0 if mode in {'pass','serial'} else 1), (mode,code,result)
    if mode in {'pass','serial'}:
        assert result['status']=='PASS' and len(stages)==10 and all(row['status']=='PASS' for row in stages.values())
        baseline_end=max(intervals[name]['end'] for name in ['python-tests','quiz-tests'])
        assert all(value['start']>=baseline_end for name,value in intervals.items() if name not in ['python-tests','quiz-tests'])
        if mode=='serial':
            database=['migration-undo-faults','database-lifecycle-faults','database-case-faults']
            assert all(intervals[a]['end']<=intervals[b]['start'] for a,b in zip(database,database[1:]))
            assert all(row['target'] is None for row in events)
        else:
            database=['database-case-faults','database-lifecycle-faults','migration-undo-faults']
            assert max(intervals[n]['start'] for n in database)<min(intervals[n]['end'] for n in database)
            targets={row['stage']:row['target'] for row in events}
            assert [targets[n] for n in database]==['sql','lifecycle','migration']
            assert (folder/'copies-cleaned').exists()
            assert float((folder/'copies-start').read_text()) < intervals['python-tests']['end']
            assert float((folder/'copies-ready').read_text()) <= min(intervals[n]['start'] for n in database)
        cpu=intervals['quiz-case-faults']; db=intervals['migration-undo-faults']
        assert max(cpu['start'],db['start'])<min(cpu['end'],db['end']), 'Independent work did not overlap'
        python=intervals['python-case-faults']
        assert max(cpu['start'],python['start'])<min(cpu['end'],python['end']), 'Independent Python audits did not overlap'
        assert intervals['quiz-case-faults']['end']<=intervals['browser-case-faults']['start']
    elif mode=='failure':
        assert result['status']=='FAIL' and result['first_failed_stage']=='quiz-case-faults'
        assert stages['quiz-case-faults']['exit']==0 and stages['quiz-case-faults']['status']=='FAIL'
        assert stages['browser-case-faults']['status']=='PENDING'
        assert stages['documentation']['status']=='PENDING'
    elif mode=='setup-failure':
        assert result['status']=='FAIL' and result['first_failed_stage']=='database-isolation'
        assert all(stages[n]['status']=='PENDING' for n in ['database-case-faults','database-lifecycle-faults','migration-undo-faults'])
        assert stages['documentation']['status']=='PENDING'
    elif mode=='prerequisite-failure':
        assert result['status']=='FAIL' and result['first_failed_stage']=='preflight'
        assert 'Injected prerequisite failure' in result['failure']
        assert all(row['status']=='PENDING' for row in stages.values()) and not events
        assert (folder/'copies-ready').exists() and (folder/'copies-cleaned').exists()
    elif mode in {'baseline-failure','interrupt-setup'}:
        assert result['status']=='FAIL' and stages['python-tests']['status']=='FAIL'
        assert all(row['status']=='PENDING' for name,row in stages.items() if name!='python-tests')
        assert (folder/'copies-ready').exists() and (folder/'copies-cleaned').exists(), 'Startup must join before cleanup'
        assert not any(row['action']=='start' and row['stage']!='python-tests' for row in events)
    else:
        assert result['status']=='FAIL' and stages['documentation']['status']=='PENDING'
        assert {'quiz-case-faults','python-case-faults','migration-undo-faults','database-case-faults','database-lifecycle-faults'} <= {
            row['stage'] for row in events if row['action']=='end'}, 'Running jobs did not execute cleanup'
        for row in events:
            try:os.kill(row['pid'],0)
            except ProcessLookupError:continue
            raise AssertionError('Job process survived runner cancellation')
        assert (folder/'copies-cleaned').exists()
    return {'scenario':mode,'passed':True,'runner_exit':code}


def check_preflight():
    sys.path.insert(0,str(ROOT))
    from tools import run_test_suite as suite
    rows=[]
    for mode in ['pass','failure','timeout','ci-guards-failure','ci-guards-timeout']:
        events=[]
        guard=threading.Lock()
        def probe(command, **kwargs):
            assert kwargs['timeout']==45 and kwargs['capture_output'] and kwargs['text']
            if command[1:2]==['tools/verify_suite_execution.py']:name='scheduling'
            elif command[1:2]==['tools/verify_native_psql.py']:name='native'
            elif command[1:2]==['tools/verify_python_isolation.py']:name='python-isolation'
            elif command[1:2]==['tools/run_ci.py']:name='ci-guards'
            elif command[0]=='node':name='browser' if '--input-type=module' in command else 'node'
            elif 'import sys,pytest' in command[-1]:name='imports'
            elif 'DatabaseTestSession' in command[-1]:name='transport'
            else:name='preservation'
            start=time.monotonic()
            time.sleep(.03)
            with guard:events.append({'name':name,'start':start,'end':time.monotonic()})
            selected = 'ci-guards' if mode.startswith('ci-guards-') else 'native'
            if name==selected and mode.endswith('timeout'):raise subprocess.TimeoutExpired(command,45)
            return subprocess.CompletedProcess(command,1 if name==selected and mode.endswith('failure') else 0,('Native psql failed checks: native_equivalence_1\nprivate-secret-output\n' if name==selected and mode.endswith('failure') else ''),'private-secret-error')
        with patch.object(suite.subprocess,'run',side_effect=probe):
            try:suite.preflight({})
            except (RuntimeError,subprocess.TimeoutExpired) as error:
                assert mode!='pass'
                assert 'private-secret-error' not in str(error) and 'private-secret-output' not in str(error)
                if mode == 'failure':
                    assert 'Native psql failed checks: native_equivalence_1' in str(error)
            else:assert mode=='pass','Failed prerequisite was accepted'
        if mode=='pass':
            by_name={event['name']:event for event in events}
            # CI ownership checks are now a mandatory ninth prerequisite.
            assert len(events)==9 and set(by_name)=={'scheduling','native','imports','node','transport','preservation','browser','python-isolation','ci-guards'}
            assert by_name['scheduling']['end']<=by_name['ci-guards']['start']
            assert by_name['native']['end']<=by_name['transport']['start']
            assert by_name['transport']['end']<=by_name['preservation']['start']
            assert max(by_name[name]['start'] for name in ['scheduling','native','imports'])<min(by_name[name]['end'] for name in ['scheduling','native','imports'])
        rows.append({'scenario':'preflight-'+mode,'passed':True})
    return rows


def check_result_validation():
    """Counterfactuals for the real result gates, independent of job exit codes."""
    sys.path.insert(0, str(ROOT))
    from tools import run_test_suite as suite
    inventory = json.loads((ROOT/'tests/suite-inventory.json').read_text())
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for folder in ['app','tests','tools'] for p in (ROOT/folder).glob('*.py')}
    python_cases = inventory['python_cases']
    valid_python_faults = [name for name in inventory['python_faults'] if name not in suite.KNOWN_INVALID_IMPORT_FAULTS and name not in inventory['python_aliases']]
    python_faults = [{'fault':name, 'status':'EXCLUDED_INVALID'} if name in suite.KNOWN_INVALID_IMPORT_FAULTS else
                    {'fault':name, 'status':'ALIAS','canonical_fault':inventory['python_aliases'][name]} if name in inventory['python_aliases'] else
                     {'fault':name,'status':'DETECTED','scope_manifest_matches':True,
                      'detected_by':python_cases if name==valid_python_faults[0] else python_cases[:1],
                      'cases':{case:{'outcome':'failed'} for case in (python_cases if name==valid_python_faults[0] else python_cases[:1])}}
                     for name in inventory['python_faults']]
    python_report = {'baseline':{'exit':0,'errors':[],'cases':{case:{'outcome':'passed'} for case in python_cases}},
                     'matrix':[{'case':case,'outcome':'passed','detects':[r['fault'] for r in python_faults if case in r.get('detected_by',[])]} for case in python_cases],
                     'faults':python_faults,'source_sha256':hashes}
    quiz_cases = inventory['quiz_cases']
    quiz_report = {'baseline':{'status':'SURVIVED','cases':dict.fromkeys(quiz_cases,'passed')},
                   'matrix':[{'case':case,'baseline':'passed','detects':inventory['quiz_faults']} for case in quiz_cases],
                   'faults':[{'fault':name,'status':'DETECTED','cases':dict.fromkeys(quiz_cases,'failed')} for name in inventory['quiz_faults']],
                   'source_sha256':{path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in ['quizzes/sprint-0-quiz.html','tests/quiz.test.js']}}
    browser_report = {'cases':[{'case':case,'baseline':{'outcome':'passed'},'mutation':{'status':'DETECTED','outcome':'failed'}} for case in inventory['browser_cases']],
                      'source_sha256':{path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in ['quizzes/sprint-0-quiz.html','tools/audit_quiz_browser.mjs']}}
    lifecycle_report = {'preserved':True,'cases':[{'case':case,'effectiveness':'DEMONSTRATED','baseline':{'outcome':'passed'},'mutation':{'outcome':'failed'}} for case in inventory['lifecycle_cases']]}
    from tools.audit_database_cases import load_cases, recipes
    module,unused = load_cases()
    sql_report = {'preserved':True,'original_fingerprint':'a'*32,'final_fingerprint':'a'*32,'source_sha256':hashlib.sha256((ROOT/'tests/test_users_notes_database.py').read_bytes()).hexdigest(),
                  'cases':[{'case':case.id,'effectiveness':'DEMONSTRATED','baseline':{'exit':0},
                            'faults':[{**fault,'status':'DETECTED_ASSERTION'} for fault in recipes(case)]} for case in module.CASES]}
    reconnect = [row for row in inventory['sql_pairs'] if row[0] not in {case.id for case in module.CASES}]
    assert len(reconnect)==1
    sql_report['cases'].append({'case':reconnect[0][0],'effectiveness':'DEMONSTRATED','baseline':{'exit':0},'faults':[{'name':reconnect[0][1],'status':'DETECTED_ASSERTION'}]})
    reports = {'python-case-faults':('merlin-python-effectiveness-final.json',python_report,'matrix'),
               'database-case-faults':('merlin-sql-effectiveness-final.json',sql_report,'cases'),
               'quiz-case-faults':('merlin-quiz-effectiveness.json',quiz_report,'matrix'),
               'browser-case-faults':('merlin-browser-effectiveness.json',browser_report,'cases'),
               'database-lifecycle-faults':('merlin-lifecycle-effectiveness.json',lifecycle_report,'cases')}
    rows=[]
    with tempfile.TemporaryDirectory(prefix='merlin-result-controls-') as directory:
        folder=Path(directory)
        target_root = '/tmp/merlin-db-sandboxes-' + '1'*32
        target = {'name':'migration','container':'2'*64,'source':'3'*64,
                  'root':target_root,'data':target_root+'/migration',
                  'socket':target_root+'/migration/socket','fingerprint':'4'*32}
        (folder/'database-targets').mkdir()
        (folder/'database-targets/migration.json').write_text(json.dumps(target))
        arguments = module.COMMAND[module.COMMAND.index('psql'):]
        target_command = ['docker','exec','-i',target['container'],'psql','-h',target['socket'],*arguments[1:]]
        source_paths = ['migrations/001_users_notes.up.sql','migrations/001_users_notes.down.sql',
                        'migrations/002_whitespace_parity.up.sql','migrations/002_whitespace_parity.down.sql',
                        'tests/test_users_notes_database.py','tools/audit_database_cases.py','tools/audit_migration_undo.py']
        witness = {'validated':True,'same_rebuilt_schema':True,'same_runtime':True,'same_source_sha256':True,
                   'reference_baseline_public_create':False,'reference_case_count':len(module.CASES),
                   'schema_sha256':'a'*64,'reference_schema_sha256':'a'*64,
                   'runtime_sha256':'c'*64,'reference_runtime_sha256':'c'*64,
                   'runtime_target_sha256':hashlib.sha256(json.dumps(target_command).encode()).hexdigest(),
                   'source_sha256':{path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in source_paths}}
        roundtrips = [{'baseline_public_create':branch,'exit':0,'down_completed':True,'roundtrip_completed':True,
                       'semantic_schema_match':True,'preserved':True,'case_count':0 if branch else len(module.CASES),
                       'replay_mode':'equivalent_rebuild' if branch else 'executed','equivalence_witness':witness}
                      for branch in [False,True]]
        migration_report = {'status':'PASS','preserved':True,'phases':{'roundtrips':roundtrips,
                            'gates':[{'case':name,'passed':True} for name in inventory['migration_gates']],
                            'repairs':[{'case':name,'passed':True,'preserved':True} for name in inventory['migration_repairs']],
                            'concurrency':{'preserved':True,'checks':['other-client-refused','table-lock-blocks-concurrent-insert','wrong-database-refused']}}}
        migration_path=folder/'migration-undo-results.json'
        migration_path.write_text(json.dumps(migration_report));suite.validate('migration-undo-faults',folder)
        rows.append({'scenario':'migration-undo-faults-complete-positive','passed':True})
        variants={}
        for dimension in ['schema','runtime']:
            faulty=json.loads(json.dumps(migration_report))
            altered=faulty['phases']['roundtrips'][1]['equivalence_witness']
            altered[dimension+'_sha256']=altered['reference_'+dimension+'_sha256']='b'*64
            variants['contradictory-'+dimension]=faulty
        for name,change in [
            ('wrong-target',lambda w:w.update(runtime_target_sha256='b'*64)),
            ('missing-source',lambda w:w['source_sha256'].pop(source_paths[0])),
            ('false-validation',lambda w:w.update(validated=False)),
            ('malformed-schema-digest',lambda w:w.update(schema_sha256='bad',reference_schema_sha256='bad'))]:
            faulty=json.loads(json.dumps(migration_report))
            for row in faulty['phases']['roundtrips']:change(row['equivalence_witness'])
            variants[name]=faulty
        for name,key,value in [('wrong-replay-count','case_count',len(module.CASES)),
                               ('wrong-replay-mode','replay_mode','executed')]:
            faulty=json.loads(json.dumps(migration_report));faulty['phases']['roundtrips'][1][key]=value
            variants[name]=faulty
        variants['missing-branch']={**migration_report,'phases':{**migration_report['phases'],'roundtrips':roundtrips[:1]}}
        for name,candidate in variants.items():
            migration_path.write_text(json.dumps(candidate))
            try:suite.validate('migration-undo-faults',folder)
            except (AssertionError,KeyError):pass
            else:raise AssertionError('Invalid migration evidence accepted: '+name)
            rows.append({'scenario':'migration-undo-faults-'+name,'passed':True})
        from tools.check_mutations import cases as legacy_faults
        legacy = [{'defect':case[0],'status':'DETECTED'} for case in legacy_faults]
        legacy_path=folder/'legacy-python-faults.json'
        legacy_path.write_text(json.dumps(legacy));suite.validate('legacy-python-faults',folder)
        rows.append({'scenario':'legacy-python-faults-complete-positive','passed':True})
        for name,candidate in [('truncated',legacy[:1]),('duplicate',legacy+[legacy[0]])]:
            legacy_path.write_text(json.dumps(candidate))
            try:suite.validate('legacy-python-faults',folder)
            except AssertionError:pass
            else:raise AssertionError('Invalid legacy evidence accepted')
            rows.append({'scenario':'legacy-python-faults-'+name,'passed':True})
        for stage,(filename,report,key) in reports.items():
            path=folder/filename
            path.write_text(json.dumps(report));suite.validate(stage,folder)
            rows.append({'scenario':stage+'-complete-positive','passed':True})
            variants={'truncated':{**report,key:report[key][:1]},
                      'duplicate':{**report,key:[*report[key],report[key][0]]}}
            if 'faults' in report:variants['missing-fault']={**report,'faults':report['faults'][1:]}
            if 'source_sha256' in report:variants['missing-source-manifest']={**report,'source_sha256':{}}
            if stage=='python-case-faults':
                faulty=json.loads(json.dumps(report));faulty['baseline']['cases'][python_cases[0]]['outcome']='failed'
                variants['contradictory-baseline']=faulty
                faulty=json.loads(json.dumps(report));next(r for r in faulty['faults'] if r['status']=='DETECTED').pop('scope_manifest_matches')
                variants['missing-scope-proof']=faulty
                faulty=json.loads(json.dumps(report));faulty['matrix'][0]['detects']=['invented-fault']
                variants['invented-detection']=faulty
            if stage=='quiz-case-faults':
                faulty=json.loads(json.dumps(report));faulty['baseline']['cases'][quiz_cases[0]]='failed'
                variants['contradictory-baseline']=faulty
                faulty=json.loads(json.dumps(report));faulty['matrix'][0]['detects']=['invented-fault']
                variants['invented-detection']=faulty
            if stage in {'browser-case-faults','database-lifecycle-faults'}:
                faulty=json.loads(json.dumps(report));faulty['cases'][0]['mutation']['outcome']='passed'
                variants['contradictory-mutation']=faulty
            if stage=='database-case-faults':
                variants['contradictory-preservation']={**report,'final_fingerprint':'b'*32}
                faulty=json.loads(json.dumps(report));faulty['cases'][0]['faults'].pop()
                variants['missing-pair']=faulty
            for mode,candidate in variants.items():
                path.write_text(json.dumps(candidate))
                try:suite.validate(stage,folder)
                except (AssertionError,KeyError):pass
                else:raise AssertionError('Invalid evidence accepted: '+stage+'-'+mode)
                rows.append({'scenario':stage+'-'+mode,'passed':True})
    return rows


def check_sql_shards():
    """Exercise the actual merge gate with independent faulty shard evidence."""
    sys.path.insert(0,str(ROOT))
    from tools.run_sql_shards import merge
    expected=['A','B','C','D'];source='a'*64
    targets=[{'name':name,'container':str(index+1)*64,'source':'3'*64,'fingerprint':'b'*32}
             for index,name in enumerate(['sql','sql-second'])]
    reports=[]
    for index in range(2):
        selected=expected[index::2]
        reports.append({'source_sha256':source,'preserved':True,'original_fingerprint':'b'*32,
                        'final_fingerprint':'b'*32,'cases':[{'case':name} for name in selected+(['test_failed_second_write_rolls_back_first_write_after_reconnect'] if index==0 else [])],
                        'shard':{'index':index,'total':2,'ordinary_case_count':4,'ordinary_case_ids':selected,'includes_reconnect':index==0}})
    result=merge(reports,targets,expected,source)
    assert [r['case'] for r in result['cases']]==expected+['test_failed_second_write_rolls_back_first_write_after_reconnect']
    rows=[{'scenario':'sql-shards-complete-positive','passed':True}]
    variants={}
    for mode in ['missing-case','duplicate-case','crossed-case','wrong-index','wrong-source','false-preservation','wrong-fingerprint','duplicate-target','missing-shard']:
        candidate=json.loads(json.dumps(reports));assigned=json.loads(json.dumps(targets))
        if mode=='missing-case':candidate[0]['cases'].pop()
        elif mode=='duplicate-case':candidate[0]['cases'].append(candidate[0]['cases'][0])
        elif mode=='crossed-case':candidate[1]['cases'][0]['case']='A'
        elif mode=='wrong-index':candidate[1]['shard']['index']=0
        elif mode=='wrong-source':candidate[1]['source_sha256']='c'*64
        elif mode=='false-preservation':candidate[1]['preserved']=False
        elif mode=='wrong-fingerprint':candidate[1]['final_fingerprint']='c'*32
        elif mode=='duplicate-target':assigned[1]['container']=assigned[0]['container']
        elif mode=='missing-shard':candidate.pop()
        try:merge(candidate,assigned,expected,source)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('Invalid SQL shard evidence accepted: '+mode)
        rows.append({'scenario':'sql-shards-'+mode,'passed':True})
    for value in ['2/2','-1/2','0/0','x/2']:
        result=subprocess.run([sys.executable,'tools/audit_database_cases.py','--shard',value,'--out','/tmp/unused-shard-report.json'],cwd=ROOT,capture_output=True,text=True,timeout=10)
        assert result.returncode==2 and '--shard' in result.stderr
        rows.append({'scenario':'sql-shards-refuse-'+value,'passed':True})
    result=subprocess.run([sys.executable,'tools/audit_database_cases.py','--shard','0/2','--only','F077','--out','/tmp/unused-shard-report.json'],cwd=ROOT,capture_output=True,text=True,timeout=10)
    assert result.returncode==2 and '--only' in result.stderr
    rows.append({'scenario':'sql-shards-refuse-partial-filter','passed':True})
    # Exercise the parent gate itself, not only the merge helper.
    from tools import run_test_suite as suite
    from tools.audit_database_cases import load_cases,recipes
    module,_=load_cases();ordinary=[case.id for case in module.CASES]
    digest=hashlib.sha256((ROOT/'tests/test_users_notes_database.py').read_bytes()).hexdigest()
    baseline_rows=[{'case':case.id,'effectiveness':'DEMONSTRATED','baseline':{'exit':0},
                    'faults':[{**fault,'status':'DETECTED_ASSERTION'} for fault in recipes(case)]} for case in module.CASES]
    baseline_rows.append({'case':'test_failed_second_write_rolls_back_first_write_after_reconnect',
                          'effectiveness':'DEMONSTRATED','baseline':{'exit':0},
                          'faults':[{'name':'premature-first-write-commit','status':'DETECTED_ASSERTION'}]})
    with tempfile.TemporaryDirectory(prefix='merlin-parent-shard-controls-') as temporary:
        folder=Path(temporary);(folder/'database-targets').mkdir()
        root='/tmp/merlin-db-sandboxes-'+'1'*32
        assigned=[{'name':name,'container':str(index+2)*64,'source':'4'*64,'fingerprint':'b'*32,
                   'root':root,'data':root+'/'+name,'socket':root+'/'+name+'/socket'}
                  for index,name in enumerate(['sql','sql-second'])]
        partitions=[]
        for index in range(2):
            selected=ordinary[index::2]
            partitions.append({'source_sha256':digest,'preserved':True,'original_fingerprint':'b'*32,'final_fingerprint':'b'*32,
                               'cases':[row for row in baseline_rows if row['case'] in set(selected+([baseline_rows[-1]['case']] if index==0 else []))],
                               'shard':{'index':index,'total':2,'ordinary_case_count':len(ordinary),'ordinary_case_ids':selected,'includes_reconnect':index==0}})
        combined=merge(partitions,assigned,ordinary,digest)
        def write(combined,parts,targets):
            (folder/'merlin-sql-effectiveness-final.json').write_text(json.dumps(combined))
            for index,(part,target) in enumerate(zip(parts,targets)):
                (folder/('merlin-sql-shard-'+str(index)+'.json')).write_text(json.dumps(part))
                (folder/'database-targets'/(target['name']+'.json')).write_text(json.dumps(target))
        write(combined,partitions,assigned);suite.validate('database-case-faults',folder)
        rows.append({'scenario':'sql-parent-shards-complete-positive','passed':True})
        for mode in ['contradictory-merged-proof','changed-child-outcome','missing-child','wrong-child-source','crossed-target']:
            top=json.loads(json.dumps(combined));parts=json.loads(json.dumps(partitions));targets=json.loads(json.dumps(assigned))
            if mode=='contradictory-merged-proof':top['shards'][0]['preserved']=False
            elif mode=='changed-child-outcome':parts[0]['cases'][0]['faults'][0]['status']='SURVIVED'
            elif mode=='wrong-child-source':parts[1]['source_sha256']='a'*64
            elif mode=='crossed-target':targets[1]['container']=targets[0]['container']
            write(top,parts,targets)
            if mode=='missing-child':(folder/'merlin-sql-shard-1.json').unlink()
            try:suite.validate('database-case-faults',folder)
            except (AssertionError,KeyError,FileNotFoundError):pass
            else:raise AssertionError('Invalid parent shard evidence accepted: '+mode)
            rows.append({'scenario':'sql-parent-shards-'+mode,'passed':True})
    return rows


def check_migration_schema_normalization():
    """Reject semantic changes while allowing inventory and generated OID changes."""
    from tools.verify_migration_roundtrip import canonical_schema, normalize

    original = [
        {'kind': 'index', 'keys': ['owner_id', 'created_at'], 'owner': 81234},
        {'kind': 'trigger', 'name': 'RI_ConstraintTrigger_a_92345'},
    ]
    roles = {'81234': 'synthetic_owner'}
    expected = [
        {'kind': 'index', 'keys': ['owner_id', 'created_at'], 'owner': 'synthetic_owner'},
        {'kind': 'trigger', 'name': 'RI_ConstraintTrigger_a_GENERATED'},
    ]
    canonical = canonical_schema(original, roles)
    changed = json.loads(json.dumps(original))
    changed[0]['keys'].reverse()
    missing = [original[0]]
    changed_owner = json.loads(json.dumps(original))
    changed_owner[0]['owner'] = 81235
    regenerated = json.loads(json.dumps(original))
    regenerated[1]['name'] = 'RI_ConstraintTrigger_a_99999'
    checks = {
        'migration-schema-literal-normalization': canonical == expected,
        'migration-schema-outer-order-equivalent': canonical_schema(original[::-1], roles) == canonical,
        'migration-schema-nested-order-change-rejected': canonical_schema(changed, roles) != canonical,
        'migration-schema-missing-row-rejected': canonical_schema(missing, roles) != canonical,
        'migration-schema-owner-change-rejected': canonical_schema(changed_owner, roles) != canonical,
        'migration-schema-generated-trigger-equivalent': canonical_schema(regenerated, roles) == canonical,
        'migration-schema-boolean-not-role-oid': normalize(True, {'1': 'synthetic_owner'}) is True,
    }
    for name, passed in checks.items():
        assert passed, name
    return [{'scenario': name, 'passed': True} for name in checks]


def check_compressor_privacy():
    """Exercise the bundled compressor without contacting an external provider."""
    import contextlib
    import importlib
    import importlib.util
    import io

    package_name = '_merlin_compressor_privacy_check'
    scripts = ROOT / '.agents/skills/caveman-compress/scripts'
    spec = importlib.util.spec_from_file_location(
        package_name, scripts / '__init__.py', submodule_search_locations=[str(scripts)])
    package = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = package
    spec.loader.exec_module(package)
    compressor = importlib.import_module(package_name + '.compress')
    checks = {}
    with tempfile.TemporaryDirectory(prefix='merlin-compressor-privacy-') as directory:
        root = Path(directory)
        source = root / 'public-guide.md'
        frontmatter = '---\nprivate_fixture: SYNTHETIC_FRONTMATTER_SENTINEL\n---\n'
        first_code = '```text\nSYNTHETIC_CODE_SENTINEL\n```\n'
        last_code = '```text\nSYNTHETIC_SECOND_CODE_SENTINEL\n```\n'
        code = first_code + '\n' + last_code
        original = frontmatter + '# Title\n\n## Required\n\n' + ('Detailed public explanation. ' * 12) + '\n\n' + code
        source.write_text(original)
        masked, blocks = compressor.mask_code_blocks(compressor.split_frontmatter(original)[1])
        first_marker, last_marker = blocks[0][0], blocks[1][0]
        candidates = ['# Title\n\nBrief.\n\n' + last_marker + '\n\n' + first_marker + '\n',
                      '# Title\n\n## Required\n\nBrief.\n\n' + first_marker + '\n\n' + last_marker + '\n']
        prompts = []
        def response(prompt):
            prompts.append(prompt)
            return candidates[len(prompts) - 1]
        with patch.object(compressor, 'backup_dir_for', return_value=root / 'backups'), \
             patch.dict(os.environ, {'XDG_DATA_HOME': str(root / 'data')}), \
             patch.object(compressor, 'call_claude', side_effect=response), \
             contextlib.redirect_stdout(io.StringIO()):
            checks['compressor-repair-succeeds'] = compressor.compress_file(source)
        checks['compressor-real-validation-retry-exercised'] = len(prompts) == 2
        checks['compressor-code-and-frontmatter-stay-local'] = all(
            sentinel not in prompt for prompt in prompts
            for sentinel in ['SYNTHETIC_FRONTMATTER_SENTINEL', 'SYNTHETIC_CODE_SENTINEL', 'SYNTHETIC_SECOND_CODE_SENTINEL'])
        checks['compressor-protected-content-restored'] = (
            source.read_text().startswith(frontmatter) and source.read_text().endswith(code)
            and (root / 'backups/public-guide.original.md').read_text() == original)
        retry_candidate = prompts[1].partition('COMPRESSED (fix this):')[2] if len(prompts) == 2 else ''
        checks['compressor-reordered-code-repair-retained'] = (
            0 <= retry_candidate.find(last_marker) < retry_candidate.find(first_marker)
            and source.read_text().index(first_code) < source.read_text().index(last_code))
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': ''}), \
             patch.object(compressor.subprocess, 'run', side_effect=subprocess.CalledProcessError(
                 1, ['claude'], stderr='SYNTHETIC_EXTERNAL_ERROR_SENTINEL')):
            try:
                compressor.call_claude('Public fixture')
            except RuntimeError as error:
                import traceback
                checks['compressor-cli-error-redacted'] = (
                    'SYNTHETIC_EXTERNAL_ERROR_SENTINEL' not in ''.join(traceback.format_exception(error)))
            else:
                checks['compressor-cli-error-redacted'] = False
    for name, passed in checks.items():
        assert passed, name
    return [{'scenario': name, 'passed': True} for name in checks]


def check_runtime_commit_compatibility():
    from tools.database_sandboxes import DatabaseSandboxes
    sandbox = DatabaseSandboxes('/unused-control-output')
    sandbox.source = 'a' * 64
    image = 'sha256:' + 'b' * 64
    digest = 'c' * 64
    commits = []
    def docker(arguments, timeout=20):
        if arguments[0] == 'diff':
            return ''
        if arguments[0] == 'commit':
            # An older Docker CLI rejects the newer --no-pause flag.
            assert '--no-pause' not in arguments
            commits.append(arguments)
            return image
        assert arguments == ['image', 'inspect', image]
        return json.dumps([{'Config': {'Labels': {}}}])
    def run(command, **kwargs):
        if command[:3] == ['docker', 'image', 'inspect']:
            return subprocess.CompletedProcess(command, 1, '', '')
        assert command[:3] == ['docker', 'exec', '-i']
        return subprocess.CompletedProcess(command, 0, digest, '')
    try:
        with patch.object(sandbox, 'docker', side_effect=docker), patch('subprocess.run', side_effect=run):
            sandbox.prepare_runtime()
        assert len(commits) == 1 and sandbox.image == image
        assert sandbox.evidence['runtime_digest'] == digest
    finally:
        if sandbox.temporary is not None:
            sandbox.temporary.cleanup()
    return [{'scenario': 'runtime-commit-older-docker-compatible', 'passed': True}]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='merlin-suite-controls-') as directory:
        # Each scenario has its own lock, trace, child process and output folder.
        # Join every scenario before the shared subprocess mock below is used.
        with ThreadPoolExecutor(max_workers=5) as pool:
            rows=list(pool.map(lambda mode:check(mode,Path(directory)),
                               ['pass','serial','failure','setup-failure','interrupt','baseline-failure','interrupt-setup','prerequisite-failure']))
    rows.extend(check_preflight())
    rows.extend(check_result_validation())
    rows.extend(check_sql_shards())
    rows.extend(check_migration_schema_normalization())
    rows.extend(check_compressor_privacy())
    rows.extend(check_runtime_commit_compatibility())
    if args.out:args.out.write_text(json.dumps({'checks':rows},indent=2)+'\n')
    print('Suite scheduling, first failure and interrupt cleanup controls PASS')


if __name__=='__main__':
    main()
