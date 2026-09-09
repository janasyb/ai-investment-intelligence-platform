from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db_session
from app.schemas.access_request import (
    AccessRequestCreate,
    AccessRequestResponse,
)
from app.services.access_request import (
    AccessRequestService,
    DuplicateAccessRequestError,
)

router = APIRouter(
    prefix="/access-requests",
    tags=["Access Requests"],
)


@router.post(
    "",
    response_model=AccessRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_access_request(
    data: AccessRequestCreate,
    session: AsyncSession = Depends(get_db_session),
) -> AccessRequestResponse:
    """Submit a request for AIIP early access."""

    service = AccessRequestService(session)

    try:
        access_request = await service.create(data)
    except DuplicateAccessRequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An access request already exists for this email address.",
        ) from exc

    return AccessRequestResponse.model_validate(access_request)
