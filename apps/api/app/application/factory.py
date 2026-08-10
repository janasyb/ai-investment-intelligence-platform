"""
FastAPI application factory for AIIP.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.router import router as api_router
from app.api.routes.health import router as health_router
from app.application.lifecycle import application_lifespan
from app.core.config.settings import settings
from app.core.logging import configure_logging
from app.exceptions import (
    AIIPException,
    aiip_exception_handler,
    unhandled_exception_handler,
)
from app.middleware import configure_middleware


def create_app() -> FastAPI:
    """
    Create and configure the AIIP FastAPI application.

    Application construction is centralized here so the ASGI entrypoint,
    tests, and future application instances can share the same configuration.
    """
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
        lifespan=application_lifespan,
    )

    configure_middleware(app)

    app.add_exception_handler(
        AIIPException,
        aiip_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )

    app.include_router(health_router)
    app.include_router(api_router)

    return app
