from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.access_request import AccessRequest
from app.schemas.access_request import AccessRequestCreate


class AccessRequestRepository:
    """Persistence operations for access requests."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        data: AccessRequestCreate,
    ) -> AccessRequest:
        """Persist a new access request."""

        access_request = AccessRequest(
            name=data.name,
            email=str(data.email),
            profile=data.profile,
            challenge=data.challenge,
            consent=data.consent,
            status="pending",
        )

        self.session.add(access_request)
        await self.session.commit()
        await self.session.refresh(access_request)

        return access_request
