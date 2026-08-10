"""
AIIP API ASGI entrypoint.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.application.factory import create_app
from app.core.config.settings import settings

app: FastAPI = create_app()


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """Return basic application metadata."""
    return {
        "company": "AIIP Technologies",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment.value,
        "status": "running",
    }
