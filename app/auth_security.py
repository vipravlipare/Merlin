"""Small, explicit security primitives for the first account sign-in slice.

Callers supply keys and Redis connections. This keeps secrets out of global
configuration and makes each security dependency visible at the call site.
The narrow login route lives in app.auth_api; production key management remains
an explicit runtime integration task.
"""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import secrets
import time
from dataclasses import dataclass
from typing import Any
from uuid import UUID

import jwt
from argon2 import PasswordHasher, Type, extract_parameters
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from redis.exceptions import RedisError


ACCESS_TOKEN_SECONDS = 15 * 60
REFRESH_IDLE_SECONDS = 30 * 24 * 60 * 60
REFRESH_ABSOLUTE_SECONDS = 90 * 24 * 60 * 60
LOGIN_WINDOW_SECONDS = 15 * 60
USERNAME_FAILURE_LIMIT = 5
IP_FAILURE_LIMIT = 20
TOKEN_ISSUER = "merlin"
TOKEN_AUDIENCE = "merlin-client"

# Keep parameters explicit so the cost is reviewable and testable. Argon2id
# stores its salt and work parameters inside the encoded hash string.
PASSWORD_HASHER = PasswordHasher(
    time_cost=3,
    memory_cost=65_536,
    parallelism=2,
    hash_len=32,
    salt_len=16,
    type=Type.ID,
)


def hash_password(password: str) -> str:
    """Return a salted Argon2id hash; callers must never log the input."""
    if not isinstance(password, str) or not password:
        raise ValueError("Password must contain 1 to 1024 UTF-8 bytes")
    try:
        password_size = len(password.encode("utf-8"))
    except UnicodeEncodeError:
        raise ValueError("Password must contain valid UTF-8 text") from None
    if password_size > 1024:
        raise ValueError("Password must contain 1 to 1024 UTF-8 bytes")
    return PASSWORD_HASHER.hash(password)


def verify_password(password: str, encoded_hash: str) -> bool:
    """Check a stored hash without exposing mismatch or malformed-hash details."""
    if not isinstance(password, str) or not isinstance(encoded_hash, str) or len(encoded_hash) > 512:
        return False
    try:
        if len(password.encode("utf-8")) > 1024:
            return False
        parameters = extract_parameters(encoded_hash)
        # Stored values come from PostgreSQL, but corruption must not make a
        # login request allocate arbitrary memory or CPU during verification.
        if (parameters.type is not Type.ID or parameters.memory_cost > 65_536
                or parameters.time_cost > 3 or parameters.parallelism > 2):
            return False
        return PASSWORD_HASHER.verify(encoded_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError, ValueError, UnicodeEncodeError):
        return False


def create_access_token(
    user_id: UUID,
    private_key: str | bytes,
    *,
    now: int | None = None,
) -> tuple[str, int]:
    """Sign a 15-minute Ed25519 token using the fixed EdDSA algorithm."""
    issued_at = int(time.time()) if now is None else now
    expires_at = issued_at + ACCESS_TOKEN_SECONDS
    token = jwt.encode(
        {
            "sub": str(user_id),
            "iss": TOKEN_ISSUER,
            "aud": TOKEN_AUDIENCE,
            "iat": issued_at,
            "exp": expires_at,
            "jti": secrets.token_urlsafe(16),
        },
        private_key,
        algorithm="EdDSA",
    )
    return token, expires_at


def validate_access_token(
    token: str,
    public_key: str | bytes,
    *,
    now: int | None = None,
) -> UUID:
    """Validate signature, fixed algorithm, issuer, audience and time claims."""
    if not isinstance(token, str) or not token or len(token) > 4096:
        raise ValueError("Invalid access token") from None
    try:
        claims = jwt.decode(
            token,
            public_key,
            algorithms=["EdDSA"],
            issuer=TOKEN_ISSUER,
            audience=TOKEN_AUDIENCE,
            leeway=0,
            options={"require": ["sub", "iss", "aud", "iat", "exp", "jti"]},
        )
        if now is not None:
            # PyJWT validates against wall time; this deterministic claim check
            # lets tests exercise expiry boundaries without changing globals.
            if type(claims["exp"]) is not int or claims["exp"] <= now:
                raise ValueError
            if type(claims["iat"]) is not int or claims["iat"] > now:
                raise ValueError
        return UUID(claims["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise ValueError("Invalid access token") from None


def create_refresh_token() -> tuple[str, bytes]:
    """Return one opaque secret and its SHA-256 digest for PostgreSQL storage."""
    token = secrets.token_urlsafe(48)
    return token, hashlib.sha256(token.encode("ascii")).digest()


def refresh_token_digest(token: str) -> bytes:
    """Hash a presented opaque refresh token before database lookup."""
    if not isinstance(token, str) or not token or len(token) > 256:
        raise ValueError("Invalid refresh token") from None
    try:
        raw = token.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("Invalid refresh token") from None
    return hashlib.sha256(raw).digest()


@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    retry_after: int = 0


_CHECK_FAILURES = """
local now = redis.call('TIME')
local now_ms = now[1] * 1000 + math.floor(now[2] / 1000)
local window_ms = tonumber(ARGV[1])
local retry = 0
for i = 1, 2 do
  local key = KEYS[i]
  local limit = tonumber(ARGV[i + 1])
  redis.call('ZREMRANGEBYSCORE', key, '-inf', now_ms - window_ms)
  local count = redis.call('ZCARD', key)
  if count >= limit then
    local first = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
    local wait = math.ceil((tonumber(first[2]) + window_ms - now_ms) / 1000)
    if wait > retry then retry = wait end
  end
end
return retry
"""

_RECORD_FAILURE = """
local now = redis.call('TIME')
local now_ms = now[1] * 1000 + math.floor(now[2] / 1000)
local window_ms = tonumber(ARGV[1])
local retry = 0
for i = 1, 2 do
  local key = KEYS[i]
  local limit = tonumber(ARGV[i + 1])
  redis.call('ZREMRANGEBYSCORE', key, '-inf', now_ms - window_ms)
  local count = redis.call('ZCARD', key)
  if count >= limit then
    local first = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
    local wait = math.ceil((tonumber(first[2]) + window_ms - now_ms) / 1000)
    if wait > retry then retry = wait end
  end
end
if retry > 0 then return retry end
local member = tostring(now_ms) .. ':' .. ARGV[4]
redis.call('ZADD', KEYS[1], now_ms, member)
redis.call('ZADD', KEYS[2], now_ms, member)
redis.call('EXPIRE', KEYS[1], tonumber(ARGV[5]))
redis.call('EXPIRE', KEYS[2], tonumber(ARGV[5]))
return 0
"""


class RateLimiterUnavailable(RuntimeError):
    """Raised when login throttling cannot be checked safely."""


class LoginRateLimiter:
    """Atomic Redis sliding-window limiter for failed username/IP logins."""

    def __init__(self, redis_client: Any, key_secret: bytes):
        if not isinstance(key_secret, bytes) or len(key_secret) < 32:
            raise ValueError("Rate-limit key secret must contain at least 32 bytes")
        self._redis = redis_client
        self._key_secret = key_secret

    def _key(self, kind: str, value: str) -> str:
        digest = hmac.new(self._key_secret, value.encode("utf-8"), hashlib.sha256).hexdigest()
        return "merlin:login:" + kind + ":" + digest

    def _keys(self, username: str, client_ip: str) -> tuple[str, str]:
        if (not isinstance(username, str) or not 1 <= len(username) <= 20
                or not username.isascii()
                or any(not (character.isalnum() or character == "_") for character in username)):
            raise ValueError("Invalid login name")
        normalized_username = username.lower()
        try:
            normalized_ip = str(ipaddress.ip_address(client_ip))
        except ValueError:
            raise ValueError("Invalid client address") from None
        return (self._key("username", normalized_username), self._key("ip", normalized_ip))

    @staticmethod
    def _decision(seconds: object) -> RateLimitDecision:
        if type(seconds) is not int or seconds < 0:
            raise RateLimiterUnavailable("Login rate limiter unavailable")
        retry_after = seconds
        return RateLimitDecision(retry_after == 0, retry_after)

    def _eval(self, script: str, username: str, client_ip: str, nonce: str = "") -> RateLimitDecision:
        keys = self._keys(username, client_ip)
        try:
            result = self._redis.eval(
                script,
                2,
                *keys,
                LOGIN_WINDOW_SECONDS * 1000,
                USERNAME_FAILURE_LIMIT,
                IP_FAILURE_LIMIT,
                nonce,
                LOGIN_WINDOW_SECONDS,
            )
        except RedisError:
            # Fail closed. Do not include Redis exception text or its cause.
            raise RateLimiterUnavailable("Login rate limiter unavailable") from None
        return self._decision(result)

    def check(self, username: str, client_ip: str) -> RateLimitDecision:
        """Reject before password verification when earlier failures hit a limit."""
        return self._eval(_CHECK_FAILURES, username, client_ip)

    def record_failure(self, username: str, client_ip: str) -> RateLimitDecision:
        """Record one failed login atomically across username and IP windows."""
        return self._eval(_RECORD_FAILURE, username, client_ip, secrets.token_hex(16))
