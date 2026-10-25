"""HTTP-boundary checks for login using synthetic accounts and temporary keys."""

from contextlib import contextmanager
from datetime import datetime, timezone
import http.client
import json
import socket
import threading
import time
from uuid import uuid4

import pytest
from psycopg import OperationalError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from starlette.requests import Request
from psycopg.pq import TransactionStatus
import uvicorn

from app.api_server import create_api_app
import app.auth_api as auth_api
import app.api_server as api_server
from app.auth_api import (
    AuthStoreUnavailable,
    Credential,
    LoginRequest,
    PostgresAuthStore,
    create_auth_app,
)
from app.auth_security import (
    RateLimitDecision,
    RateLimiterUnavailable,
    hash_password,
    refresh_token_digest,
    validate_access_token,
    create_access_token,
)


PASSWORD = "synthetic correct horse"
USERNAME = "sample_user"


class SyntheticRateLimiter:
    """Record calls and allow tests to select a normal or blocked decision."""

    def __init__(self, decision=None, error=None):
        self.decision = decision or RateLimitDecision(True, 0)
        self.error = error
        self.events = []
        self.failures = []

    def check(self, username, client_ip):
        self.events.append(("check", username, client_ip))
        if self.error:
            raise self.error
        return self.decision

    def record_failure(self, username, client_ip):
        self.events.append(("record_failure", username, client_ip))
        if self.error:
            raise self.error
        self.failures.append((username, client_ip))
        return RateLimitDecision(True, 0)


class SyntheticStore:
    """Provide one fake account and retain only refresh-token digests."""

    def __init__(self, credential, error=None, session_error=None):
        self.credential = credential
        self.error = error
        self.session_error = session_error
        self.lookups = []
        self.refresh_rows = []

    def lookup_credential(self, username):
        self.lookups.append(username)
        if self.error:
            raise self.error
        if self.credential is None or username != USERNAME:
            return None
        return self.credential

    def create_refresh_session(self, user_id, token_digest, device_label):
        if self.session_error:
            raise self.session_error
        self.refresh_rows.append((user_id, token_digest, device_label))


@pytest.fixture
def login_app():
    """Build isolated app dependencies; no real account or key enters tests."""
    private = Ed25519PrivateKey.generate()
    private_bytes = private.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    public_bytes = private.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    actor = uuid4()
    store = SyntheticStore(Credential(actor, hash_password(PASSWORD)))
    limiter = SyntheticRateLimiter()
    dummy_hash = hash_password("synthetic dummy password")
    app = create_auth_app(
        store=store,
        rate_limiter=limiter,
        signing_key=private_bytes,
        verification_key=public_bytes,
        dummy_password_hash=dummy_hash,
    )
    return app, actor, private_bytes, public_bytes, store, limiter, dummy_hash


def login_response(app, payload, client_ip="192.0.2.10"):
    """Exercise the registered FastAPI endpoint without an unpinned client."""
    route = next(
        route for route in app.routes
        if isinstance(route, APIRoute) and route.path == "/auth/login"
    )
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/auth/login",
        "raw_path": b"/auth/login",
        "query_string": b"",
        "headers": [],
        "client": (client_ip, 32100),
        "server": ("testserver", 80),
    }
    response = route.endpoint(LoginRequest.model_validate(payload), Request(scope))
    return response.status_code, dict(response.headers.raw), json.loads(response.body)


def test_successful_login_signs_access_token_and_stores_only_refresh_digest(login_app):
    app, actor, _private_key, public_key, store, limiter, _dummy_hash = login_app

    status, headers, response = login_response(
        app, {"username": USERNAME, "password": PASSWORD, "device_label": "synthetic laptop"}
    )

    assert status == 200
    assert response["token_type"] == "bearer"
    assert response["expires_in"] == 15 * 60
    assert validate_access_token(response["access_token"], public_key) == actor
    assert len(store.refresh_rows) == 1
    stored_user, stored_digest, device_label = store.refresh_rows[0]
    assert stored_user == actor
    assert stored_digest == refresh_token_digest(response["refresh_token"])
    assert response["refresh_token"].encode("ascii") not in stored_digest
    assert device_label == "synthetic laptop"
    assert limiter.events[0] == ("check", USERNAME, "192.0.2.10")
    assert store.lookups == [USERNAME]
    assert headers[b"content-type"].startswith(b"application/json")


def test_unknown_username_and_wrong_password_have_same_public_error(login_app):
    app, _actor, _private_key, _public_key, store, limiter, _dummy_hash = login_app

    unknown_status, _unknown_headers, unknown = login_response(
        app, {"username": "missing_user", "password": PASSWORD}
    )
    wrong_status, _wrong_headers, wrong = login_response(
        app, {"username": USERNAME, "password": "incorrect password"}
    )

    assert unknown_status == wrong_status == 401
    assert unknown == wrong == {
        "error": "invalid_credentials",
        "message": "Username or password is incorrect",
    }
    assert limiter.failures == [
        ("missing_user", "192.0.2.10"),
        (USERNAME, "192.0.2.10"),
    ]
    assert store.lookups == ["missing_user", USERNAME]


def test_rate_limit_returns_retry_after_without_looking_up_account(login_app):
    app, _actor, _private_key, _public_key, store, limiter, _dummy_hash = login_app
    limiter.decision = RateLimitDecision(False, 45)

    status, headers, response = login_response(
        app, {"username": USERNAME, "password": PASSWORD}
    )

    assert status == 429
    assert headers[b"retry-after"] == b"45"
    assert response == {"error": "rate_limited", "message": "Too many login attempts"}
    assert store.lookups == []


def test_rate_limiter_and_database_errors_are_generic(login_app):
    app, _actor, _private_key, _public_key, store, limiter, _dummy_hash = login_app
    limiter.error = RateLimiterUnavailable("private redis detail")

    status, _headers, response = login_response(
        app, {"username": USERNAME, "password": PASSWORD}
    )

    assert status == 503
    assert response == {
        "error": "service_unavailable",
        "message": "Authentication service unavailable",
    }
    assert "private redis detail" not in json.dumps(response)
    assert store.lookups == []

    limiter.error = None
    store.error = AuthStoreUnavailable("private database detail")
    status, _headers, response = login_response(
        app, {"username": USERNAME, "password": PASSWORD}
    )
    assert status == 503
    assert response == {
        "error": "service_unavailable",
        "message": "Authentication service unavailable",
    }
    assert "private database detail" not in json.dumps(response)


def test_database_connection_failure_uses_generic_login_error(login_app):
    _app, _actor, private_key, public_key, _store, limiter, _dummy_hash = login_app
    sentinel = "SYNTHETIC_DATABASE_CONNECTION_SENTINEL"

    def unavailable():
        raise OperationalError(sentinel)

    app = create_auth_app(
        store=PostgresAuthStore(unavailable),
        rate_limiter=limiter,
        signing_key=private_key,
        verification_key=public_key,
    )
    status, _headers, response = login_response(
        app, {"username": USERNAME, "password": PASSWORD}
    )
    assert status == 503
    assert response == {
        "error": "service_unavailable",
        "message": "Authentication service unavailable",
    }
    assert sentinel not in json.dumps(response)


def test_login_does_not_return_success_when_refresh_session_cannot_be_saved(login_app):
    app, _actor, _private_key, _public_key, store, _limiter, _dummy_hash = login_app
    store.session_error = AuthStoreUnavailable("private session detail")

    status, _headers, response = login_response(
        app, {"username": USERNAME, "password": PASSWORD}
    )

    assert status == 503
    assert response == {
        "error": "service_unavailable",
        "message": "Authentication service unavailable",
    }
    assert "private session detail" not in json.dumps(response)
    assert store.refresh_rows == []


def test_invalid_login_shape_uses_generic_error_and_does_not_touch_dependencies(login_app):
    app, _actor, _private_key, _public_key, store, limiter, _dummy_hash = login_app

    route = app.exception_handlers[RequestValidationError]
    request = Request({
        "type": "http", "method": "POST", "scheme": "http",
        "path": "/auth/login", "raw_path": b"/auth/login", "query_string": b"",
        "headers": [], "client": ("192.0.2.10", 32100), "server": ("testserver", 80),
    })
    invalid = RequestValidationError([{
        "type": "missing", "loc": ("body", "password"),
        "msg": "Field required", "input": None,
    }])
    import asyncio
    response = asyncio.run(route(request, invalid))
    status = response.status_code
    body = json.loads(response.body)

    assert status == 422
    assert body == {"error": "invalid_request", "message": "Request is invalid"}
    assert store.lookups == []
    assert limiter.events == []


def test_unknown_account_still_verifies_the_configured_dummy_hash(login_app, monkeypatch):
    app, _actor, _private_key, _public_key, _store, _limiter, dummy_hash = login_app
    real_verify = auth_api.verify_password
    observed = []

    def record_verify(password, encoded_hash):
        observed.append((password, encoded_hash))
        return real_verify(password, encoded_hash)

    monkeypatch.setattr(auth_api, "verify_password", record_verify)
    status, _headers, _response = login_response(
        app, {"username": "missing_user", "password": PASSWORD}
    )

    assert status == 401
    assert observed == [(PASSWORD, dummy_hash)]


@contextmanager
def running_asgi_app(app):
    """Run a real loopback HTTP server and always stop its serving thread."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 0))
    listener.listen(128)
    address = listener.getsockname()
    server = uvicorn.Server(uvicorn.Config(
        app,
        host="127.0.0.1",
        port=address[1],
        log_level="critical",
        access_log=False,
        lifespan="off",
        proxy_headers=False,
    ))
    errors = []

    def serve():
        try:
            server.run(sockets=[listener])
        except BaseException as error:
            errors.append(error)

    thread = threading.Thread(target=serve, daemon=True)
    try:
        thread.start()
        deadline = time.monotonic() + 3
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started, "ASGI server did not start"
        yield address
    finally:
        server.should_exit = True
        thread.join(timeout=3)
        listener.close()
        assert not thread.is_alive(), "ASGI server thread survived cleanup"
        assert not errors, "ASGI server raised unexpectedly"


def http_json(address, method, path, payload=None, headers=None):
    """Send one bounded loopback request and close its connection."""
    connection = http.client.HTTPConnection(*address, timeout=3)
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request_headers = dict(headers or {})
    if body is not None:
        request_headers["Content-Type"] = "application/json"
    try:
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        response_body = response.read(8193)
        assert len(response_body) <= 8192, "Auth response exceeded test bound"
        return response.status, response.headers, json.loads(response_body or b"null")
    finally:
        connection.close()


def test_asgi_http_login_current_user_identity_and_health_are_wired(login_app):
    _auth_app, actor, private_key, public_key, store, limiter, _dummy_hash = login_app
    app = create_api_app(
        store=store,
        rate_limiter=limiter,
        signing_key=private_key,
        verification_key=public_key,
    )

    with running_asgi_app(app) as address:
        health_status, _health_headers, health = http_json(address, "GET", "/health")
        assert health_status == 200 and health == {"status": "ok"}

        login_status, _headers, login = http_json(
            address, "POST", "/auth/login",
            {"username": USERNAME, "password": PASSWORD},
        )
        assert login_status == 200
        current_status, _headers, current = http_json(
            address,
            "GET",
            "/me?user_id=" + str(uuid4()),
            headers={"Authorization": "Bearer " + login["access_token"]},
        )
        assert current_status == 200 and current == {"user_id": str(actor)}


def test_asgi_http_me_rejects_missing_malformed_expired_and_wrong_key(login_app):
    _auth_app, actor, private_key, public_key, store, limiter, _dummy_hash = login_app
    app = create_api_app(
        store=store,
        rate_limiter=limiter,
        signing_key=private_key,
        verification_key=public_key,
    )
    other_private = Ed25519PrivateKey.generate()
    other_private_bytes = other_private.private_bytes(
        Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
    )
    other_token, _expiry = create_access_token(actor, other_private_bytes)
    expired_token, _expiry = create_access_token(
        actor, private_key, now=int(time.time()) - 3600
    )

    with running_asgi_app(app) as address:
        cases = [
            {},
            {"Authorization": "Basic not-a-bearer"},
            {"Authorization": "Bearer malformed"},
            {"Authorization": "Bearer " + other_token},
            {"Authorization": "Bearer " + expired_token},
        ]
        for headers in cases:
            status, response_headers, body = http_json(address, "GET", "/me", headers=headers)
            assert status == 401
            assert body == {"error": "invalid_token", "message": "Authentication required"}
            assert response_headers.get("www-authenticate") == "Bearer"


def test_asgi_http_validation_and_unknown_notes_route_are_safe(login_app):
    _auth_app, _actor, private_key, public_key, store, limiter, _dummy_hash = login_app
    app = create_api_app(
        store=store,
        rate_limiter=limiter,
        signing_key=private_key,
        verification_key=public_key,
    )

    with running_asgi_app(app) as address:
        status, _headers, body = http_json(
            address, "POST", "/auth/login", {"username": USERNAME}
        )
        assert status == 422
        assert body == {"error": "invalid_request", "message": "Request is invalid"}
        health_status, health_headers, health_error = http_json(address, "POST", "/health")
        assert health_status == 405
        assert health_headers.get("allow") == "GET"
        assert health_error == {
            "error": "method_not_allowed", "message": "Method not allowed"
        }
        missing_status, _headers, missing = http_json(address, "GET", "/notes")
        assert missing_status == 404
        assert missing == {"error": "not_found", "message": "Not found"}
        assert store.lookups == []
        assert limiter.events == []


def test_asgi_http_rate_limit_uses_peer_address_and_stops_lookup(login_app):
    _auth_app, _actor, private_key, public_key, store, limiter, _dummy_hash = login_app
    limiter.decision = RateLimitDecision(False, 45)
    app = create_api_app(
        store=store,
        rate_limiter=limiter,
        signing_key=private_key,
        verification_key=public_key,
    )

    with running_asgi_app(app) as address:
        status, headers, response = http_json(
            address,
            "POST",
            "/auth/login",
            {"username": USERNAME, "password": PASSWORD},
            headers={"X-Forwarded-For": "198.51.100.44"},
        )

    assert status == 429
    assert headers.get("retry-after") == "45"
    assert response == {"error": "rate_limited", "message": "Too many login attempts"}
    assert limiter.events == [("check", USERNAME, "127.0.0.1")]
    assert store.lookups == []


def test_api_server_entrypoint_uses_injected_dependencies_and_loopback(login_app, monkeypatch):
    _auth_app, _actor, private_key, public_key, store, limiter, _dummy_hash = login_app
    observed = {}

    def fake_uvicorn_run(app, *, host, port, proxy_headers):
        observed.update(app=app, host=host, port=port, proxy_headers=proxy_headers)

    monkeypatch.setattr(uvicorn, "run", fake_uvicorn_run)
    api_server.run_api_server(
        store=store,
        rate_limiter=limiter,
        signing_key=private_key,
        verification_key=public_key,
    )

    assert observed["host"] == "127.0.0.1"
    assert observed["port"] == 8000
    assert observed["proxy_headers"] is False
    assert set(observed["app"].openapi()["paths"]) == {"/health", "/auth/login", "/me"}


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def execute(self, statement, parameters):
        self.calls.append((statement, parameters))

    def fetchone(self):
        return self.rows.pop(0)


class FakeConnection:
    def __init__(self, cursor):
        self.info = type("ConnectionInfo", (), {"transaction_status": TransactionStatus.IDLE})()
        self._cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def cursor(self):
        return self._cursor


def test_postgres_store_uses_narrow_bound_lookup_and_local_refresh_owner():
    actor = uuid4()
    family_id = uuid4()
    expiry = datetime(2026, 10, 24, tzinfo=timezone.utc)
    lookup_cursor = FakeCursor([(actor, "$argon2id$synthetic")])
    refresh_cursor = FakeCursor([(family_id, expiry)])
    connections = iter([FakeConnection(lookup_cursor), FakeConnection(refresh_cursor)])
    store = PostgresAuthStore(lambda: next(connections))

    assert store.lookup_credential(USERNAME) == Credential(actor, "$argon2id$synthetic")
    digest = b"d" * 32
    store.create_refresh_session(actor, digest, "synthetic phone")

    lookup_sql, lookup_values = lookup_cursor.calls[0]
    assert "public.lookup_auth_credential(%s)" in lookup_sql
    assert lookup_values == (USERNAME,)
    assert "auth_credentials" not in lookup_sql
    local_owner_sql, local_owner_values = refresh_cursor.calls[0]
    assert "set_config('merlin.actor_id', %s, true)" in local_owner_sql
    assert local_owner_values == (str(actor),)
    assert "INTERVAL '30 days'" in refresh_cursor.calls[1][0]
    assert "INTERVAL '90 days'" in refresh_cursor.calls[1][0]
    assert refresh_cursor.calls[2][1] == (digest, family_id, expiry)
