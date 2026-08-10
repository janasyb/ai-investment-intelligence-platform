from dataclasses import dataclass

from app.core.config.settings import settings


@dataclass(slots=True, frozen=True)
class SecuritySettings:
    """Security configuration derived from application settings."""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int = 7


security_settings = SecuritySettings(
    secret_key=settings.secret_key,
    algorithm=settings.algorithm,
    access_token_expire_minutes=settings.access_token_expire_minutes,
)
