from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.security.config import security_settings


def create_access_token(subject: str) -> str:
    """Create a short-lived JWT access token."""
    now = datetime.now(UTC)
    expires_at = now + timedelta(minutes=security_settings.access_token_expire_minutes)

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expires_at,
        "type": "access",
    }

    return jwt.encode(
        payload,
        security_settings.secret_key,
        algorithm=security_settings.algorithm,
    )


def create_refresh_token(subject: str) -> str:
    """Create a longer-lived JWT refresh token."""
    now = datetime.now(UTC)
    expires_at = now + timedelta(days=security_settings.refresh_token_expire_days)

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expires_at,
        "type": "refresh",
    }

    return jwt.encode(
        payload,
        security_settings.secret_key,
        algorithm=security_settings.algorithm,
    )


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token."""
    payload = jwt.decode(
        token,
        security_settings.secret_key,
        algorithms=[security_settings.algorithm],
        options={
            "require": ["sub", "iat", "exp", "type"],
        },
    )

    token_type = payload.get("type")

    if token_type not in {"access", "refresh"}:
        raise jwt.InvalidTokenError("Invalid token type.")

    return payload
