from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api.dependencies.database import get_db_session
from app.auth.dependencies import get_current_operator
from app.auth.session import OperatorSession
from app.main import app
from app.models.access_request import AccessRequest


class FakeAccessRequestService:
    """Deterministic service double for operations route tests."""

    def __init__(self, requests: list[AccessRequest]) -> None:
        self.requests = requests

    async def list_all(self) -> list[AccessRequest]:
        return self.requests

    async def get_by_id(
        self,
        access_request_id,
    ) -> AccessRequest | None:
        return next(
            (request for request in self.requests if request.id == access_request_id),
            None,
        )

    async def update_status(
        self,
        access_request_id,
        status: str,
    ) -> AccessRequest | None:
        request = await self.get_by_id(access_request_id)

        if request is None:
            return None

        request.status = status
        request.updated_at = datetime.now(UTC)

        return request


def build_access_request(
    *,
    status: str = "pending",
) -> AccessRequest:
    """Create an in-memory access request for route tests."""

    now = datetime.now(UTC)

    return AccessRequest(
        id=uuid4(),
        name="Test Investor",
        email="investor@example.com",
        profile="investor",
        challenge="I need better digital-asset investment research.",
        consent=True,
        status=status,
        created_at=now,
        updated_at=now,
    )


def build_operator_session(
    *,
    role: str = "operator",
) -> OperatorSession:
    """Create an authenticated operator session for tests."""

    now = datetime.now(UTC)

    return OperatorSession(
        session_id="test-session",
        subject="auth0|test-operator",
        role=role,
        email="operator@example.com",
        name="AIIP Operator",
        created_at=now,
        expires_at=now.replace(
            year=now.year + 1,
        ),
        last_seen_at=now,
    )


class FakeDatabaseSession:
    """Minimal database-session stand-in for route dependency resolution."""


@pytest.fixture
def access_request() -> AccessRequest:
    return build_access_request()


@pytest.fixture
def service(
    access_request: AccessRequest,
) -> FakeAccessRequestService:
    return FakeAccessRequestService([access_request])


@pytest.fixture
def client(
    service: FakeAccessRequestService,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient]:
    async def override_db_session():
        yield FakeDatabaseSession()

    async def override_operator() -> OperatorSession:
        return build_operator_session()

    app.dependency_overrides[get_current_operator] = override_operator
    app.dependency_overrides[get_db_session] = override_db_session

    monkeypatch.setattr(
        "app.api.routes.operations_access_requests.AccessRequestService",
        lambda _: service,
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_operations_list_requires_authentication() -> None:
    async def unauthenticated_operator() -> OperatorSession:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
        )

    app.dependency_overrides[get_current_operator] = unauthenticated_operator

    with TestClient(app) as test_client:
        response = test_client.get(
            "/api/v1/operations/access-requests",
        )

    app.dependency_overrides.clear()

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required."


def test_operations_list_requires_operator_role() -> None:
    async def non_operator() -> OperatorSession:
        raise HTTPException(
            status_code=403,
            detail="Operator access required.",
        )

    app.dependency_overrides[get_current_operator] = non_operator

    with TestClient(app) as test_client:
        response = test_client.get(
            "/api/v1/operations/access-requests",
        )

    app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "Operator access required."


def test_operator_can_list_access_requests(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/operations/access-requests",
    )

    assert response.status_code == 200

    payload = response.json()

    assert len(payload) == 1
    assert payload[0]["name"] == "Test Investor"
    assert payload[0]["email"] == "investor@example.com"
    assert payload[0]["status"] == "pending"


def test_operator_can_retrieve_access_request(
    client: TestClient,
    access_request: AccessRequest,
) -> None:
    response = client.get(
        f"/api/v1/operations/access-requests/{access_request.id}",
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["id"] == str(access_request.id)
    assert payload["name"] == "Test Investor"
    assert payload["challenge"] == ("I need better digital-asset investment research.")
    assert payload["status"] == "pending"


def test_missing_access_request_returns_404(
    client: TestClient,
) -> None:
    missing_id = uuid4()

    response = client.get(
        f"/api/v1/operations/access-requests/{missing_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Access request not found."


@pytest.mark.parametrize(
    "new_status",
    [
        "reviewed",
        "contacted",
        "interview",
        "qualified",
        "report",
        "paid",
        "converted",
        "rejected",
    ],
)
def test_operator_can_update_access_request_status(
    client: TestClient,
    access_request: AccessRequest,
    new_status: str,
) -> None:
    response = client.patch(
        f"/api/v1/operations/access-requests/{access_request.id}/status",
        json={"status": new_status},
    )

    assert response.status_code == 200
    assert response.json()["status"] == new_status
    assert access_request.status == new_status


def test_invalid_status_is_rejected(
    client: TestClient,
    access_request: AccessRequest,
) -> None:
    response = client.patch(
        f"/api/v1/operations/access-requests/{access_request.id}/status",
        json={"status": "invalid-status"},
    )

    assert response.status_code == 422


def test_updating_missing_access_request_returns_404(
    client: TestClient,
) -> None:
    missing_id = uuid4()

    response = client.patch(
        f"/api/v1/operations/access-requests/{missing_id}/status",
        json={"status": "contacted"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Access request not found."


def test_public_access_request_endpoint_remains_public() -> None:
    app.dependency_overrides.clear()

    with TestClient(app) as test_client:
        response = test_client.post(
            "/api/v1/access-requests",
            json={
                "name": "Public Test User",
                "email": "public-test@example.com",
                "profile": "investor",
                "challenge": "Testing public early access.",
                "consent": True,
            },
        )

    assert response.status_code in {201, 409}
