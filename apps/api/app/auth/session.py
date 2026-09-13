from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, ConfigDict
from redis.asyncio import Redis


class OperatorSession(BaseModel):
    """Authenticated AIIP internal operator session."""

    model_config = ConfigDict(frozen=True)

    session_id: str
    subject: str
    role: str
    email: str | None = None
    name: str | None = None
    created_at: datetime
    expires_at: datetime
    last_seen_at: datetime


class OperatorSessionStore:
    """Redis-backed server-side operator session store."""

    _PREFIX = "aiip:operator-session:"

    def __init__(
        self,
        redis: Redis,
        *,
        ttl_seconds: int,
        idle_ttl_seconds: int,
    ) -> None:
        self._redis = redis
        self._ttl_seconds = ttl_seconds
        self._idle_ttl_seconds = idle_ttl_seconds

    async def create(
        self,
        *,
        subject: str,
        role: str,
        email: str | None = None,
        name: str | None = None,
    ) -> OperatorSession:
        now = datetime.now(UTC)
        session_id = secrets.token_urlsafe(32)

        session = OperatorSession(
            session_id=session_id,
            subject=subject,
            role=role,
            email=email,
            name=name,
            created_at=now,
            expires_at=now + timedelta(seconds=self._ttl_seconds),
            last_seen_at=now,
        )

        await self._redis.set(
            self._key(session_id),
            session.model_dump_json(),
            ex=self._ttl_seconds,
        )

        return session

    async def get(self, session_id: str) -> OperatorSession | None:
        key = self._key(session_id)
        payload = await self._redis.get(key)

        if payload is None:
            return None

        session = OperatorSession.model_validate_json(payload)
        now = datetime.now(UTC)

        if now >= session.expires_at:
            await self._redis.delete(key)
            return None

        remaining_seconds = max(
            1,
            int((session.expires_at - now).total_seconds()),
        )
        redis_ttl_seconds = min(
            self._idle_ttl_seconds,
            remaining_seconds,
        )

        refreshed_session = session.model_copy(
            update={"last_seen_at": now},
        )

        await self._redis.set(
            key,
            refreshed_session.model_dump_json(),
            ex=redis_ttl_seconds,
        )

        return refreshed_session

    async def delete(self, session_id: str) -> None:
        await self._redis.delete(self._key(session_id))

    @classmethod
    def _key(cls, session_id: str) -> str:
        return f"{cls._PREFIX}{session_id}"
