"""
FastAPI exception handlers for AIIP application exceptions.
"""

from __future__ import annotations

import logging
from typing import cast

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.base import AIIPException

logger = logging.getLogger(__name__)


async def aiip_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Convert an AIIP application exception into a consistent API response."""

    aiip_exc = cast(AIIPException, exc)

    logger.warning(
        "Application exception: code=%s path=%s message=%s",
        aiip_exc.code,
        request.url.path,
        aiip_exc.message,
    )

    return JSONResponse(
        status_code=aiip_exc.status_code,
        content={
            "error": {
                "code": aiip_exc.code,
                "message": aiip_exc.message,
                "details": aiip_exc.details,
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
