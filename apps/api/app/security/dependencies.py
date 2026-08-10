from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.exceptions import UnauthorizedException
from app.security.tokens import decode_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    """Resolve the current authenticated user from an access token."""
    try:
        payload = decode_token(token)
    except Exception as exc:
        raise UnauthorizedException(
            "Invalid or expired authentication token.",
            code="INVALID_TOKEN",
        ) from exc

    if payload.get("type") != "access":
        raise UnauthorizedException(
            "An access token is required.",
            code="INVALID_TOKEN_TYPE",
        )

    return payload


async def get_current_active_user(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Resolve the current active authenticated user."""
    return current_user
