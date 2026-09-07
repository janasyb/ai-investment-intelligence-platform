from __future__ import annotations

import asyncio
import os
import sys
from collections.abc import Generator

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.environ.setdefault(
    "SECRET_KEY",
    "test-secret-key-for-aiip-api-tests-only-32chars",
)

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
