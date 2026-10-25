"""Authentication HTTP routes, built from explicitly supplied dependencies."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import secrets
from typing import Protocol
from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator
import psycopg
from psycopg.pq import TransactionStatus
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.auth_security import (
    ACCESS_TOKEN_SECONDS,
    LoginRateLimiter,
    RateLimiterUnavailable,
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    validate_access_token,
)


class AuthStoreUnavailable(RuntimeError):
    """Raised when account or refresh-session storage cannot be used safely."""


@dataclass(frozen=True)
class Credential:
    """Only values needed to verify one account's password."""

    user_id: UUID
    password_hash: str


class AuthStore(Protocol):
    """Small storage seam. Tests supply synthetic accounts through this API."""

    def lookup_credential(self, username: str) -> Credential | None: ...

    def create_refresh_session(
        self, user_id: UUID, token_digest: bytes, device_label: str | None
    ) -> None: ...


class PostgresAuthStore:
    """Use only the narrow migration lookup and transaction-local owner setting."""

    def __init__(self, connect: Callable[[], psycopg.Connection]):
        self._connect = connect

    def lookup_credential(self, username: str) -> Credential | None:
        try:
            with self._connect() as connection:
                with connection.cursor() as cursor:
                    # The database function reveals one exact account, not a table scan.
                    cursor.execute(
                        "SELECT user_id, password_hash "
                        "FROM public.lookup_auth_credential(%s)",
                        (username,),
                    )
                    row = cursor.fetchone()
        except psycopg.Error:
            raise AuthStoreUnavailable("Authentication storage unavailable") from None

        if row is None:
            return None
        user_id, password_hash = row
        if not isinstance(user_id, UUID) or not isinstance(password_hash, str):
            raise AuthStoreUnavailable("Authentication storage unavailable") from None
        return Credential(user_id, password_hash)

    def create_refresh_session(
        self, user_id: UUID, token_digest: bytes, device_label: str | None
    ) -> None:
        try:
            with self._connect() as connection:
                if connection.info.transaction_status is not TransactionStatus.IDLE:
                    raise AuthStoreUnavailable("Authentication storage unavailable")
                with connection.cursor() as cursor:
                    # The authenticated actor exists only for this transaction.
                    cursor.execute(
                        "SELECT set_config('merlin.actor_id', %s, true)",
                        (str(user_id),),
                    )
                    cursor.execute(
                        """
                        INSERT INTO public.auth_refresh_families
                            (user_id, device_label, idle_expires_at, absolute_expires_at)
                        VALUES (
                            %s, %s,
                            statement_timestamp() + INTERVAL '30 days',
                            statement_timestamp() + INTERVAL '90 days'
                        )
                        RETURNING id, idle_expires_at
                        """,
                        (user_id, device_label),
                    )
                    family = cursor.fetchone()
                    if family is None:
                        raise AuthStoreUnavailable("Authentication storage unavailable")
                    family_id, idle_expires_at = family
                    # Reuse the family's exact expiry so timestamp rounding cannot
                    # make a new token outlive its parent session.
                    cursor.execute(
                        """
                        INSERT INTO public.auth_refresh_tokens
                            (token_hash, family_id, expires_at)
                        VALUES (%s, %s, %s)
                        """,
                        (token_digest, family_id, idle_expires_at),
                    )
        except psycopg.Error:
            raise AuthStoreUnavailable("Authentication storage unavailable") from None


class LoginRequest(BaseModel):
    """Bounded login input; Pydantic errors are replaced with a generic shape."""

    model_config = ConfigDict(extra="forbid", strict=True)

    username: str = Field(
        min_length=1,
        max_length=20,
        pattern=r"^[A-Za-z0-9_]+$",
    )
    password: str = Field(min_length=1)
    device_label: str | None = Field(default=None, max_length=120)

    @field_validator("password")
    @classmethod
    def password_is_bounded_utf8(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 1024:
            raise ValueError("Password is too long")
        return value

    @field_validator("device_label")
    @classmethod
    def device_label_is_bounded_utf8(cls, value: str | None) -> str | None:
        if value is not None and len(value.encode("utf-8")) > 120:
            raise ValueError("Device label is too long")
        return value


def _error(status_code: int, code: str, message: str, *, headers=None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": code, "message": message},
        headers=headers,
    )


def create_auth_app(
    *,
    store: AuthStore,
    rate_limiter: LoginRateLimiter,
    signing_key: str | bytes,
    verification_key: str | bytes,
    dummy_password_hash: str | None = None,
) -> FastAPI:
    """Build an auth-only ASGI app from explicit, replaceable dependencies."""
    # Unknown usernames still pay Argon2id's normal cost, reducing timing clues.
    if dummy_password_hash is None:
        dummy_password_hash = hash_password(secrets.token_urlsafe(32))

    # This is mounted by api_server; hiding the autogenerated docs keeps the
    # narrow auth application limited to the routes this learning slice needs.
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    @app.exception_handler(RequestValidationError)
    async def invalid_request_handler(
        _request: Request, _error_detail: RequestValidationError
    ) -> JSONResponse:
        return _error(422, "invalid_request", "Request is invalid")

    @app.exception_handler(StarletteHTTPException)
    async def route_error_handler(
        _request: Request, error: StarletteHTTPException
    ) -> JSONResponse:
        if error.status_code == 404:
            return _error(404, "not_found", "Not found")
        if error.status_code == 405:
            return _error(
                405,
                "method_not_allowed",
                "Method not allowed",
                headers=error.headers,
            )
        return _error(error.status_code, "request_failed", "Request could not be completed")

    @app.post("/auth/login")
    def login(payload: LoginRequest, request: Request) -> JSONResponse:
        # Use the direct peer address. Do not trust caller-supplied forwarding headers.
        client_ip = request.client.host if request.client is not None else ""
        normalized_username = payload.username.lower()
        try:
            decision = rate_limiter.check(normalized_username, client_ip)
        except (RateLimiterUnavailable, ValueError):
            return _error(503, "service_unavailable", "Authentication service unavailable")
        if not decision.allowed:
            return _error(
                429,
                "rate_limited",
                "Too many login attempts",
                headers={"Retry-After": str(max(1, decision.retry_after))},
            )

        try:
            credential = store.lookup_credential(normalized_username)
        except AuthStoreUnavailable:
            return _error(503, "service_unavailable", "Authentication service unavailable")

        # A missing account follows the same Argon2id work path as a bad password.
        valid_password = verify_password(
            payload.password,
            credential.password_hash if credential is not None else dummy_password_hash,
        )
        if credential is None or not valid_password:
            try:
                rate_limiter.record_failure(normalized_username, client_ip)
            except (RateLimiterUnavailable, ValueError):
                return _error(503, "service_unavailable", "Authentication service unavailable")
            return _error(401, "invalid_credentials", "Username or password is incorrect")

        access_token, _expires_at = create_access_token(credential.user_id, signing_key)
        refresh_token, token_digest = create_refresh_token()
        try:
            store.create_refresh_session(
                credential.user_id,
                token_digest,
                payload.device_label,
            )
        except AuthStoreUnavailable:
            # Never return an access token when the agreed device session was not stored.
            return _error(503, "service_unavailable", "Authentication service unavailable")

        return JSONResponse(
            status_code=200,
            content={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_SECONDS,
                "refresh_token": refresh_token,
            },
        )

    @app.get("/me")
    def current_user(request: Request) -> JSONResponse:
        """Return only the actor identified by a valid bearer access token."""
        authorization_values = request.headers.getlist("authorization")
        if len(authorization_values) != 1:
            return _invalid_bearer()

        # Split into exactly a scheme and credential; do not accept a query or
        # body user ID as identity, even when a caller supplies one.
        parts = authorization_values[0].split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return _invalid_bearer()
        try:
            actor_id = validate_access_token(parts[1], verification_key)
        except ValueError:
            return _invalid_bearer()

        return JSONResponse(status_code=200, content={"user_id": str(actor_id)})

    return app


def _invalid_bearer() -> JSONResponse:
    """Give every missing, malformed or invalid access token one safe result."""
    return _error(
        401,
        "invalid_token",
        "Authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )
