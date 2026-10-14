"""Prove real target routing, fault isolation and fail-closed sandbox guards."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

PROBE="""from tools.database_test_session import DatabaseTestSession,container_command
with DatabaseTestSession() as session:
 result=session.run(container_command(['psql']),input="SELECT current_setting('data_directory');")
 assert result.returncode==0
 print(result.stdout.strip())
"""


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    from tools.database_sandboxes import LANES
    lanes=LANES if os.environ.get('MERLIN_SQL_SHARDS','2') == '2' else LANES[:3]
    targets={name:json.loads((args.targets/(name+'.json')).read_text()) for name in lanes}
    assert len({t['container'] for t in targets.values()})==len(lanes)
    rows=[]
    def probe(path):
        env=dict(os.environ,MERLIN_DB_SANDBOX=str(path))
        return subprocess.run([sys.executable,'-c',PROBE],env=env,cwd=ROOT,text=True,capture_output=True,timeout=20)
    def route(name):
        target=targets[name]
        result=probe(args.targets/(name+'.json'))
        assert result.returncode==0 and result.stdout.strip()==target['data'], 'Actual target routing failed: '+name+'\n'+result.stderr
        print('route-'+name+' PASS',flush=True)
        return {'case':'route-'+name,'passed':True}
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows.extend(pool.map(route,targets))
    # Poison inspection metadata while retaining the real, working copy. If a
    # boundary guard disappears, the unchanged live query would pass and this
    # check fails. Never create an unsafe mount, network or published port.
    metadata_faults=[('cpu-limit-changed',"info['HostConfig']['NanoCpus']=3000000000",'ownership, isolation or resource limits differ'),
                     ('memory-limit-changed',"info['HostConfig']['Memory']=2147483648",'ownership, isolation or resource limits differ'),
                     ('external-network-refused',"info['HostConfig']['NetworkMode']='bridge'",'ownership, isolation or resource limits differ'),
                     ('shared-source-volume-refused',"next(m for m in info['Mounts'] if m['Type']=='volume')['Name']='merlin-d6-20261008105707_postgres_data'",'unexpected or shared storage'),
                     ('published-port-refused',"info['NetworkSettings']['Ports']={'5432/tcp':[{'HostIp':'127.0.0.1','HostPort':'55433'}]}",'published ports or inherited Desktop'),
                     ('stale-desktop-port-refused',"info['Config']['Labels']['desktop.docker.io/ports/5432/tcp']='127.0.0.1:55432'",'published ports or inherited Desktop')]
    def metadata_reject(case):
        name,change,reason=case
        script="""import json,subprocess
from unittest.mock import patch
original=subprocess.run
def inspected(command,*args,**kwargs):
 result=original(command,*args,**kwargs)
 if command[:3]==['docker','container','inspect'] and command[3]==%r:
  info=json.loads(result.stdout)[0]
  %s
  return subprocess.CompletedProcess(command,result.returncode,json.dumps([info]),result.stderr)
 return result
with patch('subprocess.run',side_effect=inspected):
""" % (targets['sql']['container'],change)
        script+='\n'.join(' '+line for line in PROBE.splitlines())
        result=subprocess.run([sys.executable,'-c',script],env=dict(os.environ,MERLIN_DB_SANDBOX=str(args.targets/'sql.json')),cwd=ROOT,text=True,capture_output=True,timeout=20)
        assert result.returncode!=0 and reason in result.stderr, 'Metadata boundary did not reject '+name+'\n'+result.stderr
        return {'case':name,'passed':True}
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows.extend(pool.map(metadata_reject,metadata_faults))
    with tempfile.TemporaryDirectory(prefix='merlin-sandbox-guards-') as directory:
        path=Path(directory)/'bad.json';base=targets['sql']
        changes=[('source-as-clone',{'container':base['source']},'Sandbox must have an independent container'),
                 ('source-volume-path',{'data':'/var/lib/postgresql/data'},'Sandbox paths are not independent temporary storage'),
                 ('wrong-source',{'source':'0'*64},'Sandbox belongs to a different container'),
                 ('wrong-container',{'container':'0'*64},'Cannot inspect the sandbox container'),
                 ('crossed-socket',{'socket':targets['migration']['socket']},'Sandbox paths are not independent temporary storage'),
                 ('wrong-fingerprint',{'fingerprint':'0'*32},'Sandbox target verification failed; no fallback to source')]
        def reject(change_case):
            name,change,reason=change_case
            candidate=Path(directory)/(name+'.json')
            candidate.write_text(json.dumps(dict(base,**change)));candidate.chmod(0o600)
            refused=probe(candidate)
            assert refused.returncode!=0 and reason in refused.stderr, 'Expected guard did not reject manifest: '+name+'\n'+refused.stderr
            print(name+' PASS',flush=True)
            return {'case':name,'passed':True}
        with ThreadPoolExecutor(max_workers=6) as pool:
            rows.extend(pool.map(reject,changes))
        path.write_text(json.dumps(base));path.chmod(0o644)
        refused=probe(path)
        assert refused.returncode!=0 and 'Sandbox manifest must be private and owned by this user' in refused.stderr
        rows.append({'case':'public-manifest-refused','passed':True})
        link=Path(directory)/'link.json';link.symlink_to(args.targets/'sql.json')
        refused=probe(link)
        assert refused.returncode!=0 and 'Too many levels of symbolic links' in refused.stderr
        rows.append({'case':'manifest-symlink-refused','passed':True})
        from tools.database_sandboxes import RUNTIME_FUNCTION
        namespace={};exec(RUNTIME_FUNCTION,namespace)
        sample=Path(directory)/'dependency.py';sample.write_text('VERSION=1\n')
        digest=namespace['runtime_digest'];entries=[['A',str(sample)]]
        original=digest(entries);sample.write_text('VERSION=2\n')
        assert digest(entries)!=original
        rows.append({'case':'changed-runtime-content-invalidates-cache','passed':True})
        sample.unlink()
        try:digest(entries)
        except FileNotFoundError:pass
        else:raise AssertionError('Missing runtime file was accepted')
        rows.append({'case':'missing-runtime-file-refused','passed':True})
    def command(target=None):
        args=['docker','exec','-i',base['source'] if target is None else target['container'],'psql','-X','-qAt']
        if target:args+=['-h',target['socket']]
        return args+['-U','merlin_d6','-d','merlin_d6','-v','ON_ERROR_STOP=1']
    # Keep a live, deliberately faulty function in one transaction. Other
    # physical copies and the original must still execute the correct function.
    holder=subprocess.Popen(command(base),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    print('Checking live fault isolation',flush=True)
    try:
        holder.stdin.write("BEGIN;CREATE OR REPLACE FUNCTION public.note_weighted_length(value TEXT) RETURNS INTEGER LANGUAGE plpython3u AS $fault$return 0$fault$;SELECT 'READY:'||public.note_weighted_length('abc');\n")
        holder.stdin.flush()
        with selectors.DefaultSelector() as selector:
            selector.register(holder.stdout,selectors.EVENT_READ)
            assert selector.select(10), 'Fault holder did not become ready'
            assert holder.stdout.readline().strip()=='READY:0'
        def check_unaffected(target):
            result=subprocess.run(command(target),input="SELECT public.note_weighted_length('abc');",text=True,capture_output=True,timeout=10)
            assert result.returncode==0 and result.stdout.strip()=='3', 'Fault escaped its physical copy'
        with ThreadPoolExecutor(max_workers=3) as pool:
            list(pool.map(check_unaffected,[None,*[target for name,target in targets.items() if name!='sql']]))
        rows.append({'case':'live-fault-isolated-from-other-copies-and-source','passed':True})
    finally:
        try:
            holder.stdin.write('ROLLBACK;\n');holder.stdin.flush();holder.communicate(timeout=10)
        except BaseException:
            holder.kill();holder.communicate()
    result=subprocess.run(command(base),input="SELECT public.note_weighted_length('abc');",text=True,capture_output=True,timeout=10)
    assert result.returncode==0 and result.stdout.strip()=='3'
    rows.append({'case':'control-fault-rolled-back','passed':True})
    args.out.write_text(json.dumps({'checks':rows},indent=2)+'\n')
    print('Database routing, isolation, runtime cache and refusal controls PASS')


if __name__=='__main__':main()
