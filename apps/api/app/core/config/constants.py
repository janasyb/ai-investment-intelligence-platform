"""
Platform-wide configuration constants.

Only values that are truly constant should live here.
"""

from pathlib import Path

PROJECT_NAME = "AI Investment Intelligence Platform"
COMPANY_NAME = "AIIP Technologies"

API_V1_PREFIX = "/api/v1"

DEFAULT_TIMEZONE = "UTC"

BASE_DIR = Path(__file__).resolve().parents[4]

APP_DIR = BASE_DIR / "apps" / "api"

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_PORT = 8000

DEFAULT_HOST = "0.0.0.0"

DEFAULT_API_TITLE = PROJECT_NAME

DEFAULT_API_VERSION = "0.1.0-alpha"

DEFAULT_OPENAPI_PATH = "/openapi.json"

DEFAULT_DOCS_PATH = "/docs"

DEFAULT_REDOC_PATH = "/redoc"