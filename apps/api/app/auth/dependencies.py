from __future__ import annotations

from fastapi import Cookie, Depends, HTTPException, status

from app.auth.session import OperatorSession, OperatorSessionStore
from app.cache.redis import redis_client
from app.core.config.settings import settings


def get_operator_session_store() -> OperatorSessionStore:
    return OperatorSessionStore(
        redis_client,
        ttl_seconds=settings.auth0_session_ttl_seconds,
        idle_ttl_seconds=settings.auth0_session_idle_ttl_seconds,
    )


async def get_current_operator(
    session_id: str | None = Cookie(
        default=None,
        alias=settings.auth0_session_cookie_name,
    ),
    store: OperatorSessionStore = Depends(get_operator_session_store),
) -> OperatorSession:
    """Require an authenticated internal operator session."""

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    session = await store.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session.",
        )

    if session.role != "operator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator access required.",
        )

    return session
