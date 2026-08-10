from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config.settings import settings
from app.core.logging import configure_logging
from app.exceptions import (
    AIIPException,
    aiip_exception_handler,
    unhandled_exception_handler,
)
from app.middleware import configure_middleware

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
)

configure_middleware(app)

app.add_exception_handler(
    AIIPException,
    aiip_exception_handler,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    return {
        "company": "AIIP Technologies",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment.value,
        "status": "running",
    }


app.include_router(health_router)
