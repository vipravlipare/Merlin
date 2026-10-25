"""Focused checks for password, access-token, refresh-token and Redis helpers."""

from __future__ import annotations

import time
from uuid import uuid4

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption
from redis.exceptions import ConnectionError as RedisConnectionError

from app.auth_security import (
    ACCESS_TOKEN_SECONDS,
    REFRESH_ABSOLUTE_SECONDS,
    REFRESH_IDLE_SECONDS,
    LoginRateLimiter,
    RateLimiterUnavailable,
    create_access_token,
    create_refresh_token,
    hash_password,
    refresh_token_digest,
    validate_access_token,
    verify_password,
)


def test_argon2id_hash_is_salted_and_verifies_only_matching_password():
    first = hash_password("synthetic correct horse")
    second = hash_password("synthetic correct horse")
    assert first.startswith("$argon2id$")
    assert first != second
    assert verify_password("synthetic correct horse", first)
    assert not verify_password("different password", first)


@pytest.mark.parametrize("password", ["", "x" * 1025, None], ids=["empty", "oversized", "non-text"])
def test_password_hash_rejects_empty_oversized_or_non_text_input(password):
    with pytest.raises(ValueError):
        hash_password(password)


def test_password_verification_hides_malformed_hash_details():
    assert not verify_password("synthetic password", "not-an-argon-hash")
    assert not verify_password(None, "$argon2id$invalid")


def signing_keys():
    private = Ed25519PrivateKey.generate()
    return (
        private.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()),
        private.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo),
    )


def test_access_token_round_trips_with_fixed_ed_dsa_and_expiry():
    private, public = signing_keys()
    actor = uuid4()
    now = int(time.time())
    token, expires_at = create_access_token(actor, private, now=now)
    assert expires_at == now + 15 * 60
    assert validate_access_token(token, public, now=now) == actor


@pytest.mark.parametrize("mutation", ["wrong-key", "tampered", "expired", "empty", "oversized"])
def test_access_token_rejects_invalid_signature_contents_and_expiry(mutation):
    private, public = signing_keys()
    actor = uuid4()
    now = int(time.time())
    token, _ = create_access_token(actor, private, now=now)
    if mutation == "wrong-key":
        _, public = signing_keys()
    elif mutation == "tampered":
        token = token[:-1] + ("A" if token[-1] != "A" else "B")
    elif mutation == "expired":
        with pytest.raises(ValueError, match="^Invalid access token$"):
            validate_access_token(token, public, now=now + ACCESS_TOKEN_SECONDS)
        return
    elif mutation == "empty":
        token = ""
    else:
        token = "x" * 4097
    with pytest.raises(ValueError, match="^Invalid access token$"):
        validate_access_token(token, public, now=now)


def test_refresh_tokens_are_opaque_random_and_only_digest_is_stored():
    first, first_digest = create_refresh_token()
    second, second_digest = create_refresh_token()
    assert first != second
    assert len(first_digest) == 32
    assert first_digest == refresh_token_digest(first)
    assert first_digest != second_digest
    assert first.encode() not in first_digest


@pytest.mark.parametrize("token", ["", "bad\N{SNOWMAN}", "x" * 257, None],
                         ids=["empty", "non-ascii", "oversized", "non-text"])
def test_refresh_token_parser_rejects_invalid_values(token):
    with pytest.raises(ValueError):
        refresh_token_digest(token)


class RedisScriptStub:
    """Capture the atomic script call without pretending to execute Redis Lua."""

    def __init__(self, result=0, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def eval(self, *args):
        self.calls.append(args)
        if self.error:
            raise self.error
        return self.result


def test_rate_limiter_uses_hmac_keys_atomic_window_and_fixed_limits():
    redis = RedisScriptStub()
    limiter = LoginRateLimiter(redis, b"s" * 32)
    decision = limiter.record_failure("Example_User", "127.0.0.1")
    assert decision.allowed and decision.retry_after == 0
    script, key_count, username_key, ip_key, window_ms, username_limit, ip_limit, nonce, ttl = redis.calls[0]
    assert key_count == 2
    assert "Example_User" not in username_key and "127.0.0.1" not in ip_key
    assert username_key.startswith("merlin:login:username:")
    assert ip_key.startswith("merlin:login:ip:")
    assert "ZREMRANGEBYSCORE" in script and "ZADD" in script
    assert script.count("redis.call('EXPIRE'") == 2
    assert (window_ms, username_limit, ip_limit, ttl) == (15 * 60 * 1000, 5, 20, 15 * 60)
    assert nonce
    assert (REFRESH_IDLE_SECONDS, REFRESH_ABSOLUTE_SECONDS) == (30 * 86400, 90 * 86400)


def test_rate_limit_keys_depend_on_secret_and_never_contain_identifiers():
    first = RedisScriptStub()
    second = RedisScriptStub()
    LoginRateLimiter(first, b"a" * 32).check("private_name", "203.0.113.8")
    LoginRateLimiter(second, b"b" * 32).check("private_name", "203.0.113.8")
    assert first.calls[0][2] != second.calls[0][2]
    assert first.calls[0][3] != second.calls[0][3]


def test_rate_limiter_returns_retry_after_from_redis_decision():
    limiter = LoginRateLimiter(RedisScriptStub(result=45), b"k" * 32)
    decision = limiter.check("sample_user", "2001:db8::1")
    assert not decision.allowed and decision.retry_after == 45


def test_rate_limiter_fails_closed_and_does_not_expose_redis_error():
    sentinel = "private redis connection detail"
    limiter = LoginRateLimiter(RedisScriptStub(error=RedisConnectionError(sentinel)), b"k" * 32)
    with pytest.raises(RateLimiterUnavailable, match="^Login rate limiter unavailable$") as error:
        limiter.check("sample_user", "192.0.2.10")
    assert sentinel not in str(error.value)
    assert error.value.__cause__ is None


@pytest.mark.parametrize("username,client_ip", [
    ("", "192.0.2.1"), ("x" * 21, "192.0.2.1"), ("bad-name", "192.0.2.1"),
    ("nämé", "192.0.2.1"), ("valid_name", "not-an-ip"),
], ids=["empty-username", "oversized-username", "invalid-characters", "non-ascii", "invalid-ip"])
def test_rate_limiter_rejects_unbounded_or_invalid_identifiers(username, client_ip):
    limiter = LoginRateLimiter(RedisScriptStub(), b"k" * 32)
    with pytest.raises(ValueError):
        limiter.check(username, client_ip)


def test_rate_limiter_requires_secret_with_at_least_256_bits():
    with pytest.raises(ValueError):
        LoginRateLimiter(RedisScriptStub(), b"short")
