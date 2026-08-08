"""
AIIP application exception package.
"""

from app.exceptions.base import (
    AIIPException,
    BadRequestException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    RateLimitException,
    UnauthorizedException,
)
from app.exceptions.handlers import (
    aiip_exception_handler,
    unhandled_exception_handler,
)

__all__ = [
    "AIIPException",
    "BadRequestException",
    "ConflictException",
    "ForbiddenException",
    "NotFoundException",
    "RateLimitException",
    "UnauthorizedException",
    "aiip_exception_handler",
    "unhandled_exception_handler",
]
