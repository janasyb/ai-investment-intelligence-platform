"""
FastAPI exception handlers for AIIP application exceptions.
"""

from __future__ import annotations

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.base import AIIPException

logger = logging.getLogger(__name__)


async def aiip_exception_handler(
    request: Request,
    exc: AIIPException,
) -> JSONResponse:
    """Convert an AIIP exception into a consistent API response."""

    logger.warning(
        "Application exception: code=%s path=%s message=%s",
        exc.code,
        request.url.path,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle unexpected exceptions without exposing internal details."""

    logger.exception(
        "Unhandled application exception: path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected internal error occurred.",
                "details": {},
            }
        },
    )
