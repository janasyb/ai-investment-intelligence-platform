"""
Application exception definitions.

This module contains the base exception hierarchy used throughout AIIP.
"""

from __future__ import annotations

from typing import Any


class AIIPException(Exception):
    """Base exception for all expected AIIP application errors."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "AIIP_ERROR",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class BadRequestException(AIIPException):
    """Raised when a request is invalid."""

    def __init__(
        self,
        message: str = "The request is invalid.",
        *,
        code: str = "BAD_REQUEST",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            status_code=400,
            details=details,
        )


class UnauthorizedException(AIIPException):
    """Raised when authentication is required or invalid."""

    def __init__(
        self,
        message: str = "Authentication is required.",
        *,
        code: str = "UNAUTHORIZED",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            status_code=401,
            details=details,
        )


class ForbiddenException(AIIPException):
    """Raised when the authenticated user lacks permission."""

    def __init__(
        self,
        message: str = "You do not have permission to perform this action.",
        *,
        code: str = "FORBIDDEN",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            status_code=403,
            details=details,
        )


class NotFoundException(AIIPException):
    """Raised when a requested resource does not exist."""

    def __init__(
        self,
        message: str = "The requested resource was not found.",
        *,
        code: str = "NOT_FOUND",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            status_code=404,
            details=details,
        )


class ConflictException(AIIPException):
    """Raised when a request conflicts with existing state."""

    def __init__(
        self,
        message: str = "The request conflicts with the current state.",
        *,
        code: str = "CONFLICT",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            status_code=409,
            details=details,
        )


class RateLimitException(AIIPException):
    """Raised when a client exceeds an allowed request rate."""

    def __init__(
        self,
        message: str = "Too many requests.",
        *,
        code: str = "RATE_LIMITED",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            status_code=429,
            details=details,
        )
