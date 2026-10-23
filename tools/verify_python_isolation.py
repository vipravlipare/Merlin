"""Verify unattended fault workers against real inherited terminal input."""
import argparse
import json
import fcntl
import os
from pathlib import Path
import pty
import subprocess
import sys
import termios

ROOT=Path(__file__).resolve().parents[1]
WORKER=r'''
import json,os,sys,tempfile,time,signal,ctypes
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path.cwd()))
from tools.audit_python_cases import faults,request,outcome,execute,is_import_guard_reversal
from tools.isolated_python import fork_jobs
mode=sys.argv[1]
assert os.isatty(0), 'Regression requires real terminal input'
with open('/dev/tty') as terminal:
 assert terminal.isatty(), 'Regression requires a controlling terminal'
with tempfile.TemporaryDirectory(prefix='merlin-python-isolation-') as directory:
 if mode=='nested-timeout':
  # Adopt only this worker's descendants so the synthetic grandchild can be
  # reaped after its owner is killed; no unrelated processes are inspected.
  assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
  marker=Path(directory)/'nested-pid'
  fixture=Path(directory)/'bounded-child.py'
  fixture.write_text('import os,time\nfrom pathlib import Path\nPath('+repr(str(marker))+').write_text(str(os.getpid()))\ntime.sleep(5)\n')
  job={'argv':[],'code':'from tools.isolated_python import run_script\nrun_script('+repr([sys.executable,str(fixture)])+',capture_output=True,text=True,timeout=4)',
       'stdout':Path(directory)/'out','stderr':Path(directory)/'err'}
  child=None
  try:
   code,out,err=next(fork_jobs([job],workers=1,timeout=.5))
   assert code is None, (code,out,err)
   assert marker.exists(), 'Nested child never started'
   child=int(marker.read_text())
   deadline=time.monotonic()+1
   while time.monotonic()<deadline:
    ended,status=os.waitpid(child,os.WNOHANG)
    if ended:break
    time.sleep(.01)
   else:raise AssertionError('Nested CLI survived its owner timeout')
   child=None
   assert os.waitstatus_to_exitcode(status)==-signal.SIGKILL
  finally:
   # Reap the owned synthetic child even when the regression assertion fails.
   if child is None and marker.exists():
    candidate=int(marker.read_text())
    try:
     ended,status=os.waitpid(candidate,os.WNOHANG)
     if not ended:child=candidate
    except ChildProcessError:pass
   if child is not None:
    os.kill(child,signal.SIGKILL);os.waitpid(child,0)
 elif mode in {'fork-probe','subprocess-probe'}:
  name,file,old,new=next(row for row in faults()
   if row[1]=='app/database_connectivity_probe.py'
   and is_import_guard_reversal(Path(row[1]).read_text(),Path(row[1]).read_text().replace(row[2],row[3])))
  source=(Path(file).read_text()).replace(old,new)
  if mode=='fork-probe':
   job=request(name,file,source,directory)
   code,out,err=next(fork_jobs([job],workers=1,timeout=2))
   report=outcome(job,code,err)
  else:
   import subprocess
   original=subprocess.run
   def bounded(*args,**kwargs):
    kwargs['timeout']=2
    return original(*args,**kwargs)
   with patch('tools.audit_python_cases.subprocess.run',side_effect=bounded):
    report=execute(name,file,source,directory)
  assert report['status']=='INVALID' and 'EOFError' in report['reason'], report
 else:
  job={'argv':[],'code':"import sys\nassert not sys.stdin.isatty()\ntry:input()\nexcept EOFError:print('EOF confirmed')\nelse:raise AssertionError('Worker received terminal input')",'stdout':Path(directory)/'out','stderr':Path(directory)/'err'}
  if mode=='real-timeout':job['code']='import time; time.sleep(30)'
  code,out,err=next(fork_jobs([job],workers=1,timeout=.2 if mode=='real-timeout' else 2))
  if mode=='real-timeout':assert code is None, 'Real timeout was accepted'
  else:assert code==0 and out.strip()=='EOF confirmed',(code,out,err)
 print(json.dumps({'case':mode,'passed':True}))
'''


def verify():
    rows=[]
    for mode in ['fork-probe','subprocess-probe','stdin-isolated','real-timeout','nested-timeout']:
        master,slave=pty.openpty()
        try:
            result=subprocess.run([sys.executable,'-c',WORKER,mode],cwd=ROOT,
                                  stdin=slave,capture_output=True,text=True,timeout=10,
                                  start_new_session=True,
                                  preexec_fn=lambda:fcntl.ioctl(0,termios.TIOCSCTTY,0))
            assert result.returncode==0, mode+' failed: '+result.stderr
            rows.append(json.loads(result.stdout))
        finally:
            os.close(master);os.close(slave)
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    rows=verify()
    if args.out:args.out.write_text(json.dumps({'checks':rows},indent=2)+'\n')
    print('Python terminal isolation and real timeout controls PASS')
