from __future__ import annotations

from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.main import app
from app.models.access_request import AccessRequest


@pytest_asyncio.fixture
async def async_client():
    """Provide an async HTTP client against the FastAPI application."""

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


def build_payload(email: str) -> dict[str, object]:
    """Build a valid early-access request payload."""

    return {
        "name": "Integration Test User",
        "email": email,
        "profile": "Digital asset investor",
        "challenge": "I need better research before making investment decisions.",
        "consent": True,
    }


@pytest.mark.asyncio
async def test_create_access_request_persists_to_database(
    async_client: AsyncClient,
) -> None:
    """A valid access request should be created and persisted."""

    email = f"integration-{uuid4()}@example.com"

    response = await async_client.post(
        "/api/v1/access-requests",
        json=build_payload(email),
    )

    assert response.status_code == 201

    body = response.json()

    assert body["email"] == email
    assert body["status"] == "pending"
    assert body["consent"] is True

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(AccessRequest).where(AccessRequest.email == email))
        access_request = result.scalar_one_or_none()

        assert access_request is not None
        assert access_request.email == email
        assert access_request.status == "pending"
        assert access_request.consent is True

        await session.delete(access_request)
        await session.commit()


@pytest.mark.asyncio
async def test_duplicate_access_request_returns_conflict(
    async_client: AsyncClient,
) -> None:
    """A second request using the same email should return HTTP 409."""

    email = f"duplicate-{uuid4()}@example.com"
    payload = build_payload(email)

    first_response = await async_client.post(
        "/api/v1/access-requests",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = await async_client.post(
        "/api/v1/access-requests",
        json=payload,
    )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "An access request already exists for this email address."
    }

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(AccessRequest).where(AccessRequest.email == email))
        access_requests = result.scalars().all()

        assert len(access_requests) == 1

        for access_request in access_requests:
            await session.delete(access_request)

        await session.commit()


@pytest.mark.asyncio
async def test_invalid_email_is_rejected(
    async_client: AsyncClient,
) -> None:
    """An invalid email address should be rejected by request validation."""

    payload = build_payload("not-an-email")

    response = await async_client.post(
        "/api/v1/access-requests",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_consent_is_required(
    async_client: AsyncClient,
) -> None:
    """An access request without consent should be rejected."""

    email = f"no-consent-{uuid4()}@example.com"

    payload = build_payload(email)
    payload["consent"] = False

    response = await async_client.post(
        "/api/v1/access-requests",
        json=payload,
    )

    assert response.status_code == 422

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(AccessRequest).where(AccessRequest.email == email))
        access_request = result.scalar_one_or_none()

        assert access_request is None
