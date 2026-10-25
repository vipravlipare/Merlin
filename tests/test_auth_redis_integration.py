"""Run atomic limiter checks against the disposable Redis supplied by CI."""

from concurrent.futures import ThreadPoolExecutor
import os
import secrets

import pytest
import redis

from app.auth_security import LoginRateLimiter, USERNAME_FAILURE_LIMIT


def test_redis_login_limiter_enforces_both_windows_and_atomic_concurrency():
    """CI sets this URL to its job-owned, disposable Redis service container."""
    url = os.environ.get("MERLIN_REDIS_TEST_URL")
    if not url:
        pytest.skip("An isolated Redis service is required for this integration case")

    client = redis.Redis.from_url(url, socket_connect_timeout=1, socket_timeout=1)
    nonce = secrets.token_hex(16)
    limiter = LoginRateLimiter(client, secrets.token_bytes(32))
    username_keys = []
    ip_keys = []

    def track_keys(username, client_ip):
        username_key, ip_key = limiter._keys(username, client_ip)
        username_keys.append(username_key)
        ip_keys.append(ip_key)

    try:
        assert client.ping() is True

        # Five failures for one normalized username block later attempts from
        # other addresses; each individual address remains below its own cap.
        for index in range(USERNAME_FAILURE_LIMIT):
            ip = f"192.0.2.{index + 1}"
            track_keys("Shared_User", ip)
            assert limiter.check("Shared_User", ip).allowed
            assert limiter.record_failure("Shared_User", ip).allowed
        track_keys("shared_user", "192.0.2.99")
        username_block = limiter.check("shared_user", "192.0.2.99")
        assert not username_block.allowed
        assert 1 <= username_block.retry_after <= 900

        # Twenty different names from one address hit the separate IP cap.
        shared_ip = "198.51.100.29"
        for index in range(20):
            username = f"user_{index:02d}"
            track_keys(username, shared_ip)
            assert limiter.check(username, shared_ip).allowed
            assert limiter.record_failure(username, shared_ip).allowed
        track_keys("new_user", shared_ip)
        ip_block = limiter.check("new_user", shared_ip)
        assert not ip_block.allowed
        assert 1 <= ip_block.retry_after <= 900

        # Concurrent failures share one atomic Lua operation. Exactly five
        # can enter the username window even when requests arrive together.
        concurrent_name = "race_" + nonce[:10]
        concurrent_ip = "203.0.113.40"
        track_keys(concurrent_name, concurrent_ip)
        with ThreadPoolExecutor(max_workers=12) as workers:
            results = list(workers.map(
                lambda _: limiter.record_failure(concurrent_name, concurrent_ip), range(12)
            ))
        assert sum(result.allowed for result in results) == USERNAME_FAILURE_LIMIT
        assert all(result.retry_after > 0 for result in results if not result.allowed)
    finally:
        # Delete only keys created from this test's synthetic identifiers.
        if username_keys or ip_keys:
            client.delete(*set(username_keys + ip_keys))
        client.close()
