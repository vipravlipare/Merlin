"""Build the local API from secrets supplied by the process environment.

This module never creates keys, loads a superuser fallback, or prints
connection details. The database login has authentication-only privileges and
must not inherit the notes role.
"""

from __future__ import annotations

import base64
import binascii
from collections.abc import Mapping
from dataclasses import dataclass, field
import os
from urllib.parse import urlsplit

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
import psycopg
from psycopg.pq import TransactionStatus
import redis

from app.api_server import create_api_app
from app.auth_api import PostgresAuthStore
from app.auth_security import LoginRateLimiter


class RuntimeBootstrapError(RuntimeError):
    """Raised when required local runtime configuration is unsafe or absent."""


@dataclass(frozen=True)
class RuntimeSettings:
    """Validated values needed to create the authenticated API."""

    database_dsn: str = field(repr=False)
    redis_url: str = field(repr=False)
    signing_key: Ed25519PrivateKey = field(repr=False)
    verification_key: Ed25519PublicKey = field(repr=False)
    rate_limit_key: bytes = field(repr=False)


def _decode_secret(value: str) -> bytes:
    try:
        if not value or any(character.isspace() for character in value):
            raise ValueError
        return base64.b64decode(value, altchars=b"-_", validate=True)
    except (binascii.Error, ValueError):
        raise RuntimeBootstrapError("Authentication runtime configuration is invalid") from None


def load_runtime_settings(environment: Mapping[str, str]) -> RuntimeSettings:
    """Parse explicit DSN, Redis URL, Ed25519 keys and HMAC secret."""
    names = (
        "MERLIN_DATABASE_DSN",
        "MERLIN_REDIS_URL",
        "MERLIN_AUTH_SIGNING_KEY_B64",
        "MERLIN_AUTH_VERIFICATION_KEY_B64",
        "MERLIN_RATE_LIMIT_KEY_B64",
    )
    if any(not environment.get(name) for name in names):
        raise RuntimeBootstrapError("Authentication runtime configuration is required")

    database_dsn = environment["MERLIN_DATABASE_DSN"]
    redis_url = environment["MERLIN_REDIS_URL"]
    try:
        # Parse locally so malformed DSNs fail before the listener starts. Never
        # include the parser's exception text; it can contain credential data.
        database_options = psycopg.conninfo.conninfo_to_dict(database_dsn)
        redis_options = redis.connection.parse_url(redis_url)
        database_host = database_options.get("host")
        database_hostaddr = database_options.get("hostaddr")
        if (not isinstance(database_host, str) or "," in database_host
                or database_host not in {"127.0.0.1", "::1"}):
            raise ValueError
        if (database_hostaddr is not None
                and ("," in database_hostaddr or database_hostaddr not in {"127.0.0.1", "::1"})):
            raise ValueError
        if redis_options.get("host") not in {"127.0.0.1", "::1"}:
            raise ValueError
        if urlsplit(redis_url).scheme != "redis":
            raise ValueError
    except (psycopg.Error, ValueError, TypeError):
        raise RuntimeBootstrapError("Authentication runtime configuration is invalid") from None

    signing_bytes = _decode_secret(environment["MERLIN_AUTH_SIGNING_KEY_B64"])
    verification_bytes = _decode_secret(
        environment["MERLIN_AUTH_VERIFICATION_KEY_B64"]
    )
    rate_limit_key = _decode_secret(environment["MERLIN_RATE_LIMIT_KEY_B64"])
    if len(rate_limit_key) < 32:
        raise RuntimeBootstrapError("Authentication runtime configuration is invalid")

    try:
        signing_key = serialization.load_pem_private_key(signing_bytes, password=None)
        verification_key = serialization.load_pem_public_key(verification_bytes)
    except (TypeError, ValueError):
        raise RuntimeBootstrapError("Authentication runtime configuration is invalid") from None
    if (not isinstance(signing_key, Ed25519PrivateKey)
            or not isinstance(verification_key, Ed25519PublicKey)):
        raise RuntimeBootstrapError("Authentication runtime configuration is invalid")

    derived_public = signing_key.public_key().public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )
    configured_public = verification_key.public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )
    if derived_public != configured_public:
        raise RuntimeBootstrapError("Authentication runtime configuration is invalid")

    return RuntimeSettings(
        database_dsn=database_dsn,
        redis_url=redis_url,
        signing_key=signing_key,
        verification_key=verification_key,
        rate_limit_key=rate_limit_key,
    )


def verify_runtime_database(connect) -> None:
    """Require the dedicated app login, RLS membership and auth schema."""
    statement = """
        SELECT current_user = 'merlin_api',
               role.rolcanlogin,
               role.rolinherit,
               role.rolsuper,
               role.rolcreatedb,
               role.rolcreaterole,
               role.rolreplication,
               role.rolbypassrls,
               NOT pg_has_role(current_user, 'merlin_d6_app', 'MEMBER'),
               to_regprocedure('public.lookup_auth_credential(text)') IS NOT NULL,
               to_regclass('public.auth_refresh_families') IS NOT NULL
        FROM pg_roles AS role
        WHERE role.rolname = current_user
    """
    try:
        with connect() as connection:
            if connection.info.transaction_status is not TransactionStatus.IDLE:
                raise RuntimeBootstrapError("Authentication database role is not ready")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                observed = cursor.fetchone()
    except RuntimeBootstrapError:
        raise
    except (psycopg.Error, OSError):
        raise RuntimeBootstrapError("Authentication database is not ready") from None

    if observed != (True, True, False, False, False, False, False, False, True, True, True):
        raise RuntimeBootstrapError("Authentication database role is not ready")


def create_runtime_app(
    settings: RuntimeSettings,
    *,
    connect_factory=None,
    redis_factory=None,
):
    """Create the API after proving database login has only app privileges."""
    connect_factory = psycopg.connect if connect_factory is None else connect_factory
    redis_factory = redis.Redis.from_url if redis_factory is None else redis_factory

    def connect():
        try:
            return connect_factory(
                settings.database_dsn,
                connect_timeout=3,
                application_name="merlin-auth-api",
            )
        except (psycopg.Error, OSError):
            # The store catches psycopg errors and turns them into the same
            # generic 503 used for query failures. Keep driver details hidden.
            raise psycopg.OperationalError("Authentication database unavailable") from None

    verify_runtime_database(connect)
    store = PostgresAuthStore(connect)
    try:
        redis_client = redis_factory(
            settings.redis_url,
            socket_connect_timeout=1,
            socket_timeout=1,
        )
    except (redis.RedisError, ValueError, TypeError):
        raise RuntimeBootstrapError("Authentication rate limiter is not ready") from None
    limiter = LoginRateLimiter(redis_client, settings.rate_limit_key)
    return create_api_app(
        store=store,
        rate_limiter=limiter,
        signing_key=settings.signing_key,
        verification_key=settings.verification_key,
    )


def main() -> None:
    """Load local secrets, verify least privilege, then start the API."""
    import uvicorn

    try:
        settings = load_runtime_settings(os.environ)
        app = create_runtime_app(settings)
    except RuntimeBootstrapError:
        # Fixed text only: startup exceptions may otherwise contain DSNs,
        # usernames, database details or secret material.
        raise SystemExit("Authentication runtime could not start") from None

    uvicorn.run(app, host="127.0.0.1", port=8000, proxy_headers=False)
