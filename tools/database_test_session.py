"""Reuse a guarded libpq connection for rollback-only SQL test experiments.

The existing container supplies Python and libpq; no installation or credentials
are added. Each experiment still runs its original SQL and stops at its first
server error. Real reconnect, psql-command and concurrency checks use psql.
"""
import json
from functools import lru_cache
import os
from pathlib import Path
import re
import selectors
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'merlin-d6-20261008105707'
CLUSTER = '7694311451826794534'


@lru_cache(maxsize=1)
def disposable_container():
    """Resolve and verify the already running disposable Compose service once."""
    result = subprocess.run(['docker', 'compose', '-p', PROJECT, 'ps', '-q', 'postgres'],
                            cwd=ROOT, capture_output=True, text=True, timeout=15)
    identifier = result.stdout.strip()
    if result.returncode or not re.fullmatch(r'[0-9a-f]{64}', identifier):
        raise RuntimeError('Expected exactly one existing disposable PostgreSQL container')
    layout = '{{.State.Running}}|{{index .Config.Labels "com.docker.compose.project"}}|{{index .Config.Labels "com.docker.compose.service"}}'
    inspected = subprocess.run(['docker', 'container', 'inspect', '--format', layout, identifier],
                               capture_output=True, text=True, timeout=15)
    if inspected.returncode or inspected.stdout.strip() != 'true|' + PROJECT + '|postgres':
        raise RuntimeError('Disposable container identity differs from expected labels')
    return identifier


def container_command(arguments):
    target = database_target()
    if target and arguments[:1] == ['psql']:
        if '-h' in arguments or '--host' in arguments:
            raise RuntimeError('Sandbox command already specifies a host')
        arguments = [arguments[0], '-h', target['socket'], *arguments[1:]]
    return ['docker', 'exec', '-i', test_container(), *arguments]


def test_container():
    target = database_target()
    return target['container'] if target else disposable_container()


@lru_cache(maxsize=1)
def database_target():
    """Admit only a private manifest and a verified independent physical copy."""
    manifest = os.environ.get('MERLIN_DB_SANDBOX')
    if not manifest:
        return None
    from tools.database_sandboxes import validate_manifest,volume_name
    descriptor = os.open(manifest, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor) as source:
        permissions = os.fstat(source.fileno())
        if permissions.st_uid != os.getuid() or permissions.st_mode & 0o777 != 0o600:
            raise RuntimeError('Sandbox manifest must be private and owned by this user')
        target = validate_manifest(json.load(source))
    if target['source'] != disposable_container():
        raise RuntimeError('Sandbox belongs to a different container')
    inspected=subprocess.run(['docker','container','inspect',target['container']],capture_output=True,text=True,timeout=10)
    if inspected.returncode:raise RuntimeError('Cannot inspect the sandbox container')
    information=json.loads(inspected.stdout)
    if len(information)!=1:raise RuntimeError('Ambiguous sandbox container')
    information=information[0];labels=information['Config']['Labels'];limits=information['HostConfig']
    actual='|'.join(map(str,[str(information['State']['Running']).lower(),labels.get('merlin.audit.source'),
                             labels.get('merlin.audit.root'),labels.get('merlin.audit.lane'),
                             limits['NetworkMode'],limits['NanoCpus'],limits['Memory']]))
    expected='true|'+target['source']+'|'+target['root']+'|'+target['name']+'|none|1000000000|1073741824'
    if actual!=expected or information['Id']!=target['container']:
        raise RuntimeError('Sandbox container ownership, isolation or resource limits differ')
    # Desktop may retain an empty binding placeholder and add its WSL distro
    # label. Reject actual addresses/ports and stale forwarding labels. The
    # independently checked `none` network cannot publish a TCP listener.
    bindings=limits.get('PortBindings') or {}
    if (any(binding.get('HostIp') or binding.get('HostPort') for rows in bindings.values() for binding in (rows or []))
        or any(information['NetworkSettings'].get('Ports',{}).values())
        or any(value for key,value in labels.items() if key.startswith('desktop.docker.io/ports/'))):
        raise RuntimeError('Sandbox contains published ports or inherited Desktop forwarding metadata')
    volumes=[]
    for mount in information['Mounts']:
        if mount['Type']=='volume' and mount['Destination']==target['data'] and mount['Name']==volume_name(target['root'],target['name']) and mount['RW'] is True:
            volumes.append(mount['Name'])
        elif mount['Type']!='tmpfs' or mount['Destination']!='/var/lib/postgresql/data':
            raise RuntimeError('Sandbox uses unexpected or shared storage')
    if len(volumes)!=1:raise RuntimeError('Sandbox does not have exactly one independent data volume')
    volume=subprocess.run(['docker','volume','inspect',volumes[0]],capture_output=True,text=True,timeout=10)
    if volume.returncode:raise RuntimeError('Cannot verify disposable volume ownership')
    info=json.loads(volume.stdout)[0];labels=info.get('Labels') or {}
    if (info['Name']!=volumes[0] or info['Driver']!='local' or info.get('Options')
        or labels.get('merlin.audit.root')!=target['root'] or labels.get('merlin.audit.source')!=target['source']):
        raise RuntimeError('Sandbox volume ownership or local storage differs')
    from tools.audit_database_cases import FINGERPRINT
    verify = r'''
import json,os,pathlib,subprocess,sys
target=json.loads(sys.argv[1]);data=pathlib.Path(target['data'])
if str(data.resolve())!=str(data) or str(pathlib.Path(target['socket']).resolve())!=target['socket']:raise RuntimeError('Sandbox path redirects')
if (data/'postmaster.pid').read_text().splitlines()[1]!=str(data):raise RuntimeError('Sandbox postmaster identity differs')
query="SELECT current_setting('data_directory'),current_database(),system_identifier,pg_is_in_recovery(),current_setting('listen_addresses'),current_setting('fsync'),current_setting('full_page_writes'),current_setting('synchronous_commit') FROM pg_control_system();SELECT (SELECT count(*) FROM public.users),(SELECT count(*) FROM public.notes);"+sys.argv[2]
r=subprocess.run(['psql','-X','-qAt','-h',target['socket'],'-U','merlin_d6','-d','merlin_d6','-v','ON_ERROR_STOP=1'],input=query,capture_output=True,text=True,timeout=10)
expected=[target['data']+'|merlin_d6|7694311451826794534|f||on|on|on','0|0',target['fingerprint']]
if r.returncode or r.stdout.splitlines()!=expected:raise RuntimeError('Sandbox target or schema verification failed')
print('Verified independent physical copy')
'''
    result = subprocess.run(['docker', 'exec', '-i', target['container'], 'python3', '-c', verify,
                             json.dumps(target), FINGERPRINT], capture_output=True, text=True, timeout=15)
    if result.returncode or result.stdout.strip() != 'Verified independent physical copy':
        raise RuntimeError('Sandbox target verification failed; no fallback to source')
    return target


# Send each original statement separately to preserve statement timestamps.
# Retain every SELECT result, including the mutation-ready marker.
SERVER = r'''
import ctypes as c, ctypes.util, json, sys
pq=c.CDLL(ctypes.util.find_library('pq'))
def bind(name,result,*args):
 f=getattr(pq,name);f.restype=result;f.argtypes=list(args);return f
ptr=c.c_void_p; integer=c.c_int; string=c.c_char_p
connect=bind('PQconnectdb',ptr,string);status=bind('PQstatus',integer,ptr)
finish=bind('PQfinish',None,ptr);send=bind('PQsendQuery',integer,ptr,string)
get=bind('PQgetResult',ptr,ptr);clear=bind('PQclear',None,ptr)
result_status=bind('PQresultStatus',integer,ptr)
rows=bind('PQntuples',integer,ptr);columns=bind('PQnfields',integer,ptr)
value=bind('PQgetvalue',string,ptr,integer,integer)
error=bind('PQresultErrorMessage',string,ptr)
transaction=bind('PQtransactionStatus',integer,ptr)
conn=connect(('dbname=merlin_d6 user=merlin_d6 connect_timeout=3 application_name=merlin_rollback_test_session options=\'-c statement_timeout=10000 -c lock_timeout=2000\''+(' host='+sys.argv[1] if len(sys.argv)>1 else '')).encode())
if not conn or status(conn)!=0:raise RuntimeError('Disposable connection failed')
def execute(sql):
 if send(conn,sql.encode('utf8'))!=1:raise RuntimeError('Query dispatch failed')
 output=[];errors=[]
 while True:
  result=get(conn)
  if not result:break
  try:
   state=result_status(result)
   if state==2:
    for row in range(rows(result)):
     output.append('|'.join(value(result,row,column).decode('utf8') for column in range(columns(result))))
   elif state not in (0,1):errors.append(error(result).decode('utf8'))
  finally:clear(result)
 if status(conn)!=0:raise RuntimeError('Disposable connection lost')
 return {'exit':3 if errors else 0,'stdout':''.join(line+'\n' for line in output),'stderr':''.join(errors)}
def checked(sql):
 result=execute(sql)
 if result['exit']:raise RuntimeError('Session cleanup or identity query failed')
 return result['stdout'].splitlines()
try:
 expected=['merlin_d6|7694311451826794534','0|0']
 probe='SELECT current_database(),system_identifier FROM pg_control_system(); SELECT (SELECT count(*) FROM public.users),(SELECT count(*) FROM public.notes);'
 if checked(probe)!=expected:raise RuntimeError('Unexpected or nonempty disposable target')
 print(json.dumps({'ready':True}),flush=True)
 for line in sys.stdin:
  try:
   statements=json.loads(line)['statements']
   result={'exit':0,'stdout':'','stderr':''}
   for statement in statements:
    part=execute(statement)
    result['stdout']+=part['stdout'];result['stderr']+=part['stderr']
    if part['exit']:
     result['exit']=part['exit'];break
   # Stop on the first failing statement, just as psql ON_ERROR_STOP does. Explicit rollback clears
   # failed transactions; DISCARD ALL resets roles, settings, temp objects,
   # prepared plans and advisory locks before the next independent experiment.
   if transaction(conn) in (2,3):checked('ROLLBACK;')
   checked('DISCARD ALL;')
   if transaction(conn)!=0 or checked(probe)!=expected:
    raise RuntimeError('Experiment did not preserve empty target and identity')
   print(json.dumps(result),flush=True)
  except Exception:
   print(json.dumps({'transport_error':'Experiment isolation or transport failed'}),flush=True)
   break
finally:finish(conn)
'''


def split_sql(sql):
    """Keep psql statement boundaries, including dollar-quoted function bodies.

    This lexer only locates semicolons outside PostgreSQL strings/comments; it
    never parses or rewrites SQL. Statement text is passed to libpq unchanged.
    """
    pieces = []
    start = index = 0
    quote = dollar = None
    escaped = False
    block_depth = 0
    line_comment = False
    punctuation = re.compile(r"[;\"'$/-]")
    while index < len(sql):
        if dollar:
            ending = sql.find(dollar, index)
            if ending < 0:
                raise ValueError('Unterminated SQL string or block comment')
            index = ending + len(dollar)
            dollar = None
            continue
        if not (quote or block_depth or line_comment):
            next_token = punctuation.search(sql, index)
            if next_token is None:
                index = len(sql)
                break
            index = next_token.start()
        char = sql[index]
        pair = sql[index:index + 2]
        if line_comment:
            if char == '\n':
                line_comment = False
        elif block_depth:
            if pair == '/*':
                block_depth += 1
                index += 1
            elif pair == '*/':
                block_depth -= 1
                index += 1
        elif dollar:
            if sql.startswith(dollar, index):
                index += len(dollar) - 1
                dollar = None
        elif quote:
            if escaped and char == '\\':
                index += 1
            elif char == quote:
                if index + 1 < len(sql) and sql[index + 1] == quote:
                    index += 1
                else:
                    quote = None
        elif pair == '--':
            line_comment = True
            index += 1
        elif pair == '/*':
            block_depth = 1
            index += 1
        elif char in "\"'":
            quote = char
            escaped = char == "'" and index > 0 and sql[index - 1] in 'Ee' and (
                index == 1 or not (sql[index - 2].isalnum() or sql[index - 2] == '_'))
        elif char == '$':
            match = re.match(r'\$(?:[A-Za-z_][A-Za-z_0-9]*)?\$', sql[index:])
            if match and (index == 0 or not (sql[index - 1].isalnum() or sql[index - 1] in '_$')):
                dollar = match.group()
                index += len(dollar) - 1
        elif char == ';':
            pieces.append(sql[start:index + 1])
            start = index + 1
        index += 1
    if sql[start:].strip():
        pieces.append(sql[start:])
    if quote or dollar or block_depth:
        raise ValueError('Unterminated SQL string or block comment')
    return pieces


class DatabaseTestSession:
    def __init__(self):
        self.process = None
        self.errors = tempfile.TemporaryFile()
        self.lock = threading.Lock()

    def __enter__(self):
        target = database_target()
        command = container_command(['python3', '-u', '-c', SERVER, *([target['socket']] if target else [])])
        try:
            self.process = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, stderr=self.errors)
            if self._read(30) != {'ready': True}:
                raise RuntimeError('Database test session did not verify its target')
            return self
        except BaseException:
            self.close()
            raise

    def _read(self, timeout):
        with selectors.DefaultSelector() as selector:
            selector.register(self.process.stdout, selectors.EVENT_READ)
            if not selector.select(timeout):
                raise subprocess.TimeoutExpired('guarded database test session', timeout)
            line = self.process.stdout.readline()
        if not line:
            raise RuntimeError('Database test session ended unexpectedly')
        result = json.loads(line)
        if result.get('transport_error'):
            raise RuntimeError(result['transport_error'])
        return result

    def run(self, command, *, input, timeout=30, **unused):
        # This transport is deliberately unavailable for commits, psql commands
        # and the reconnect test. Those retain the original subprocess boundary.
        if re.search(r'\bCOMMIT\b', input, re.I) or re.search(r'^\s*\\', input, re.M):
            raise ValueError('Persistent test transport only accepts rollback-only SQL')
        sql = input.lstrip()
        if sql.startswith('SELECT'):
            sql = 'BEGIN READ ONLY;\n' + sql + '\nROLLBACK;'
        elif not sql.startswith('BEGIN;'):
            raise ValueError('Experiment must begin an explicit transaction')
        with self.lock:
            try:
                self.process.stdin.write((json.dumps({'statements': split_sql(sql)}) + '\n').encode())
                self.process.stdin.flush()
                result = self._read(timeout)
                return subprocess.CompletedProcess(command, result['exit'], result['stdout'], result['stderr'])
            except BaseException:
                self.close()
                raise

    def close(self):
        if self.process is not None:
            self.process.stdin.close()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.terminate()
                try:
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait()
            self.process.stdout.close()
            self.process = None
        self.errors.close()

    def __exit__(self, *error):
        self.close()
