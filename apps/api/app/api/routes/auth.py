from __future__ import annotations

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse

from app.auth.dependencies import get_current_operator
from app.auth.oidc import (
    Auth0OIDCService,
    OIDCAuthenticationError,
    OIDCConfigurationError,
)
from app.auth.oidc_transaction import OIDCLoginTransactionStore
from app.auth.session import OperatorSession, OperatorSessionStore
from app.cache.redis import redis_client
from app.core.config.settings import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_oidc_transaction_store() -> OIDCLoginTransactionStore:
    return OIDCLoginTransactionStore(redis_client)


def get_oidc_service() -> Auth0OIDCService:
    return Auth0OIDCService()


def get_operator_session_store() -> OperatorSessionStore:
    return OperatorSessionStore(
        redis_client,
        ttl_seconds=settings.auth0_session_ttl_seconds,
        idle_ttl_seconds=settings.auth0_session_idle_ttl_seconds,
    )


@router.get("/login")
async def login(
    transaction_store: OIDCLoginTransactionStore = Depends(get_oidc_transaction_store),
    oidc: Auth0OIDCService = Depends(get_oidc_service),
) -> RedirectResponse:
    try:
        authorization_url = await oidc.build_authorization_url(
            transaction_store=transaction_store,
        )
    except OIDCConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication provider is not configured.",
        ) from exc
    except OIDCAuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication provider is unavailable.",
        ) from exc

    return RedirectResponse(
        url=authorization_url,
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/callback")
async def callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    transaction_store: OIDCLoginTransactionStore = Depends(get_oidc_transaction_store),
    session_store: OperatorSessionStore = Depends(get_operator_session_store),
    oidc: Auth0OIDCService = Depends(get_oidc_service),
) -> Response:
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication was not completed.",
        )

    if not code or not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid authentication callback.",
        )

    transaction = await transaction_store.consume(state)

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired authentication transaction.",
        )

    try:
        token_response = await oidc.exchange_code(
            code=code,
            transaction=transaction,
        )

        claims = await oidc.validate_id_token(
            id_token=token_response["id_token"],
            transaction=transaction,
        )

    except (OIDCAuthenticationError, OIDCConfigurationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed.",
        ) from exc

    subject = claims.get("sub")

    if not isinstance(subject, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed.",
        )

    if not settings.auth0_operator_subject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator access is not configured.",
        )

    if subject != settings.auth0_operator_subject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator access denied.",
        )

    email = claims.get("email")
    name = claims.get("name")

    session = await session_store.create(
        subject=subject,
        role="operator",
        email=email if isinstance(email, str) else None,
        name=name if isinstance(name, str) else None,
    )

    redirect = RedirectResponse(
        url=f"{settings.frontend_url.rstrip('/')}/operations",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    redirect.set_cookie(
        key=settings.auth0_session_cookie_name,
        value=session.session_id,
        max_age=settings.auth0_session_ttl_seconds,
        httponly=True,
        secure=settings.auth0_secure_cookie,
        samesite="lax",
        path="/",
    )

    return redirect


@router.get("/session")
async def session(
    operator: OperatorSession = Depends(get_current_operator),
) -> dict[str, object]:
    return {
        "authenticated": True,
        "subject": operator.subject,
        "role": operator.role,
        "email": operator.email,
        "name": operator.name,
        "expires_at": operator.expires_at,
        "last_seen_at": operator.last_seen_at,
    }


@router.post("/logout")
async def logout(
    response: Response,
    session_id: str | None = Cookie(
        default=None,
        alias=settings.auth0_session_cookie_name,
    ),
    session_store: OperatorSessionStore = Depends(get_operator_session_store),
) -> dict[str, bool]:
    if session_id:
        await session_store.delete(session_id)

    response.delete_cookie(
        key=settings.auth0_session_cookie_name,
        httponly=True,
        secure=settings.auth0_secure_cookie,
        samesite="lax",
        path="/",
    )

    return {"logged_out": True}
