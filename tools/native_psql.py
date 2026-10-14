"""Launch fresh native psql processes through one verified container transport.

Only Docker CLI startup is amortized. Every request launches and closes its own
psql process and database connection. Interactive holders still use normal Popen.
"""
import atexit
import json
import os
import selectors
import subprocess
import threading

from tools.database_test_session import container_command, test_container

SERVER = r'''
import json, select, signal, subprocess, sys, tempfile, time
print(json.dumps({'ready':True}),flush=True)
for line in sys.stdin:
 request=json.loads(line)
 command=request['command']
 if not command or command[0]!='psql' or 'ON_ERROR_STOP=1' not in command:
  raise RuntimeError('Only guarded native psql with ON_ERROR_STOP is allowed')
 # A seekable input avoids the container Python's interrupted-communicate stdin bug.
 with tempfile.TemporaryFile(mode='w+t',encoding='utf8') as script:
  script.write(request['input']);script.seek(0)
  process=subprocess.Popen(command,stdin=script,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  started=time.monotonic();disconnected=False
  while True:
   try:
    output,errors=process.communicate(timeout=.05)
    response={'exit':process.returncode,'stdout':output,'stderr':errors}
    break
   except subprocess.TimeoutExpired:
    disconnected=bool(select.select([sys.stdin],[],[],0)[0])
    if time.monotonic()-started>=request['timeout'] or disconnected:
     # SIGINT asks psql/libpq to cancel the server query before closing its connection.
     # ON_ERROR_STOP prevents subsequent SQL, including a COMMIT, from running.
     process.send_signal(signal.SIGINT)
     try:process.communicate(timeout=5)
     except subprocess.TimeoutExpired:
      process.kill();process.communicate()
      raise RuntimeError('Native query cancellation did not finish')
     response={'timeout':True}
     break
 if disconnected:break
 print(json.dumps(response),flush=True)
'''
_process = None
_lock = threading.Lock()


def close():
    global _process
    if _process is not None:
        process, _process = _process, None
        process.stdin.close()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait()
        process.stdout.close()
        process.stderr.close()


atexit.register(close)


def read(timeout):
    with selectors.DefaultSelector() as selector:
        selector.register(_process.stdout, selectors.EVENT_READ)
        if not selector.select(timeout):
            raise subprocess.TimeoutExpired('native psql transport', timeout)
        line = _process.stdout.readline()
    if not line:
        raise RuntimeError('Native psql transport ended unexpectedly')
    return json.loads(line)


def run(command, *, input, text=True, capture_output=True, timeout=30):
    """Preserve native psql argv, script, stdout, stderr, exit and fresh connection."""
    global _process
    if os.environ.get('MERLIN_FAST_DB_TESTS') != '1':
        return subprocess.run(command, input=input, text=text, capture_output=capture_output, timeout=timeout)
    prefix = ['docker', 'exec', '-i', test_container()]
    if command[:4] != prefix or command[4:5] != ['psql'] or 'ON_ERROR_STOP=1' not in command or not text or not capture_output:
        raise ValueError('Native psql transport requires the verified disposable command')
    with _lock:
        try:
            if _process is None:
                _process = subprocess.Popen(container_command(['python3', '-u', '-c', SERVER]),
                                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if read(15) != {'ready': True}:
                    raise RuntimeError('Native psql transport readiness failed')
            request = {'command':command[4:], 'input':input, 'timeout':timeout}
            _process.stdin.write((json.dumps(request)+'\n').encode()); _process.stdin.flush()
            result = read(timeout+6)
            if result.get('timeout'):
                raise subprocess.TimeoutExpired(command, timeout)
            return subprocess.CompletedProcess(command, result['exit'], result['stdout'], result['stderr'])
        except BaseException:
            close()
            raise
