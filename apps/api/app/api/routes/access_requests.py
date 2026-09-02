from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db_session
from app.schemas.access_request import (
    AccessRequestCreate,
    AccessRequestResponse,
)
from app.services.access_request import AccessRequestService

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

    access_request = await service.create(data)

    return AccessRequestResponse.model_validate(access_request)
