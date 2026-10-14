"""Run two serial SQL audits on independent guarded copies, then verify their union."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
NAMES=('sql','sql-second')


def merge(reports, targets, expected, source_hash):
    assert len(reports)==len(targets)==2
    assert len({t['container'] for t in targets})==2
    assert [t['name'] for t in targets]==list(NAMES)
    assert len({t['source'] for t in targets})==1
    assert len({t['fingerprint'] for t in targets})==1
    rows=[];proof=[]
    reconnect='test_failed_second_write_rolls_back_first_write_after_reconnect'
    for index,(report,target) in enumerate(zip(reports,targets)):
        selected=expected[index::2]
        actual=[r['case'] for r in report['cases']]
        assert len(actual)==len(set(actual))
        assert set(actual)==set(selected+([reconnect] if index==0 else []))
        assert report['shard']=={'index':index,'total':2,'ordinary_case_count':len(expected),
                                'ordinary_case_ids':selected,'includes_reconnect':index==0}
        assert report['source_sha256']==source_hash
        assert report['preserved'] is True
        assert report['original_fingerprint']==report['final_fingerprint']==target['fingerprint']
        proof.append({'index':index,'target':target,'case_ids':actual,'preserved':True,
                      'original_fingerprint':report['original_fingerprint'],'final_fingerprint':report['final_fingerprint']})
        rows.extend(report['cases'])
    assert len(rows)==len(expected)+1 and len({r['case'] for r in rows})==len(rows)
    order={name:index for index,name in enumerate([*expected,reconnect])}
    return {'source_sha256':source_hash,'original_fingerprint':targets[0]['fingerprint'],
            'final_fingerprint':targets[0]['fingerprint'],'preserved':True,
            'cases':sorted(rows,key=lambda r:order[r['case']]),'shards':proof}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    from tools.database_sandboxes import validate_manifest
    targets=[validate_manifest(json.loads((args.targets/(name+'.json')).read_text())) for name in NAMES]
    assert targets[0]['container']!=targets[1]['container']
    def audit(index):
        output=args.out.parent/('merlin-sql-shard-'+str(index)+'.json')
        env=dict(os.environ,MERLIN_DB_SANDBOX=str(args.targets/(NAMES[index]+'.json')))
        command=[sys.executable,'tools/audit_database_cases.py','--shard',str(index)+'/2','--out',str(output)]
        result=subprocess.run(command,cwd=ROOT,env=env)
        if result.returncode:raise RuntimeError('SQL shard failed: '+str(index))
        return json.loads(output.read_text())
    # Children inherit this process group, so runner interruption reaches both.
    with ThreadPoolExecutor(max_workers=2) as pool:reports=list(pool.map(audit,range(2)))
    from tools.audit_database_cases import load_cases
    module,_=load_cases()
    result=merge(reports,targets,[case.id for case in module.CASES],
                 hashlib.sha256((ROOT/'tests/test_users_notes_database.py').read_bytes()).hexdigest())
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print('Complete SQL shard union and both-copy preservation PASS',flush=True)


if __name__=='__main__':main()
