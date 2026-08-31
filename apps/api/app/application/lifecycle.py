"""
Application lifecycle management for the AIIP API.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import dispose_engine


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage application startup and shutdown lifecycle.

    Database infrastructure is disposed during application shutdown.
    """

    yield

    await dispose_engine()
