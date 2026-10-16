"""Contract checks for the real scratch API; all files and servers are synthetic.

These are loopback integration tests plus focused entry-point/response unit tests.
No real database, private files, fixed-port listener or external service is used.
"""
from contextlib import contextmanager
import http.client
import json
import select
from pathlib import Path
import socket
import subprocess
import sys
import threading
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app import health_api, health_server

PRIVATE_SENTINEL = "SYNTHETIC_HEALTH_ERROR_SENTINEL"
FILE_SENTINEL = "SYNTHETIC_FILE_CONTENT_SENTINEL"
ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def running_api(health_func=None, address=("127.0.0.1", 0)):
    """Own every accepted socket and worker so failed tests can still clean up."""
    handler = (health_api.make_health_handler() if health_func is None
               else health_api.make_health_handler(health_func))
    ready = threading.Event()
    accepted_connection = threading.Event()
    guard = threading.Lock()
    sockets, workers, errors = [], [], []

    class TrackedServer(health_server.ThreadingHTTPServer):
        def service_actions(self):
            ready.set()  # The serving loop actually ran; no startup sleep.
            super().service_actions()

        def get_request(self):
            connection, peer = super().get_request()
            with guard:
                sockets.append(connection)
            accepted_connection.set()
            return connection, peer

        def finish_request(self, connection, peer):
            with guard:
                workers.append(threading.current_thread())
            super().finish_request(connection, peer)

        def handle_error(self, connection, peer):
            # Unexpected background exceptions must fail rather than merely log.
            with guard:
                errors.append(type(sys.exception()).__name__)

    server = TrackedServer(address, handler)
    thread = threading.Thread(target=server.serve_forever,
                              kwargs={"poll_interval": 0.01}, daemon=True)
    api = SimpleNamespace(server=server, address=server.server_address,
                          thread=thread, workers=workers, accepted=accepted_connection)
    try:
        thread.start()
        assert ready.wait(2), "API serving loop did not start"
        yield api
    finally:
        # First unblock owned connections, including a failed idle-client test.
        with guard:
            accepted = list(sockets)
        for connection in accepted:
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass  # The handler may already have closed its connection.
            connection.close()
        if thread.is_alive():
            server.shutdown()  # Controlling thread, never the serving thread.
        server.server_close()
        if thread.ident is not None:
            thread.join(timeout=3)
        assert not thread.is_alive(), "API serving thread survived cleanup"
        for worker in workers:
            worker.join(timeout=3)
            assert not worker.is_alive(), "API request worker survived cleanup"
        assert not errors, "Unexpected background API exception: " + ",".join(errors)


@pytest.fixture
def api_server():
    """Return the context manager so each test makes its lifetime explicit."""
    return running_api


def request(api, method="GET", path="/health", *, timeout=3):
    """Bypass proxy settings; bound reads and close even on assertion failure."""
    client = http.client.HTTPConnection(*api.address, timeout=timeout)
    try:
        client.request(method, path)
        response = client.getresponse()
        body = response.read(4097)
        assert len(body) <= 4096, "Small API response exceeded its test limit"
        return response.status, response.headers, body
    finally:
        client.close()


def assert_json_response(response, status, expected, *, allow=None):
    actual, headers, body = response
    assert actual == status
    assert headers.get_all("Content-Type") == ["application/json"]
    assert headers.get_all("Content-Length") == [str(len(body))]
    assert json.loads(body.decode("utf-8")) == expected
    if allow is not None:
        assert headers.get_all("Allow") == [allow]
    return headers, body


def test_health_endpoint_success(api_server):
    """API-01: compare status, complete JSON, encoding and response framing."""
    with api_server() as api:
        assert_json_response(request(api), 200, {"status": "ok"})


@pytest.mark.parametrize("method", ["GET", "POST", "PUT"])
def test_unknown_path_is_not_found_before_method_dispatch(api_server, method):
    """API-02 and routing precedence: an unknown route is never healthy/405."""
    health = Mock(side_effect=AssertionError("Unknown route called health"))
    with api_server(health) as api:
        assert_json_response(request(api, method, "/missing"), 404,
                             {"error": "Not found"})
        health.assert_not_called()


@pytest.mark.parametrize("method", ["GET", "POST", "PUT"])
def test_sensitive_path_never_serves_a_file(api_server, tmp_path, monkeypatch, method):
    """API-03: a real synthetic file makes accidental file serving observable."""
    (tmp_path / ".env").write_text(FILE_SENTINEL, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    health = Mock(side_effect=AssertionError("Unknown route called health"))
    with api_server(health) as api:
        headers, body = assert_json_response(request(api, method, "/.env"), 404,
                                             {"error": "Not found"})
        assert FILE_SENTINEL not in body.decode("utf-8") + str(headers)
        health.assert_not_called()


@pytest.mark.parametrize("method", ["POST", "PUT"])
def test_unsupported_method_has_exact_error_and_allow(api_server, method):
    """API-04/05: each real dispatch must reject the method and advertise GET."""
    health = Mock(side_effect=AssertionError("Unsupported method called health"))
    with api_server(health) as api:
        assert_json_response(request(api, method), 405,
                             {"error": "Method not allowed"}, allow="GET")
        health.assert_not_called()


def test_handler_failure_is_generic_and_recovers_on_same_server(api_server):
    """API-06/07: a failing replacement cannot kill or poison this server."""
    health = Mock(side_effect=[RuntimeError(PRIVATE_SENTINEL), {"status": "ok"}])
    with api_server(health) as api:
        headers, body = assert_json_response(request(api), 500,
                                             {"error": "Internal server error"})
        assert PRIVATE_SENTINEL not in body.decode("utf-8") + str(headers)
        assert_json_response(request(api), 200, {"status": "ok"})
        assert health.call_count == 2
    with api_server() as normal:
        assert_json_response(request(normal), 200, {"status": "ok"})


def test_unserializable_health_result_is_generic_500(api_server):
    """JSON preparation failure must occur before any successful headers."""
    with api_server(lambda: object()) as api:
        assert_json_response(request(api), 500, {"error": "Internal server error"})


def test_body_write_failure_does_not_send_a_second_response():
    """Regression: network failure after 200 headers cannot become another 500."""
    handler_class = health_api.make_health_handler()
    handler = handler_class.__new__(handler_class)
    handler.path = "/health"
    handler.send_response = Mock()
    handler.send_header = Mock()
    handler.end_headers = Mock()
    handler.wfile = Mock()
    handler.wfile.write.side_effect = BrokenPipeError("Synthetic disconnected client")
    with pytest.raises(BrokenPipeError):
        handler.handle_request("GET")
    handler.send_response.assert_called_once_with(200)
    assert handler.wfile.write.call_count == 1


def test_idle_connection_does_not_block_health_and_times_out(api_server):
    """Exercise concurrency and the real two-second accepted-socket timeout."""
    assert health_api.make_health_handler().timeout == 2
    with api_server() as api:
        idle = socket.create_connection(api.address, timeout=3)
        try:
            # Receiving EOF proves the server accepted and closed this socket.
            # The health request must succeed while that socket remains idle.
            assert api.accepted.wait(1), "Idle connection was not accepted"
            assert_json_response(request(api, timeout=1), 200, {"status": "ok"})
            assert not select.select([idle], [], [], 0)[0], "Idle connection closed prematurely"
            idle.settimeout(3)
            assert idle.recv(1) == b"", "Idle connection remained open or sent data"
        finally:
            idle.close()


def test_loopback_cleanup_after_failure_and_real_restart(api_server):
    """An assertion failure still releases workers/socket; a new server works."""
    with pytest.raises(AssertionError, match="Synthetic failed assertion"):
        with api_server() as first:
            address = first.address
            assert address[0] == "127.0.0.1" and address[1] > 0
            assert_json_response(request(first), 200, {"status": "ok"})
            raise AssertionError("Synthetic failed assertion")
    assert not first.thread.is_alive()
    assert all(not worker.is_alive() for worker in first.workers)
    with api_server(address=address) as restarted:
        assert_json_response(request(restarted), 200, {"status": "ok"})


@pytest.mark.parametrize("failure", [KeyboardInterrupt, RuntimeError])
def test_actual_entry_point_binds_loopback_and_always_closes(monkeypatch, failure):
    """Check production constructor arguments, not only our fixture's address."""
    server = Mock()
    server.serve_forever.side_effect = failure("Synthetic serving stop")
    constructor = Mock(return_value=server)
    expected_handler = health_api.make_health_handler()
    factory = Mock(return_value=expected_handler)
    monkeypatch.setattr(health_api, "make_health_handler", factory)
    monkeypatch.setattr(health_server, "ThreadingHTTPServer", constructor)
    if failure is KeyboardInterrupt:
        health_server.run()
    else:
        with pytest.raises(RuntimeError, match="Synthetic serving stop"):
            health_server.run()
    arguments, keywords = constructor.call_args
    assert not keywords and arguments[0] == ("127.0.0.1", 8000)
    assert arguments[1] is expected_handler
    factory.assert_called_once_with()
    constructor.assert_called_once()
    server.serve_forever.assert_called_once_with()
    server.server_close.assert_called_once_with()


def test_module_imports_have_no_server_side_effects():
    """A fresh interpreter must neither construct a listener nor start threads."""
    script = """
from unittest.mock import patch
with patch('socket.socket', side_effect=AssertionError('Import opened a socket')), \\
     patch('threading.Thread.start', side_effect=AssertionError('Import started a thread')):
    import app.health_api
    import app.health_server
"""
    result = subprocess.run([sys.executable, "-c", script], cwd=ROOT,
                            capture_output=True, text=True, timeout=5)
    assert result.returncode == 0, "Import unexpectedly attempted server startup"
