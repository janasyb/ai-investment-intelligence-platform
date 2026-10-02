from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from app.core.config.environments import Environment
from app.core.config.settings import Settings


def build_production_settings(**overrides: object) -> Settings:
    values: dict[str, Any] = {
        "environment": Environment.PRODUCTION,
        "secret_key": "production-secret-key-that-is-long-enough-123456",
        "auth0_domain": "aiip.example.auth0.com",
        "auth0_client_id": "production-client-id",
        "auth0_client_secret": "production-client-secret",
        "auth0_redirect_uri": "https://api.aiip.example.com/api/v1/auth/callback",
        "auth0_audience": "https://api.aiip.example.com",
        "auth0_operator_subject": "auth0|production-operator",
        "frontend_url": "https://app.aiip.example.com",
        "auth0_secure_cookie": True,
    }

    values.update(overrides)

    return Settings(**values)


def test_production_security_configuration_is_accepted() -> None:
    settings = build_production_settings()

    assert settings.environment is Environment.PRODUCTION
    assert settings.auth0_secure_cookie is True
    assert settings.frontend_url.startswith("https://")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("secret_key", Settings.DEVELOPMENT_SECRET_KEY),
        ("auth0_secure_cookie", False),
        ("frontend_url", "http://app.aiip.example.com"),
        (
            "auth0_redirect_uri",
            "http://api.aiip.example.com/api/v1/auth/callback",
        ),
    ],
)
def test_production_rejects_unsafe_security_configuration(
    field: str,
    value: object,
) -> None:
    with pytest.raises(ValidationError):
        build_production_settings(**{field: value})


@pytest.mark.parametrize(
    "field",
    [
        "auth0_domain",
        "auth0_client_id",
        "auth0_client_secret",
        "auth0_redirect_uri",
        "auth0_audience",
        "auth0_operator_subject",
    ],
)
def test_production_requires_auth0_configuration(field: str) -> None:
    with pytest.raises(ValidationError):
        build_production_settings(**{field: ""})


def test_development_can_use_local_security_defaults() -> None:
    settings = Settings(
        environment=Environment.DEVELOPMENT,
    )

    assert settings.is_development is True
    assert settings.auth0_secure_cookie is False
