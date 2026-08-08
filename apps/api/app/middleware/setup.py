"""
Application middleware registration.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


def configure_middleware(app: FastAPI) -> None:
    """Register all application middleware."""

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)