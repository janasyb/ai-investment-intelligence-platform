from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.access_request import AccessRequest
from app.repositories.access_request import AccessRequestRepository
from app.schemas.access_request import AccessRequestCreate


class AccessRequestService:
    """Application service for early-access requests."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = AccessRequestRepository(session)

    async def create(
        self,
        data: AccessRequestCreate,
    ) -> AccessRequest:
        """Create and persist an early-access request."""

        return await self.repository.create(data)
