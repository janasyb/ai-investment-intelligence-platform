from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.config.settings import settings
from app.main import app


def test_cors_allows_configured_frontend_origin() -> None:
    with TestClient(app) as client:
        response = client.options(
            "/api/v1/operations/access-requests/example/status",
            headers={
                "Origin": settings.frontend_url.rstrip("/"),
                "Access-Control-Request-Method": "PATCH",
                "Access-Control-Request-Headers": "Content-Type, X-CSRF-Token",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (settings.frontend_url.rstrip("/"))
    assert response.headers["access-control-allow-credentials"] == "true"


def test_cors_allows_csrf_header_for_configured_frontend() -> None:
    with TestClient(app) as client:
        response = client.options(
            "/api/v1/operations/access-requests/example/status",
            headers={
                "Origin": settings.frontend_url.rstrip("/"),
                "Access-Control-Request-Method": "PATCH",
                "Access-Control-Request-Headers": "X-CSRF-Token",
            },
        )

    assert response.status_code == 200
    assert "x-csrf-token" in response.headers["access-control-allow-headers"].lower()


def test_cors_rejects_unconfigured_origin() -> None:
    with TestClient(app) as client:
        response = client.options(
            "/api/v1/operations/access-requests/example/status",
            headers={
                "Origin": "https://malicious.example",
                "Access-Control-Request-Method": "PATCH",
                "Access-Control-Request-Headers": "X-CSRF-Token",
            },
        )

    assert "access-control-allow-origin" not in response.headers
