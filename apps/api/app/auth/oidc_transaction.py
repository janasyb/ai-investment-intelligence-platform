from __future__ import annotations

import secrets
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict
from redis.asyncio import Redis


class OIDCLoginTransaction(BaseModel):
    """Short-lived server-side state for an OIDC authorization transaction."""

    model_config = ConfigDict(frozen=True)

    state: str
    nonce: str
    code_verifier: str
    created_at: datetime


class OIDCLoginTransactionStore:
    """Redis-backed, one-time OIDC login transaction store."""

    _PREFIX = "aiip:oidc-login:"

    def __init__(
        self,
        redis: Redis,
        *,
        ttl_seconds: int = 600,
    ) -> None:
        self._redis = redis
        self._ttl_seconds = ttl_seconds

    async def create(
        self,
        *,
        nonce: str,
        code_verifier: str,
    ) -> OIDCLoginTransaction:
        transaction = OIDCLoginTransaction(
            state=secrets.token_urlsafe(32),
            nonce=nonce,
            code_verifier=code_verifier,
            created_at=datetime.now(UTC),
        )

        await self._redis.set(
            self._key(transaction.state),
            transaction.model_dump_json(),
            ex=self._ttl_seconds,
        )

        return transaction

    async def consume(self, state: str) -> OIDCLoginTransaction | None:
        key = self._key(state)
        payload = await self._redis.getdel(key)

        if payload is None:
            return None

        return OIDCLoginTransaction.model_validate_json(payload)

    @classmethod
    def _key(cls, state: str) -> str:
        return f"{cls._PREFIX}{state}"
