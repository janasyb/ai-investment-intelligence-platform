from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.config.settings import settings


@dataclass(frozen=True, slots=True)
class HealthCheck:
    name: str
    status: str
    details: dict[str, Any]


def check_liveness() -> HealthCheck:
    return HealthCheck(
        name="application",
        status="healthy",
        details={
            "environment": settings.environment.value,
        },
    )


def check_readiness() -> HealthCheck:
    return HealthCheck(
        name="application",
        status="ready",
        details={
            "environment": settings.environment.value,
        },
    )
