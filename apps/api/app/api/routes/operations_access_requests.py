# ruff: noqa: B008

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db_session
from app.auth.dependencies import get_current_operator, require_csrf
from app.auth.session import OperatorSession
from app.schemas.access_request import (
    AccessRequestStatusUpdate,
    OperationsAccessRequestResponse,
)
from app.services.access_request import AccessRequestService

router = APIRouter(
    prefix="/operations/access-requests",
    tags=["Operations - Access Requests"],
)


@router.get(
    "",
    response_model=list[OperationsAccessRequestResponse],
)
async def list_access_requests(
    _: OperatorSession = Depends(get_current_operator),
    session: AsyncSession = Depends(get_db_session),
) -> list[OperationsAccessRequestResponse]:
    """List early-access requests for authorized operators."""

    service = AccessRequestService(session)
    access_requests = await service.list_all()

    return [
        OperationsAccessRequestResponse.model_validate(access_request)
        for access_request in access_requests
    ]


@router.get(
    "/{access_request_id}",
    response_model=OperationsAccessRequestResponse,
)
async def get_access_request(
    access_request_id: UUID,
    _: OperatorSession = Depends(get_current_operator),
    session: AsyncSession = Depends(get_db_session),
) -> OperationsAccessRequestResponse:
    """Retrieve one early-access request for an authorized operator."""

    service = AccessRequestService(session)

    access_request = await service.get_by_id(access_request_id)

    if access_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access request not found.",
        )

    return OperationsAccessRequestResponse.model_validate(access_request)


@router.patch(
    "/{access_request_id}/status",
    response_model=OperationsAccessRequestResponse,
)
async def update_access_request_status(
    access_request_id: UUID,
    data: AccessRequestStatusUpdate,
    _: OperatorSession = Depends(require_csrf),
    session: AsyncSession = Depends(get_db_session),
) -> OperationsAccessRequestResponse:
    """Update an early-access request's operational status."""

    service = AccessRequestService(session)

    access_request = await service.update_status(
        access_request_id,
        data.status,
    )

    if access_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access request not found.",
        )

    return OperationsAccessRequestResponse.model_validate(access_request)
