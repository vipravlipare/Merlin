"""Own one fresh, unpublished CI database; never reuse local application storage."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import uuid


PROTECTED_CLUSTERS = {'7694311451826794534', '7691749973399031842'}


def verify_metadata(info, volume, *, source, image, nonce):
    """Pure ownership/isolation gate, shared with synthetic counterfactual checks."""
    project = "merlin-ci-" + nonce
    volume_name = project + "-data"
    config_hash = hashlib.sha256((image + project).encode()).hexdigest()
    host = info['HostConfig']
    labels = info['Config'].get('Labels') or {}
    if (info['Id'] != source or info['Image'] != image
            or not info['State']['Running']
            or labels.get('merlin.ci.owner') != nonce
            or labels.get('com.docker.compose.project') != project
            or labels.get('com.docker.compose.service') != 'postgres'
            or labels.get('com.docker.compose.config-hash') != config_hash
            or labels.get('com.docker.compose.oneoff') != 'False'
            or host['NetworkMode'] != 'none'
            or host['NanoCpus'] != 1000000000 or host['Memory'] != 1073741824
            or host.get('Privileged') or host.get('Binds')
            or host.get('VolumesFrom') or host.get('Devices') or host.get('CapAdd')):
        raise RuntimeError('CI container ownership or isolation differs')
    if (any((host.get('PortBindings') or {}).values())
            or any(info['NetworkSettings'].get('Ports', {}).values())
            or any(value for key, value in labels.items()
                   if key.startswith('desktop.docker.io/ports/'))):
        raise RuntimeError('CI source must not publish ports')
    mounts = info['Mounts']
    if (len(mounts) != 1 or mounts[0]['Type'] != 'volume'
            or mounts[0]['Name'] != volume_name or mounts[0]['RW'] is not True
            or mounts[0]['Destination'] != '/var/lib/postgresql/data'):
        raise RuntimeError('CI source must use exactly its own data volume')
    if (volume["Name"] != volume_name or volume["Driver"] != "local"
            or volume.get("Options")
            or (volume.get("Labels") or {}).get("merlin.ci.owner") != nonce):
        raise RuntimeError("Refusing unowned or redirected CI volume")
    return info


class CiDatabase:
    def __init__(self, image, nonce=None):
        if not re.fullmatch(r'sha256:[0-9a-f]{64}', image):
            raise ValueError('CI runtime must be an immutable Docker image ID')
        self.nonce = nonce if nonce is not None else uuid.uuid4().hex
        if not re.fullmatch(r'[0-9a-f]{32}', self.nonce):
            raise ValueError('Invalid CI ownership nonce')
        self.image = image
        self.project = 'merlin-ci-' + self.nonce
        self.volume = self.project + '-data'
        self.source = self.cluster = None
        self.cleanup_passed = False

    def _docker(self, arguments, *, input=None, timeout=30):
        try:
            result = subprocess.run(['docker', *arguments], input=input,
                                    capture_output=True, text=True, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired):
            raise RuntimeError('CI Docker operation unavailable or timed out') from None
        if result.returncode:
            # Docker errors may include configuration or private daemon details.
            raise RuntimeError('CI Docker operation failed: ' + arguments[0])
        return result.stdout

    def _volume(self):
        rows = json.loads(self._docker(['volume', 'inspect', self.volume]))
        if len(rows) != 1:
            raise RuntimeError('Ambiguous CI volume')
        volume = rows[0]
        if (volume['Name'] != self.volume or volume['Driver'] != 'local'
                or volume.get('Options')
                or (volume.get('Labels') or {}).get('merlin.ci.owner') != self.nonce):
            raise RuntimeError('Refusing unowned or redirected CI volume')
        return volume

    def verify(self):
        """Verify isolation and ownership immediately before every container exec."""
        if not self.source or not re.fullmatch(r'[0-9a-f]{64}', self.source):
            raise RuntimeError('CI container has not been created')
        rows = json.loads(self._docker(['container', 'inspect', self.source]))
        if len(rows) != 1:
            raise RuntimeError('Ambiguous CI container')
        info = rows[0]
        verify_metadata(info, self._volume(), source=self.source, image=self.image, nonce=self.nonce)
        return info

    def command(self, arguments):
        self.verify()
        return ['docker', 'exec', '-i', self.source, *arguments]

    def _psql(self, sql, *, single_transaction=False):
        arguments = ['psql', '-X', '-qAt', '-U', 'merlin_d6', '-d', 'merlin_d6',
                     '-v', 'ON_ERROR_STOP=1']
        if single_transaction:
            arguments.append('--single-transaction')
        command = self.command(arguments)
        return self._docker(command[1:], input=sql, timeout=60).strip()

    def query(self, sql, *, single_transaction=False):
        if not self.cluster:
            raise RuntimeError('CI cluster has not been identified')
        gate = ("DO $ci_identity$ BEGIN IF current_database()<>'merlin_d6' OR "
                "(SELECT system_identifier::text FROM pg_control_system())<>'" + self.cluster +
                "' THEN RAISE EXCEPTION 'CI database identity changed'; END IF; END $ci_identity$;\n")
        return self._psql(gate + sql, single_transaction=single_transaction)

    def bootstrap(self, directory):
        """Apply reviewed migration inputs only after the caller renders CI identity."""
        directory = Path(directory)
        self.query('CREATE EXTENSION plpython3u;')
        self.query((directory / 'migrations/001_users_notes.up.sql').read_text(),
                   single_transaction=True)
        self.query((directory / 'migrations/002_whitespace_parity.up.sql').read_text())
        self.query((directory / 'migrations/003_auth_foundation.up.sql').read_text())
        if self.query('SELECT (SELECT count(*) FROM public.users),(SELECT count(*) FROM public.notes),'
                      '(SELECT count(*) FROM public.auth_credentials),'
                      '(SELECT count(*) FROM public.auth_refresh_families),'
                      '(SELECT count(*) FROM public.auth_refresh_tokens);') != '0|0|0|0|0':
            raise RuntimeError('CI bootstrap did not leave empty application tables')

    def __enter__(self):
        label = 'merlin.ci.owner=' + self.nonce
        # Never adopt a nonce that already owns resources from another process.
        if (self._docker(['ps', '-aq', '--filter', 'label=' + label]).strip()
                or self._docker(['volume', 'ls', '-q', '--filter', 'label=' + label]).strip()):
            raise RuntimeError('CI ownership nonce is already in use')
        try:
            created = self._docker(['volume', 'create', '--label', label, self.volume]).strip()
            if created != self.volume:
                raise RuntimeError('Unexpected CI volume identity')
            self._volume()
            self.source = self._docker([
                'create', '--name', self.project, '--network', 'none', '--cpus', '1', '--memory', '1g',
                '--label', label, '--label', 'com.docker.compose.project=' + self.project,
                '--label', 'com.docker.compose.service=postgres',
                '--label', 'com.docker.compose.config-hash=' + hashlib.sha256(
                    (self.image + self.project).encode()).hexdigest(),
                '--label', 'com.docker.compose.oneoff=False',
                '--mount', 'type=volume,source=' + self.volume + ',target=/var/lib/postgresql/data,volume-nocopy',
                '-e', 'POSTGRES_USER=merlin_d6', '-e', 'POSTGRES_DB=merlin_d6',
                '-e', 'POSTGRES_HOST_AUTH_METHOD=trust', self.image,
                'postgres', '-c', 'listen_addresses=', '-c', 'fsync=on',
                '-c', 'full_page_writes=on', '-c', 'synchronous_commit=on']).strip()
            if not re.fullmatch(r'[0-9a-f]{64}', self.source):
                raise RuntimeError('Unexpected CI container identity')
            self._docker(['start', self.source])
            deadline = time.monotonic() + 45
            while True:
                self.verify()
                if self._docker(['exec', self.source, 'cat', '/proc/1/comm']).strip() != 'postgres':
                    if time.monotonic() >= deadline:
                        raise RuntimeError('CI database entry point did not finish initialization')
                    time.sleep(.2)
                    continue
                try:
                    observed = self._psql("SELECT current_database(),current_user,system_identifier,current_setting('server_version_num'),current_setting('listen_addresses'),current_setting('fsync'),current_setting('full_page_writes'),current_setting('synchronous_commit') FROM pg_control_system();")
                except RuntimeError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError('CI database startup timed out') from None
                    time.sleep(.2)
                    continue
                values = observed.split('|')
                if (len(values) != 8 or values[:2] != ['merlin_d6', 'merlin_d6']
                        or not re.fullmatch(r'[0-9]{1,20}', values[2])
                        or values[2] in PROTECTED_CLUSTERS
                        or values[3:] != ['170011', '', 'on', 'on', 'on']):
                    raise RuntimeError('Unexpected CI PostgreSQL identity or durability')
                self.cluster = values[2]
                if self.query("SELECT to_regclass('public.users') IS NULL AND to_regclass('public.notes') IS NULL;") != 't':
                    raise RuntimeError('CI database is not fresh')
                return self
        except BaseException:
            self.close()
            raise

    def close(self):
        """Inventory by unique ownership to catch daemon-side partial creates."""
        self.cleanup_passed = False
        label = 'label=merlin.ci.owner=' + self.nonce
        # Runtime commits inherit the CI owner label. Their audit copies use
        # a different Compose project and must be handled as descendants.
        identifiers = self._docker(['ps', '-aq', '--no-trunc', '--filter', label,
                                    '--filter', 'label=com.docker.compose.project=' + self.project]).split()
        for identifier in identifiers:
            rows = json.loads(self._docker(['container', 'inspect', identifier]))
            if (len(rows) != 1 or rows[0]['Id'] != identifier
                    or rows[0]['Image'] != self.image
                    or (rows[0]['Config'].get('Labels') or {}).get('merlin.ci.owner') != self.nonce
                    or rows[0]['Name'] != '/' + self.project):
                raise RuntimeError('Refusing cleanup of an unowned CI container')
            # A cancelled child may not finish its own finally block. Only
            # descendants of this independently owned CI source may be removed.
            verify_metadata(dict(rows[0], State={'Running': True}), self._volume(),
                            source=identifier, image=self.image, nonce=self.nonce)
            self._close_descendants(identifier)
            self._docker(['rm', '-f', '-v', identifier])
        volumes = self._docker(['volume', 'ls', '-q', '--filter', label]).split()
        for volume in volumes:
            if volume != self.volume:
                raise RuntimeError('Refusing cleanup of an unexpected CI volume')
            self._volume()
            self._docker(['volume', 'rm', volume])
        self.source = None
        self.cleanup_passed = True

    def _close_descendants(self, source):
        from tools.database_sandboxes import LANES, validate_manifest, volume_name

        selector = 'label=merlin.audit.source=' + source
        identifiers = self._docker(['ps', '-aq', '--no-trunc', '--filter', selector]).split()
        for identifier in identifiers:
            rows = json.loads(self._docker(['container', 'inspect', identifier]))
            if len(rows) != 1:
                raise RuntimeError('Ambiguous CI descendant')
            info = rows[0]
            labels = info['Config'].get('Labels') or {}
            root, lane = labels.get('merlin.audit.root'), labels.get('merlin.audit.lane')
            if (info['Id'] != identifier or identifier == source
                    or labels.get('merlin.audit.source') != source):
                raise RuntimeError('Refusing unowned CI descendant')
            target = validate_manifest({'source': source, 'container': identifier,
                                        'root': root, 'name': lane,
                                        'data': str(root) + '/' + str(lane),
                                        'socket': str(root) + '/' + str(lane) + '/socket',
                                        'fingerprint': '0' * 32})
            host = info['HostConfig']
            if (host['NetworkMode'] != 'none' or host['NanoCpus'] != 1000000000
                    or host['Memory'] != 1073741824 or host.get('Privileged')
                    or host.get('Binds') or host.get('VolumesFrom') or host.get('Devices')
                    or host.get('CapAdd') or any((host.get('PortBindings') or {}).values())
                    or any(info['NetworkSettings'].get('Ports', {}).values())):
                raise RuntimeError('CI descendant isolation differs; retain resources')
            mounts = info['Mounts']
            owned = [mount for mount in mounts if mount['Type'] == 'volume'
                     and mount['Name'] == volume_name(root, lane)
                     and mount['Destination'] == target['data'] and mount['RW'] is True]
            if len(owned) != 1 or any(mount not in owned and not (
                    mount['Type'] == 'tmpfs' and mount['Destination'] == '/var/lib/postgresql/data')
                    for mount in mounts):
                raise RuntimeError('CI descendant uses shared storage; retain resources')
            self._docker(['rm', '-f', '-v', identifier])
        volumes = self._docker(['volume', 'ls', '-q', '--filter', selector]).split()
        for name in volumes:
            rows = json.loads(self._docker(['volume', 'inspect', name]))
            if len(rows) != 1:
                raise RuntimeError('Ambiguous CI descendant volume')
            info = rows[0]
            labels = info.get('Labels') or {}
            root = labels.get('merlin.audit.root', '')
            allowed = {volume_name(root, lane) for lane in LANES}
            if (info['Name'] != name or name not in allowed or info['Driver'] != 'local'
                    or info.get('Options') or labels.get('merlin.audit.source') != source):
                raise RuntimeError('Refusing unowned CI descendant volume')
            self._docker(['volume', 'rm', name])
        images = self._docker(['images', '-q', '--no-trunc', '--filter', selector]).split()
        for image in set(images):
            rows = json.loads(self._docker(['image', 'inspect', image]))
            labels = rows[0]['Config'].get('Labels') or {} if len(rows) == 1 else {}
            if (len(rows) != 1 or rows[0]['Id'] != image or image == self.image
                    or labels.get('merlin.audit.source') != source
                    or not re.fullmatch(r'[0-9a-f]{64}', labels.get('merlin.audit.runtime', ''))):
                raise RuntimeError('Refusing unowned CI runtime cache')
            self._docker(['image', 'rm', image])

    def __exit__(self, *unused):
        self.close()


def self_check():
    """Counterfactuals exercise the same metadata gate used before every exec."""
    from copy import deepcopy
    from unittest.mock import patch

    image, nonce, source = 'sha256:' + '1' * 64, '2' * 32, '3' * 64
    database = CiDatabase(image, nonce)
    volume = {'Name': database.volume, 'Driver': 'local', 'Options': None,
              'Labels': {'merlin.ci.owner': nonce}}
    info = {'Id': source, 'Image': image, 'State': {'Running': True},
            'Config': {'Labels': {'merlin.ci.owner': nonce,
                                 'com.docker.compose.project': database.project,
                                 'com.docker.compose.service': 'postgres',
                                 'com.docker.compose.config-hash': hashlib.sha256(
                                     (image + database.project).encode()).hexdigest(),
                                 'com.docker.compose.oneoff': 'False'}},
            'HostConfig': {'NetworkMode': 'none', 'NanoCpus': 1000000000,
                           'Memory': 1073741824, 'PortBindings': {}},
            'NetworkSettings': {'Ports': {}},
            'Mounts': [{'Type': 'volume', 'Name': database.volume,
                        'RW': True, 'Destination': '/var/lib/postgresql/data'}]}
    verify_metadata(info, volume, source=source, image=image, nonce=nonce)
    rows = [{'scenario': 'ci-source-valid-owned-metadata', 'passed': True}]
    variants = [
        ('network', lambda i, v: i['HostConfig'].update(NetworkMode='host')),
        ('cpu', lambda i, v: i['HostConfig'].update(NanoCpus=0)),
        ('memory', lambda i, v: i['HostConfig'].update(Memory=0)),
        ('privileged', lambda i, v: i['HostConfig'].update(Privileged=True)),
        ('bind-mount', lambda i, v: i['HostConfig'].update(Binds=['/private:/private'])),
        ('volumes-from', lambda i, v: i['HostConfig'].update(VolumesFrom=['other'])),
        ('device', lambda i, v: i['HostConfig'].update(Devices=[{'PathOnHost': '/dev/example'}])),
        ('capability', lambda i, v: i['HostConfig'].update(CapAdd=['SYS_ADMIN'])),
        ('shared-mount', lambda i, v: i['Mounts'][0].update(Name='preserved-local-storage')),
        ('read-only-data', lambda i, v: i['Mounts'][0].update(RW=False)),
        ('data-destination', lambda i, v: i['Mounts'][0].update(Destination='/other')),
        ('source-id', lambda i, v: i.update(Id='4' * 64)),
        ('image', lambda i, v: i.update(Image='sha256:' + '4' * 64)),
        ('container-owner', lambda i, v: i['Config']['Labels'].update({'merlin.ci.owner': '4' * 32})),
        ('volume-owner', lambda i, v: v['Labels'].update({'merlin.ci.owner': '4' * 32})),
        ('volume-driver', lambda i, v: v.update(Driver='remote')),
        ('volume-options', lambda i, v: v.update(Options={'device': '/private'})),
        ('ports', lambda i, v: i['HostConfig'].update(PortBindings={'5432/tcp': [{'HostPort': '5432'}]})),
        ('network-ports', lambda i, v: i['NetworkSettings'].update(Ports={'5432/tcp': [{'HostPort': '5432'}]})),
        ('desktop-forwarding', lambda i, v: i['Config']['Labels'].update({'desktop.docker.io/ports/5432/tcp': '127.0.0.1:5432'})),
        ('compose-config', lambda i, v: i['Config']['Labels'].pop('com.docker.compose.config-hash')),
        ('compose-oneoff', lambda i, v: i['Config']['Labels'].update({'com.docker.compose.oneoff': 'True'})),
    ]
    for name, change in variants:
        altered, storage = deepcopy(info), deepcopy(volume)
        change(altered, storage)
        try:
            verify_metadata(altered, storage, source=source, image=image, nonce=nonce)
        except RuntimeError:
            rows.append({'scenario': 'ci-source-refuses-' + name, 'passed': True})
        else:
            raise AssertionError('CI metadata gate admitted ' + name)
    def empty_inventory(arguments, **unused):
        if arguments[:2] == ['ps', '-aq']:
            assert arguments[-2:] == ['--filter', 'label=com.docker.compose.project=' + database.project]
        else:
            assert arguments[:3] == ['volume', 'ls', '-q']
        return ''
    with patch.object(database, '_docker', side_effect=empty_inventory):
        database.close()
    assert database.cleanup_passed
    rows.append({'scenario': 'ci-cleanup-source-project-filter', 'passed': True})
    occupied = CiDatabase(image, '4' * 32)
    with patch.object(occupied, '_docker', return_value='existing-owner') as calls:
        try:
            occupied.__enter__()
        except RuntimeError:
            assert calls.call_count == 1 and calls.call_args.args[0][:2] == ['ps', '-aq']
        else:
            raise AssertionError('Occupied nonce was reused')
    rows.append({'scenario': 'ci-source-occupied-nonce-refused-before-create', 'passed': True})

    partial = CiDatabase(image, '5' * 32)
    storage = dict(volume, Name=partial.volume, Labels={'merlin.ci.owner': partial.nonce})
    live = []
    def partial_failure(arguments, **unused):
        if arguments[:2] == ['ps', '-aq']:
            return ''
        if arguments[:3] == ['volume', 'ls', '-q']:
            return '\n'.join(live)
        if arguments[:2] == ['volume', 'create']:
            live.append(partial.volume)
            return partial.volume
        if arguments[:2] == ['volume', 'inspect']:
            return json.dumps([storage])
        if arguments[0] == 'create':
            raise RuntimeError('Synthetic create failure')
        if arguments[:2] == ['volume', 'rm']:
            assert arguments[2] == partial.volume
            live.remove(partial.volume)
            return ''
        raise AssertionError('Unexpected partial-create operation')
    with patch.object(partial, '_docker', side_effect=partial_failure):
        try:
            partial.__enter__()
        except RuntimeError as error:
            assert str(error) == 'Synthetic create failure'
        else:
            raise AssertionError('Failed create succeeded')
    assert not live and partial.cleanup_passed
    rows.append({'scenario': 'ci-source-partial-create-cleans-owned-volume', 'passed': True})

    root, child, cache = '/tmp/merlin-db-sandboxes-' + '6' * 32, '7' * 64, 'sha256:' + '8' * 64
    child_volume = 'merlin-audit-' + '6' * 32 + '-sql'
    descendant = {'Id': child,
                  'Config': {'Labels': {'merlin.audit.root': root, 'merlin.audit.lane': 'sql',
                                        'merlin.audit.source': source}},
                  'HostConfig': {'NetworkMode': 'none', 'NanoCpus': 1000000000, 'Memory': 1073741824},
                  'NetworkSettings': {'Ports': {}},
                  'Mounts': [{'Type': 'volume', 'Name': child_volume, 'Destination': root + '/sql', 'RW': True},
                             {'Type': 'tmpfs', 'Destination': '/var/lib/postgresql/data'}]}
    child_storage = {'Name': child_volume, 'Driver': 'local', 'Options': None,
                     'Labels': {'merlin.audit.root': root, 'merlin.audit.source': source}}
    cached = {'Id': cache, 'Config': {'Labels': {'merlin.audit.source': source,
                                               'merlin.audit.runtime': '9' * 64}}}
    operations = []
    def descendant_inventory(arguments, **unused):
        operations.append(arguments)
        if arguments[:2] == ['ps', '-aq']:
            return child
        if arguments[:2] == ['container', 'inspect']:
            return json.dumps([descendant])
        if arguments[:3] == ['volume', 'ls', '-q']:
            return child_volume
        if arguments[:2] == ['volume', 'inspect']:
            return json.dumps([child_storage])
        if arguments[:2] == ['images', '-q']:
            return cache
        if arguments[:2] == ['image', 'inspect']:
            return json.dumps([cached])
        assert arguments in [['rm', '-f', '-v', child], ['volume', 'rm', child_volume], ['image', 'rm', cache]]
        return ''
    with patch.object(database, '_docker', side_effect=descendant_inventory):
        database._close_descendants(source)
        assert [call for call in operations if call[0] == 'rm' or call[:2] in [['volume', 'rm'], ['image', 'rm']]] == [
            ['rm', '-f', '-v', child], ['volume', 'rm', child_volume], ['image', 'rm', cache]]
        rows.append({'scenario': 'ci-cleanup-owned-descendants-volume-cache', 'passed': True})
        operations.clear()
        descendant['Mounts'][0]['Name'] = 'preserved-local-storage'
        try:
            database._close_descendants(source)
        except RuntimeError:
            assert not any(call[0] == 'rm' for call in operations)
        else:
            raise AssertionError('Shared storage was admitted for cleanup')
    rows.append({'scenario': 'ci-cleanup-shared-source-storage-refused-before-remove', 'passed': True})
    return rows
