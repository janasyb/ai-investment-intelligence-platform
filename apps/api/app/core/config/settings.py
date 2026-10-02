"""
Application settings.

Loads configuration from environment variables and an optional .env file.
"""

from functools import lru_cache
from pathlib import Path
from typing import ClassVar

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.constants import (
    DEFAULT_API_TITLE,
    DEFAULT_API_VERSION,
    DEFAULT_DOCS_PATH,
    DEFAULT_HOST,
    DEFAULT_LOG_LEVEL,
    DEFAULT_OPENAPI_PATH,
    DEFAULT_PORT,
    DEFAULT_REDOC_PATH,
)
from app.core.config.environments import Environment


class Settings(BaseSettings):
    """Application configuration."""

    DEVELOPMENT_SECRET_KEY: ClassVar[str] = (
        "AIIP_DEVELOPMENT_ONLY_SECRET_KEY_DO_NOT_USE_IN_PRODUCTION_123456789"
    )

    API_ROOT: ClassVar[Path] = Path(__file__).resolve().parents[3]

    model_config = SettingsConfigDict(
        env_file=API_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    ########################################################
    # Application
    ########################################################

    app_name: str = DEFAULT_API_TITLE
    app_version: str = DEFAULT_API_VERSION

    environment: Environment = Environment.DEVELOPMENT

    debug: bool = False

    ########################################################
    # Server
    ########################################################

    host: str = DEFAULT_HOST

    port: int = DEFAULT_PORT

    ########################################################
    # API
    ########################################################

    api_prefix: str = "/api/v1"

    docs_url: str = DEFAULT_DOCS_PATH

    redoc_url: str = DEFAULT_REDOC_PATH

    openapi_url: str = DEFAULT_OPENAPI_PATH

    ########################################################
    # Security
    ########################################################

    secret_key: str = Field(
        default=DEVELOPMENT_SECRET_KEY,
        min_length=32,
    )

    algorithm: str = "HS256"

    access_token_expire_minutes: int = 30

    ########################################################
    # Internal Operations Authentication
    ########################################################

    auth0_domain: str = ""
    auth0_client_id: str = ""
    auth0_client_secret: str = ""
    auth0_redirect_uri: str = "http://localhost:8000/api/v1/auth/callback"
    auth0_audience: str = ""
    auth0_scope: str = "openid profile email"
    auth0_operator_subject: str = ""

    auth0_session_cookie_name: str = "aiip_operator_session"

    auth0_session_ttl_seconds: int = 3600
    auth0_session_idle_ttl_seconds: int = 1800

    auth0_secure_cookie: bool = False

    frontend_url: str = "http://localhost:3000"

    ########################################################
    # Database
    ########################################################

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/aiip"

    ########################################################
    # Redis
    ########################################################

    redis_url: str = "redis://localhost:6379/0"

    ########################################################
    # Logging
    ########################################################

    log_level: str = DEFAULT_LOG_LEVEL

    ########################################################
    # Helpers
    ########################################################

    @property
    def is_development(self) -> bool:
        return self.environment.is_local

    @property
    def is_production(self) -> bool:
        return self.environment.is_production

    @property
    def is_testing(self) -> bool:
        return self.environment.is_testing

    @model_validator(mode="after")
    def validate_production_security(self) -> Settings:
        """Prevent unsafe security configuration in production."""

        if not self.is_production:
            return self

        if self.secret_key == self.DEVELOPMENT_SECRET_KEY:
            raise ValueError("Production requires a non-default SECRET_KEY.")

        if not self.auth0_secure_cookie:
            raise ValueError("Production requires AUTH0_SECURE_COOKIE=true.")

        if not self.frontend_url.startswith("https://"):
            raise ValueError("Production requires FRONTEND_URL to use HTTPS.")

        if not self.auth0_redirect_uri.startswith("https://"):
            raise ValueError("Production requires AUTH0_REDIRECT_URI to use HTTPS.")

        required_auth0_settings = {
            "AUTH0_DOMAIN": self.auth0_domain,
            "AUTH0_CLIENT_ID": self.auth0_client_id,
            "AUTH0_CLIENT_SECRET": self.auth0_client_secret,
            "AUTH0_REDIRECT_URI": self.auth0_redirect_uri,
            "AUTH0_AUDIENCE": self.auth0_audience,
            "AUTH0_OPERATOR_SUBJECT": self.auth0_operator_subject,
        }

        missing = [name for name, value in required_auth0_settings.items() if not value.strip()]

        if missing:
            raise ValueError(
                "Production requires these authentication settings: " + ", ".join(missing)
            )

        return self


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings singleton.

    Prevents rebuilding configuration for every request.
    """
    return Settings()


settings = get_settings()
