"""Independent physical database copies for concurrent, unchanged fault audits.

Copies run in individually capped, network-isolated temporary containers.
The runtime image is content-verified and cached; database backups are fresh.
Copies retain fsync/WAL and use private data directories and Unix sockets.
The source database and its volume are never stopped or removed.
"""
import json
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import uuid

LANES=('sql','lifecycle','migration','sql-second')

RUNTIME_FUNCTION = r'''
import hashlib,json,os,pathlib,stat,sys
def runtime_digest(entries):
 digest=hashlib.sha256()
 for entry in entries:
  change,path=entry
  digest.update(json.dumps(entry).encode())
  if change=='D':
   if os.path.lexists(path):raise RuntimeError('Deleted runtime path reappeared')
   continue
  info=os.lstat(path)
  digest.update(str((info.st_mode,info.st_uid,info.st_gid)).encode())
  if stat.S_ISLNK(info.st_mode):digest.update(os.readlink(path).encode())
  elif stat.S_ISREG(info.st_mode):
   with open(path,'rb') as source:
    for part in iter(lambda:source.read(1024*1024),b''):digest.update(part)
 return digest.hexdigest()
'''

BACKUP = r'''
import fcntl,json,pathlib,platform,re,shutil,signal,subprocess,sys,time
root=pathlib.Path(sys.argv[1]);root.mkdir(mode=0o700)
kernel=tuple(map(int,re.match(r'(\d+)\.(\d+)',platform.release()).groups()))
if platform.system()!='Linux' or kernel<(5,8):raise RuntimeError('syncfs requires Linux 5.8 or newer')
lock=(root/'owner.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX)
def run(args):
 if (root/'cancel').exists():raise RuntimeError('Sandbox startup cancelled')
 p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 started=time.monotonic()
 try:
  while True:
   try:output,errors=p.communicate(timeout=.1);break
   except subprocess.TimeoutExpired:
    if (root/'cancel').exists() or time.monotonic()-started>45:
     p.send_signal(signal.SIGINT)
     try:p.communicate(timeout=5)
     except subprocess.TimeoutExpired:p.kill();p.communicate()
     raise RuntimeError('Sandbox command cancelled or timed out')
  if p.returncode:raise RuntimeError('Sandbox command failed: '+args[0])
  return output
 finally:
  if p.poll() is None:p.kill();p.wait()
started=time.monotonic()
run(['pg_basebackup','-U','merlin_d6','-D',str(root/'base'),'-X','fetch','-c','fast','--sync-method=syncfs'])
run(['pg_verifybackup',str(root/'base')])
print(json.dumps({'backup_seconds':time.monotonic()-started}),flush=True)
'''

LAUNCH = RUNTIME_FUNCTION + r'''
import pwd,subprocess
entries=json.loads(pathlib.Path('/tmp/merlin-runtime-entries.json').read_text())
if runtime_digest(entries)!=sys.argv[3]:raise RuntimeError('Runtime cache differs from the verified source')
root=pathlib.Path(sys.argv[1]);root.mkdir(mode=0o700,exist_ok=True)
if root.is_symlink() or str(root.resolve())!=str(root):raise RuntimeError('Copy root redirects')
os.chmod(root,0o700)
data=root/sys.argv[2]
if not data.is_dir() or any(data.iterdir()):raise RuntimeError('Copy volume is not empty')
os.chmod(data,0o700)
subprocess.run(['tar','-xzf','/tmp/merlin-base.tar.gz','-C',str(data),'--strip-components=1'],check=True)
os.chmod(data,0o700)
socket=data/'socket';socket.mkdir(mode=0o700)
owner=pwd.getpwnam('postgres')
os.chown(root,owner.pw_uid,owner.pw_gid)
for directory,dirs,files in os.walk(data):
 os.chown(directory,owner.pw_uid,owner.pw_gid)
 for name in files:os.chown(os.path.join(directory,name),owner.pw_uid,owner.pw_gid)
os.execvp('runuser',['runuser','-u','postgres','--','postgres','-D',str(data),'-k',str(socket),'-c','listen_addresses=','-c','shared_buffers=32MB','-c','recovery_init_sync_method=syncfs'])
'''

CLEAN = r'''
import fcntl,pathlib,re,shutil,subprocess,sys,time
root=pathlib.Path(sys.argv[1])
if not re.fullmatch(r'/tmp/merlin-db-sandboxes-[0-9a-f]{32}',str(root)):raise RuntimeError('Unsafe cleanup root')
if root.is_symlink():raise RuntimeError('Sandbox root became a symlink')
if root.exists():
 (root/'cancel').touch()
 lock=(root/'owner.lock').open('a');deadline=time.monotonic()+15
 while True:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
  except BlockingIOError:
   if time.monotonic()>deadline:raise RuntimeError('Startup cancellation did not finish; retain files')
   time.sleep(.05)
 for name in ['sql','lifecycle','migration','sql-second']:
  data=root/name
  if data.is_symlink():raise RuntimeError('Sandbox data became a symlink')
  if (data/'postmaster.pid').exists():
   if (data/'postmaster.pid').read_text().splitlines()[1]!=str(data):raise RuntimeError('Unexpected postmaster data identity')
   result=subprocess.run(['pg_ctl','-D',str(data),'-m','immediate','-t','10','stop'],capture_output=True,timeout=15)
   if result.returncode:raise RuntimeError('Sandbox shutdown failed; retain files')
 shutil.rmtree(root)
print('Sandbox processes stopped and temporary copies removed')
'''


def validate_manifest(data):
    """Reject source paths, path traversal, other clusters and forged shapes."""
    if set(data) != {'source', 'container', 'root', 'name', 'data', 'socket', 'fingerprint'}:
        raise RuntimeError('Unexpected sandbox manifest fields')
    if not re.fullmatch(r'[0-9a-f]{64}', data['source']):
        raise RuntimeError('Invalid sandbox container identity')
    if not re.fullmatch(r'[0-9a-f]{64}', data['container']) or data['container']==data['source']:
        raise RuntimeError('Sandbox must have an independent container')
    if not re.fullmatch(r'/tmp/merlin-db-sandboxes-[0-9a-f]{32}', data['root']):
        raise RuntimeError('Invalid sandbox root')
    if data['name'] not in LANES:
        raise RuntimeError('Invalid sandbox lane')
    if data['data'] != data['root'] + '/' + data['name'] or data['socket'] != data['data'] + '/socket':
        raise RuntimeError('Sandbox paths are not independent temporary storage')
    if not re.fullmatch(r'[0-9a-f]{32}', data['fingerprint']):
        raise RuntimeError('Invalid sandbox schema fingerprint')
    return data


def volume_name(root, name):
    if not re.fullmatch(r'/tmp/merlin-db-sandboxes-[0-9a-f]{32}',root) or name not in LANES:
        raise RuntimeError('Invalid disposable volume identity')
    return 'merlin-audit-'+root.rsplit('-',1)[1]+'-'+name


class DatabaseSandboxes:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.lanes = LANES if os.environ.get('MERLIN_SQL_SHARDS','2') == '2' else LANES[:3]
        self.root = '/tmp/merlin-db-sandboxes-' + uuid.uuid4().hex
        self.source = None
        self.image = None
        self.containers = []
        self.manifests = {}
        self.temporary = None
        self.evidence = {'status': 'PENDING', 'root': self.root}

    def command(self, script, *args):
        return ['docker', 'exec', '-u', 'postgres', '-i', self.source,
                'python3', '-u', '-c', script, *args]

    def source_fingerprint(self):
        from tools.audit_database_cases import FINGERPRINT
        query = "SELECT current_database(),system_identifier FROM pg_control_system();SELECT (SELECT count(*) FROM public.users),(SELECT count(*) FROM public.notes);SELECT count(*) FROM pg_tablespace WHERE spcname NOT IN ('pg_default','pg_global');" + FINGERPRINT
        result = subprocess.run(['docker', 'exec', '-i', self.source, 'psql', '-X', '-qAt', '-U', 'merlin_d6', '-d', 'merlin_d6', '-v', 'ON_ERROR_STOP=1'],
                                input=query, text=True, capture_output=True, timeout=15)
        lines = result.stdout.splitlines()
        # Plain basebackup otherwise restores custom tablespaces at their
        # original absolute locations. Refuse them before creating any backup.
        if result.returncode or len(lines) != 4 or lines[:3] != ['merlin_d6|7694311451826794534', '0|0','0']:
            raise RuntimeError('Source preservation gate failed')
        return lines[3]

    def __enter__(self):
        from tools.database_test_session import disposable_container
        if os.environ.get('MERLIN_DB_SANDBOX'):
            raise RuntimeError('Nested sandbox creation is forbidden')
        self.source = disposable_container()
        started = time.monotonic()
        try:
            self.original = self.source_fingerprint()
            phase=time.monotonic()
            def prepare_runtime():
                started_runtime = time.monotonic()
                self.prepare_runtime()
                self.evidence['runtime_prepare_seconds'] = round(time.monotonic()-started_runtime, 3)
            def backup():
                started_backup = time.monotonic()
                result = subprocess.run(self.command(BACKUP, self.root), text=True, capture_output=True, timeout=60)
                self.evidence['backup_command_seconds'] = round(time.monotonic()-started_backup, 3)
                return result
            # Code verification and the verified fresh backup read independent
            # paths. Join both jobs before using either result or cleaning up.
            with ThreadPoolExecutor(max_workers=2) as pool:
                runtime_job = pool.submit(prepare_runtime)
                backup_job = pool.submit(backup)
                runtime_job.result()
                result = backup_job.result()
            if result.returncode:
                raise RuntimeError('Independent database startup failed')
            startup = json.loads(result.stdout)
            archive=Path(self.temporary.name)/'base.tar.gz'
            with archive.open('wb') as output:
                result=subprocess.run(['docker','exec','-u','postgres',self.source,'tar','-I','gzip -1','-cf','-','-C',self.root,'base'],stdout=output,stderr=subprocess.PIPE,timeout=20)
            if result.returncode:raise RuntimeError('Fresh backup transfer failed')
            def start_copy(name):
                volume=volume_name(self.root,name)
                created=self.docker(['volume','create','--label','merlin.audit.root='+self.root,
                                     '--label','merlin.audit.source='+self.source,volume]).strip()
                if created!=volume:raise RuntimeError('Unexpected disposable volume identity')
                identifier=self.docker(['create','--network','none','--no-healthcheck','--cpus','1','--memory','1g',
                                        *[argument for key in self.desktop_labels for argument in ('--label',key+'=')],
                                        '--tmpfs','/var/lib/postgresql/data:rw,size=1m,noexec,nosuid,nodev',
                                        '--mount','type=volume,source='+volume+',target='+self.root+'/'+name+',volume-nocopy',
                                        '--label','merlin.audit.root='+self.root,
                                        '--label','merlin.audit.source='+self.source,
                                        '--label','merlin.audit.lane='+name,
                                        '--entrypoint','python3',self.image,'-u','-c',LAUNCH,self.root,name,self.runtime_hash]).strip()
                if not re.fullmatch(r'[0-9a-f]{64}',identifier):raise RuntimeError('Invalid clone container identity')
                self.containers.append(identifier)
                self.docker(['cp',str(archive),identifier+':/tmp/merlin-base.tar.gz'])
                self.docker(['cp',str(Path(self.temporary.name)/'runtime-entries.json'),identifier+':/tmp/merlin-runtime-entries.json'])
                self.docker(['start',identifier])
                target={'name':name,'container':identifier,'data':self.root+'/'+name,'socket':self.root+'/'+name+'/socket'}
                deadline=time.monotonic()+30
                while True:
                    probe=subprocess.run(['docker','exec',target['container'],'pg_isready','-h',target['socket'],'-U','merlin_d6','-d','merlin_d6'],capture_output=True,timeout=5)
                    if probe.returncode==0:break
                    state=json.loads(self.docker(['container','inspect',identifier]))[0]['State']
                    if not state['Running']:
                        log=subprocess.run(['docker','logs','--tail','30',identifier],capture_output=True,text=True,timeout=10)
                        path=self.directory.parent/('database-startup-'+name+'.log')
                        path.write_text(log.stdout+log.stderr)
                        path.chmod(0o600)
                        raise RuntimeError('Disposable PostgreSQL startup failed; inspect '+str(path))
                    if time.monotonic()>deadline:raise RuntimeError('Clone startup timed out')
                    time.sleep(.05)
                return target
            # Each copy has separate storage and ownership labels. The executor
            # waits for all creation jobs before exception cleanup inventories
            # their resources, including any daemon-side late create result.
            with ThreadPoolExecutor(max_workers=3) as pool:
                targets=list(pool.map(start_copy,self.lanes))
            self.directory.mkdir(mode=0o700)
            for target in targets:
                data = validate_manifest(dict(target, root=self.root, source=self.source, fingerprint=self.original))
                path = self.directory / (target['name'] + '.json')
                descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                with os.fdopen(descriptor, 'w') as output:
                    json.dump(data, output)
                self.manifests[target['name']] = str(path)
            self.evidence.update(status='PASS', setup_seconds=round(time.monotonic()-started, 3), targets=targets,
                                 source_fingerprint=self.original, startup_timings=startup)
            return self
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.source is None:
            return
        started = time.monotonic()
        # Inventory by a unique per-run label also catches a daemon-side create
        # that succeeded just before its client timed out. Verify every object
        # before removal; never remove the source or any source-mounted volume.
        identifiers=self.docker(['ps','-aq','--no-trunc','--filter','label=merlin.audit.root='+self.root]).split()
        for identifier in identifiers:
            info=json.loads(self.docker(['container','inspect',identifier]))[0];labels=info['Config']['Labels']
            if info['Id']==self.source or labels.get('merlin.audit.source')!=self.source or labels.get('merlin.audit.root')!=self.root:
                raise RuntimeError('Refuse cleanup of an unowned container')
            self.docker(['rm','-f','-v',identifier])
        volumes=self.docker(['volume','ls','-q','--filter','label=merlin.audit.root='+self.root]).split()
        allowed={volume_name(self.root,name) for name in LANES}
        for volume in volumes:
            info=json.loads(self.docker(['volume','inspect',volume]))[0]
            labels=info.get('Labels') or {}
            if info['Name']!=volume or volume not in allowed or labels.get('merlin.audit.root')!=self.root or labels.get('merlin.audit.source')!=self.source:
                raise RuntimeError('Refuse cleanup of an unowned volume')
            self.docker(['volume','rm',volume])
        images=self.docker(['images','-q','--no-trunc','--filter','label=merlin.audit.root='+self.root]).split()
        for image in set(images):
            info=json.loads(self.docker(['image','inspect',image]))[0]
            if info['Config']['Labels'].get('merlin.audit.root')!=self.root:
                raise RuntimeError('Refuse removal of an unowned image')
            self.docker(['image','rm',image])
        result = subprocess.run(self.command(CLEAN, self.root), text=True, capture_output=True, timeout=45)
        self.evidence['cleanup_seconds'] = round(time.monotonic()-started, 3)
        self.evidence['cleanup_passed'] = result.returncode == 0
        if result.returncode:
            raise RuntimeError('Sandbox cleanup failed; temporary resources retained')
        if self.temporary is not None:
            self.temporary.cleanup()
            self.temporary=None
        final = self.source_fingerprint()
        self.evidence['source_preserved'] = final == getattr(self, 'original', final)
        if not self.evidence['source_preserved']:
            raise RuntimeError('Original database fingerprint changed')
        self.source = None

    def docker(self, arguments, timeout=20):
        started=time.monotonic()
        result=subprocess.run(['docker',*arguments],capture_output=True,text=True,timeout=timeout)
        self.evidence.setdefault('docker_operation_seconds',[]).append({'operation':arguments[0],'seconds':round(time.monotonic()-started,3)})
        if result.returncode:raise RuntimeError('Disposable Docker operation failed: '+arguments[0])
        return result.stdout

    def prepare_runtime(self):
        """Cache dependency code only; verify content in the source and each clone."""
        helper=['docker','exec','-i',self.source,'python3','-c',RUNTIME_FUNCTION]
        entries=[]
        for line in self.docker(['diff',self.source]).splitlines():
            change,path=line.split(' ',1)
            if any(path==prefix or path.startswith(prefix+'/') for prefix in
                   ['/tmp','/run','/var/run','/var/log','/var/cache','/var/lib/postgresql/data']):
                continue
            entries.append([change,path])
        entries.sort()
        result=subprocess.run(helper[:-1]+[RUNTIME_FUNCTION+"print(runtime_digest(json.load(sys.stdin)))"],
                              input=json.dumps(entries),capture_output=True,text=True,timeout=30)
        self.runtime_hash=result.stdout.strip()
        if result.returncode or not re.fullmatch(r'[0-9a-f]{64}',self.runtime_hash):
            raise RuntimeError('Runtime content verification failed')
        if not entries:
            # With no persistent runtime changes, the immutable source image is
            # already the exact runtime. Avoid committing the unchanged
            # container; this saves work without caching or changing storage.
            source_info=json.loads(self.docker(['container','inspect',self.source]))[0]
            self.image=source_info['Image']
            if not re.fullmatch(r'sha256:[0-9a-f]{64}',self.image):
                raise RuntimeError('Source image identity is invalid')
            info=json.loads(self.docker(['image','inspect',self.image]))[0]
            self.evidence.update(runtime_cache_hit=False,
                                 runtime_reuse='verified-unchanged-source-image')
        else:
            tag='merlin-test-runtime:'+self.source[:16]+'-'+self.runtime_hash
            cached=subprocess.run(['docker','image','inspect',tag],capture_output=True,text=True,timeout=10)
            self.evidence['runtime_cache_hit']=cached.returncode==0
            if cached.returncode==0:
                info=json.loads(cached.stdout)[0];self.image=info['Id'];labels=info['Config']['Labels']
                if labels.get('merlin.audit.runtime')!=self.runtime_hash or labels.get('merlin.audit.source')!=self.source:
                    raise RuntimeError('Runtime cache provenance differs')
            else:
                # Capture overlaps native transport checks on the live source.
                # Never pause it; Docker renamed this option between CLI versions.
                help_text=self.docker(['commit','--help'])
                if re.search(r'(?m)^\s+--no-pause\b',help_text):
                    pause_option='--no-pause'
                elif re.search(r'(?m)^\s+(?:-p,\s+)?--pause\b',help_text):
                    pause_option='--pause=false'
                else:
                    raise RuntimeError('Docker commit has no supported non-pausing option')
                commit=self.docker(['commit',pause_option,
                                   '--change','ENV POSTGRES_PASSWORD=unused_for_existing_copy',
                                   '--change','LABEL com.docker.compose.project=merlin-audit-runtime',
                                   '--change','LABEL com.docker.compose.service=postgres-sandbox',
                                   '--change','LABEL merlin.audit.runtime='+self.runtime_hash,
                                   '--change','LABEL merlin.audit.source='+self.source,self.source,tag],timeout=45)
                matches=re.findall(r'sha256:[0-9a-f]{64}',commit)
                if len(matches)!=1:raise RuntimeError('Invalid captured runtime identity')
                self.image=matches[0]
                info=json.loads(self.docker(['image','inspect',self.image]))[0]
        self.evidence.update(runtime_image=self.image,runtime_digest=self.runtime_hash)
        # A committed Desktop container inherits its WSL port-forwarding labels.
        # They describe the original service, not these unpublished Unix-socket
        # copies. Desktop otherwise waits about three seconds on every inspect
        # and exec while resolving the stale forwarding metadata.
        # A cache hit already inspected this exact immutable image ID.
        labels=info['Config'].get('Labels') or {}
        self.desktop_labels=tuple(key for key in labels if key.startswith('desktop.docker.io/'))
        self.temporary=tempfile.TemporaryDirectory(prefix='merlin-db-transfer-')
        (Path(self.temporary.name)/'runtime-entries.json').write_text(json.dumps(entries))

    def __exit__(self, *unused):
        self.close()
