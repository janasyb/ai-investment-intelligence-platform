from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.api.routes.auth import get_operator_session_store
from app.auth.dependencies import get_current_operator
from app.auth.session import OperatorSession
from app.main import app


def build_operator_session() -> OperatorSession:
    now = datetime.now(UTC)

    return OperatorSession(
        session_id="test-session-id",
        subject="auth0|test-operator",
        role="operator",
        email="operator@example.com",
        name="AIIP Operator",
        csrf_token="test-csrf-token",
        created_at=now,
        expires_at=now + timedelta(hours=1),
        last_seen_at=now,
    )


class FakeOperatorSessionStore:
    """Minimal session-store double for authentication route tests."""

    def __init__(self, session: OperatorSession) -> None:
        self.session = session
        self.deleted_session_ids: list[str] = []

    async def delete(self, session_id: str) -> None:
        self.deleted_session_ids.append(session_id)


def test_authenticated_session_returns_csrf_token_and_not_session_id() -> None:
    session = build_operator_session()

    async def override_operator() -> OperatorSession:
        return session

    app.dependency_overrides[get_current_operator] = override_operator

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/auth/session")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    payload = response.json()

    assert payload["authenticated"] is True
    assert payload["subject"] == session.subject
    assert payload["role"] == "operator"
    assert payload["email"] == session.email
    assert payload["name"] == session.name
    assert payload["csrf_token"] == session.csrf_token
    assert "session_id" not in payload


def test_logout_requires_csrf_token() -> None:
    session = build_operator_session()
    store = FakeOperatorSessionStore(session)

    async def override_operator() -> OperatorSession:
        return session

    def override_store() -> FakeOperatorSessionStore:
        return store

    app.dependency_overrides[get_current_operator] = override_operator
    app.dependency_overrides[get_operator_session_store] = override_store

    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/auth/logout")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "CSRF validation failed."
    assert store.deleted_session_ids == []


def test_logout_rejects_invalid_csrf_token() -> None:
    session = build_operator_session()
    store = FakeOperatorSessionStore(session)

    async def override_operator() -> OperatorSession:
        return session

    def override_store() -> FakeOperatorSessionStore:
        return store

    app.dependency_overrides[get_current_operator] = override_operator
    app.dependency_overrides[get_operator_session_store] = override_store

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/auth/logout",
                headers={"X-CSRF-Token": "wrong-token"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "CSRF validation failed."
    assert store.deleted_session_ids == []


def test_logout_with_valid_csrf_token_deletes_session() -> None:
    session = build_operator_session()
    store = FakeOperatorSessionStore(session)

    async def override_operator() -> OperatorSession:
        return session

    def override_store() -> FakeOperatorSessionStore:
        return store

    app.dependency_overrides[get_current_operator] = override_operator
    app.dependency_overrides[get_operator_session_store] = override_store

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/auth/logout",
                headers={"X-CSRF-Token": session.csrf_token},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"logged_out": True}
    assert store.deleted_session_ids == [session.session_id]
