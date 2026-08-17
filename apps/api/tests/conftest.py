import os
from collections.abc import Generator

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
