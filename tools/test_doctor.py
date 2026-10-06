"""Regression checks for private output and meaningful authentication proof."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import doctor


class DoctorTests(unittest.TestCase):
    def result(self, code=0, out='', err=''):
        return subprocess.CompletedProcess([], code, out, err)

    def test_command_errors_are_captured_and_not_relayed(self):
        with tempfile.TemporaryDirectory() as directory:
            output = io.StringIO()
            with patch('doctor.subprocess.run', return_value=self.result(1, 'password=secret', 'secret')) as called:
                with contextlib.redirect_stdout(output):
                    result = doctor.run(['example'], Path(directory))
            self.assertEqual(result.returncode, 1)
            self.assertEqual(output.getvalue(), '')
            self.assertTrue(called.call_args.kwargs['capture_output'])
            self.assertEqual(called.call_args.kwargs['cwd'], Path(directory))

    def test_timeout_does_not_print_partial_secret(self):
        output = io.StringIO()
        with patch('doctor.subprocess.run', side_effect=subprocess.TimeoutExpired('secret', 30, output='secret')):
            with contextlib.redirect_stdout(output):
                result = doctor.run(['example'])
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('secret', output.getvalue())

    def test_wrong_password_requires_authentication_rejection(self):
        for negative, succeeds in ((self.result(2, err='connection refused secret'), False),
                                   (self.result(0, '1'), False),
                                   (self.result(2, err='FATAL: password authentication failed for secret'), True)):
            with self.subTest(negative=negative.returncode, succeeds=succeeds):
                instance = doctor.Doctor(Path('/tmp'))
                output = io.StringIO()
                with patch.object(instance, 'compose', side_effect=[self.result(0, '1'), negative, self.result(0, '123456')]):
                    with contextlib.redirect_stdout(output):
                        instance.postgres_checks()
                self.assertIn('PG-AUTH-NEGATIVE ' + ('PASS' if succeeds else 'FAIL'), output.getvalue())
                self.assertNotIn('secret', output.getvalue())

    def test_cluster_is_observed_without_assuming_original(self):
        instance = doctor.Doctor(Path('/tmp'))
        with patch.object(instance, 'compose', side_effect=[self.result(0, '1'), self.result(2, err='password authentication failed'), self.result(0, '456')]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                instance.postgres_checks()
        self.assertIn('PG-CLUSTER PASS: cluster identifier observed (456)', output.getvalue())
        self.assertEqual(instance.failures, 0)

    def test_inspect_never_requests_environment_and_rejects_malformed_data(self):
        instance = doctor.Doctor(Path('/tmp'))
        with patch.object(instance, 'command', return_value=self.result(0, 'secret invalid')) as call:
            self.assertIsNone(instance.inspect('a' * 64))
        self.assertNotIn('Config.Env', call.call_args.args[0][-2])
        self.assertNotIn('config', call.call_args.args[0])

    def test_host_auth_uses_env_and_rejects_generic_errors(self):
        for error, status in [('connection timeout secret', 'FAIL'), ('password authentication failed secret', 'PASS')]:
            instance = doctor.Doctor(Path('/tmp'))
            instance.host_ports = {'postgres': '15432', 'redis': '16379'}
            output = io.StringIO()
            with patch('doctor.shutil.which', return_value='/client'), patch.object(instance, 'compose', return_value=self.result(0, 'user\0database\0secret')):
                with patch('doctor.run', side_effect=[self.result(0, '1'), self.result(2, err=error), self.result(0, 'PONG')]) as called:
                    with contextlib.redirect_stdout(output):
                        instance.host_checks()
                    positive, negative = called.call_args_list[:2]
                    self.assertNotIn('secret', str(positive.args[0]))
                    self.assertEqual(positive.args[0][positive.args[0].index('-h') + 1], '127.0.0.1')
                    # Each subprocess receives its own environment snapshot.
                    self.assertEqual(positive.args[2]['PGPASSWORD'], 'secret')
                    self.assertEqual(negative.args[2]['PGPASSWORD'], 'secret__doctor_wrong')
            self.assertIn('HOST-PG-NEGATIVE ' + status, output.getvalue())
            self.assertNotIn('secret', output.getvalue())

    def test_static_never_invokes_runtime(self):
        instance = doctor.Doctor(Path('/tmp'), static=True)
        with patch.object(instance, 'static_checks', return_value=True), patch.object(instance, 'runtime_checks') as runtime:
            self.assertEqual(instance.execute(), 0)
        runtime.assert_not_called()

    def test_runtime_accepts_clone_project_and_alternate_loopback_port(self):
        instance = doctor.Doctor(Path('/tmp'))
        def compose(*args):
            if args[:2] == ('ps', '-q'):
                return self.result(0, 'a' * 64)
            if args[0] == 'exec' and args[-1].startswith("awk"):
                return self.result(0, '999')
            if args[-1] == 'ping':
                return self.result(0, 'PONG')
            values = {'save': '', 'appendonly': 'no', 'maxmemory': '134217728', 'maxmemory-policy': 'noeviction'}
            return self.result(0, args[-1] + '\n' + values[args[-1]] + '\n')
        infos = []
        for service, port, memory, cpus, target in [('postgres', '5432', 1073741824, 1000000000, '/var/lib/postgresql/data'), ('redis', '6379', 268435456, 500000000, '/data')]:
            infos.append(('healthy', {'PortBindings': {port + '/tcp': [{'HostIp': '127.0.0.1', 'HostPort': '15432'}]}, 'Memory': memory, 'NanoCpus': cpus, 'LogConfig': {'Type': 'json-file', 'Config': {'max-size': '10m', 'max-file': '3'}}}, [{'Destination': target, 'Type': 'volume', 'Name': 'clone42_' + service + '_data'}], {'com.docker.compose.project': 'clone42'}))
        with patch.object(instance, 'compose', side_effect=compose), patch.object(instance, 'inspect', side_effect=infos), patch.object(instance, 'postgres_checks'), patch.object(instance, 'host_checks'):
            with contextlib.redirect_stdout(io.StringIO()):
                instance.runtime_checks()
        self.assertEqual(instance.failures, 0)


if __name__ == '__main__':
    unittest.main()
