"""Run Python checks in fresh forked processes from a pristine import snapshot.

Ubuntu/WSL only. Never fork a multithreaded parent or reuse a test process.
Each child gets separate memory, process group, output and a timeout. The parent
imports dependencies only: it must not execute tests or import app modules.
"""
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
import time
import traceback


def _exit_code(action):
    try:
        action()
        return 0
    except SystemExit as error:
        if error.code is None:
            return 0
        if isinstance(error.code, int):
            return error.code
        print(error.code, file=sys.stderr)
        return 1
    except BaseException:
        traceback.print_exc()
        return 1


def _start(action, stdout, stderr):
    if threading.active_count() != 1:
        raise RuntimeError('Fork isolation requires a single-threaded parent')
    sys.stdout.flush(); sys.stderr.flush()
    pid = os.fork()
    if pid == 0:
        try:
            os.setsid()
            # Faults can turn import guards into interactive CLI entry points.
            # A detached session still inherits an open terminal on fd 0;
            # close that input channel so unattended audits cannot await secrets.
            with open(os.devnull, 'r') as input_stream:
                os.dup2(input_stream.fileno(), 0)
            sys.stdin = os.fdopen(os.dup(0), 'r', encoding='utf8')
            with open(stdout, 'w') as output, open(stderr, 'w') as errors:
                os.dup2(output.fileno(), 1); os.dup2(errors.fileno(), 2)
                sys.stdout = os.fdopen(os.dup(1), 'w', buffering=1, encoding='utf8')
                sys.stderr = os.fdopen(os.dup(2), 'w', buffering=1, encoding='utf8')
                code = _exit_code(action)
                sys.stdout.flush(); sys.stderr.flush()
            os._exit(code & 255)
        except BaseException:
            os._exit(127)
    return pid


def _kill(pid):
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        # A child may not have reached setsid yet.
        try: os.kill(pid, signal.SIGKILL)
        except ProcessLookupError: pass


def fork_jobs(jobs, *, workers=8, timeout=45):
    """Yield ordered (returncode, stdout, stderr) results; never cache a result."""
    import pytest  # Warm dependency imports only; pytest.main runs in children.
    import importlib
    from _pytest.config import default_plugins
    for plugin in default_plugins:
        importlib.import_module("_pytest." + plugin)
    for dependency in ["emoji", "regex", "psycopg", "unittest.mock", "tomllib"]:
        importlib.import_module(dependency)
    forbidden = ['app.health_api', 'app.health_server', 'test_health_api', 'tests.test_health_api',
                 'app.note_rules', 'app.notes_maintenance', 'app.database_connectivity_probe',
                 'tools.doctor', 'doctor', 'tools.prd_lint']
    if any(name in sys.modules for name in forbidden):
        raise RuntimeError('Fork parent must not contain application modules')
    active = {}; completed = {}; launched = yielded = 0
    try:
        while yielded < len(jobs):
            while launched < len(jobs) and len(active) < workers:
                job = jobs[launched]
                def action(job=job):
                    sys.argv = ['-c', *job['argv']]
                    exec(compile(job['code'], '<string>', 'exec'), {'__name__': '__main__'})
                pid = _start(action, job['stdout'], job['stderr'])
                active[pid] = (launched, time.monotonic())
                launched += 1
            for pid, (index, started) in list(active.items()):
                ended, status = os.waitpid(pid, os.WNOHANG)
                expired = not ended and time.monotonic() - started > timeout
                if expired:
                    _kill(pid); os.waitpid(pid, 0)
                if ended or expired:
                    job = jobs[index]
                    completed[index] = (None if expired else os.waitstatus_to_exitcode(status),
                                        Path(job['stdout']).read_text(), Path(job['stderr']).read_text())
                    del active[pid]
            while yielded in completed:
                yield completed.pop(yielded)
                yielded += 1
            if active:
                time.sleep(.002)
    finally:
        for pid in active:
            _kill(pid); os.waitpid(pid, 0)


def run_script(command, *, capture_output, text, timeout, cwd=None):
    """Execute the actual CLI file in a fresh process, preserving its argv."""
    import runpy
    with tempfile.TemporaryDirectory(prefix='merlin-python-cli-') as directory:
        out = Path(directory) / 'stdout'; err = Path(directory) / 'stderr'
        def action():
            if cwd is not None:
                os.chdir(cwd)
            sys.argv = list(command[1:])
            sys.path[0] = str(Path(command[1]).resolve().parent)
            runpy.run_path(command[1], run_name='__main__')
        pid = _start(action, out, err)
        started = time.monotonic()
        try:
            while True:
                ended, status = os.waitpid(pid, os.WNOHANG)
                if ended:
                    return subprocess.CompletedProcess(command, os.waitstatus_to_exitcode(status),
                                                       out.read_text(), err.read_text())
                if time.monotonic() - started > timeout:
                    _kill(pid); os.waitpid(pid, 0)
                    raise subprocess.TimeoutExpired(command, timeout)
                time.sleep(.001)
        except BaseException:
            # If the child was already reaped this is harmless.
            _kill(pid)
            try: os.waitpid(pid, 0)
            except ChildProcessError: pass
            raise
