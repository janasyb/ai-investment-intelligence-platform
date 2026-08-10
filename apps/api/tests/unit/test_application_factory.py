from fastapi import FastAPI

from app.application.factory import create_app


def test_create_app_returns_fastapi_application() -> None:
    application = create_app()

    assert isinstance(application, FastAPI)
