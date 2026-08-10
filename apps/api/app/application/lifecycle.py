"""
Application lifecycle management for the AIIP API.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage application startup and shutdown lifecycle.

    Infrastructure-specific startup and shutdown hooks will be
    registered here as the platform grows.
    """
    yield
