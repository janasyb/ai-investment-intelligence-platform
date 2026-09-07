from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.access_request import AccessRequest
from app.repositories.access_request import AccessRequestRepository
from app.schemas.access_request import AccessRequestCreate


class DuplicateAccessRequestError(Exception):
    """Raised when an access request already exists for an email address."""


class AccessRequestService:
    """Application service for early-access requests."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = AccessRequestRepository(session)

    async def create(
        self,
        data: AccessRequestCreate,
    ) -> AccessRequest:
        """Create and persist an early-access request."""

        try:
            return await self.repository.create(data)
        except IntegrityError as exc:
            await self.repository.session.rollback()

            constraint_name = getattr(
                getattr(exc.orig, "diag", None),
                "constraint_name",
                None,
            )

            if constraint_name == "uq_access_requests_email":
                raise DuplicateAccessRequestError from exc

            raise
