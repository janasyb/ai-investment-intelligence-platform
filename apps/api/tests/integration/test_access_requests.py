from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.auth.dependencies import get_current_operator
from app.auth.session import OperatorSession
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


@pytest_asyncio.fixture
async def operator_async_client():
    """Provide an authenticated async HTTP client for operations routes."""

    now = datetime.now(UTC)

    async def override_operator() -> OperatorSession:
        return OperatorSession(
            session_id="integration-test-session",
            subject="auth0|integration-test-operator",
            role="operator",
            email="operator@example.com",
            name="Integration Test Operator",
            csrf_token="test-csrf-token",
            created_at=now,
            expires_at=now.replace(year=now.year + 1),
            last_seen_at=now,
        )

    app.dependency_overrides[get_current_operator] = override_operator

    transport = ASGITransport(app=app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


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


@pytest.mark.asyncio
async def test_update_access_request_status_persists_to_database(
    async_client: AsyncClient,
    operator_async_client: AsyncClient,
) -> None:
    """An operations status update should persist to PostgreSQL."""

    email = f"status-persistence-{uuid4()}@example.com"

    create_response = await async_client.post(
        "/api/v1/access-requests",
        json=build_payload(email),
    )

    assert create_response.status_code == 201

    created_body = create_response.json()
    access_request_id = created_body["id"]

    assert created_body["status"] == "pending"

    update_response = await operator_async_client.patch(
        f"/api/v1/operations/access-requests/{access_request_id}/status",
        headers={"X-CSRF-Token": "test-csrf-token"},
        json={"status": "contacted"},
    )

    assert update_response.status_code == 200

    updated_body = update_response.json()

    assert updated_body["id"] == access_request_id
    assert updated_body["status"] == "contacted"

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AccessRequest).where(
                AccessRequest.email == email,
            )
        )
        access_request = result.scalar_one_or_none()

        assert access_request is not None
        assert str(access_request.id) == access_request_id
        assert access_request.status == "contacted"

        await session.delete(access_request)
        await session.commit()
