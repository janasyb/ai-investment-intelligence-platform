from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest

from app.auth.session import OperatorSession, OperatorSessionStore


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.expirations: dict[str, int] = {}

    async def set(
        self,
        name: str,
        value: str,
        *,
        ex: int | None = None,
    ) -> bool:
        self.values[name] = value

        if ex is not None:
            self.expirations[name] = ex

        return True

    async def get(self, name: str) -> str | None:
        return self.values.get(name)

    async def delete(self, *names: str) -> int:
        deleted = 0

        for name in names:
            if name in self.values:
                del self.values[name]
                self.expirations.pop(name, None)
                deleted += 1

        return deleted


@pytest.mark.asyncio
async def test_create_and_get_session() -> None:
    redis = FakeRedis()

    store = OperatorSessionStore(
        redis,
        ttl_seconds=3600,
        idle_ttl_seconds=1800,
    )

    session = await store.create(
        subject="auth0|operator-123",
        role="operator",
        email="operator@example.com",
        name="AIIP Operator",
    )

    restored = await store.get(session.session_id)

    assert restored is not None
    assert restored.session_id == session.session_id
    assert restored.subject == "auth0|operator-123"
    assert restored.role == "operator"
    assert restored.email == "operator@example.com"
    assert restored.name == "AIIP Operator"

    assert restored.created_at.tzinfo == UTC
    assert restored.expires_at > restored.created_at
    assert restored.last_seen_at >= session.last_seen_at


@pytest.mark.asyncio
async def test_missing_session_returns_none() -> None:
    redis = FakeRedis()

    store = OperatorSessionStore(
        redis,
        ttl_seconds=3600,
        idle_ttl_seconds=1800,
    )

    assert await store.get("missing-session") is None


@pytest.mark.asyncio
async def test_delete_session() -> None:
    redis = FakeRedis()

    store = OperatorSessionStore(
        redis,
        ttl_seconds=3600,
        idle_ttl_seconds=1800,
    )

    session = await store.create(
        subject="auth0|operator-123",
        role="operator",
    )

    await store.delete(session.session_id)

    assert await store.get(session.session_id) is None


@pytest.mark.asyncio
async def test_session_refreshes_idle_timeout() -> None:
    redis = FakeRedis()

    store = OperatorSessionStore(
        redis,
        ttl_seconds=3600,
        idle_ttl_seconds=1800,
    )

    session = await store.create(
        subject="auth0|operator-123",
        role="operator",
    )

    key = f"aiip:operator-session:{session.session_id}"

    assert redis.expirations[key] == 3600

    await store.get(session.session_id)

    assert redis.expirations[key] <= 1800


@pytest.mark.asyncio
async def test_expired_session_is_deleted() -> None:
    redis = FakeRedis()

    store = OperatorSessionStore(
        redis,
        ttl_seconds=3600,
        idle_ttl_seconds=1800,
    )

    now = datetime.now(UTC)
    key = "aiip:operator-session:expired-session"

    expired = {
        "session_id": "expired-session",
        "subject": "auth0|operator-123",
        "role": "operator",
        "email": None,
        "name": None,
        "created_at": (now - timedelta(hours=2)).isoformat(),
        "expires_at": (now - timedelta(hours=1)).isoformat(),
        "last_seen_at": (now - timedelta(hours=1, minutes=30)).isoformat(),
    }

    redis.values[key] = json.dumps(expired)

    assert await store.get("expired-session") is None
    assert key not in redis.values


@pytest.mark.asyncio
async def test_idle_timeout_cannot_extend_beyond_absolute_expiration() -> None:
    redis = FakeRedis()

    store = OperatorSessionStore(
        redis,
        ttl_seconds=10,
        idle_ttl_seconds=30,
    )

    session = await store.create(
        subject="auth0|operator-123",
        role="operator",
    )

    key = f"aiip:operator-session:{session.session_id}"

    await store.get(session.session_id)

    assert 1 <= redis.expirations[key] <= 10


@pytest.mark.asyncio
async def test_session_persists_updated_last_seen_at() -> None:
    redis = FakeRedis()

    store = OperatorSessionStore(
        redis,
        ttl_seconds=3600,
        idle_ttl_seconds=1800,
    )

    session = await store.create(
        subject="auth0|operator-123",
        role="operator",
    )

    before = session.last_seen_at

    restored = await store.get(session.session_id)

    assert restored is not None
    assert restored.last_seen_at >= before

    key = f"aiip:operator-session:{session.session_id}"
    payload = redis.values[key]
    persisted = OperatorSession.model_validate_json(payload)

    assert persisted.last_seen_at == restored.last_seen_at
