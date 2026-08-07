from fastapi import FastAPI

from app.core.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
)


@app.get("/", tags=["System"])
async def root():
    return {
        "company": "AIIP Technologies",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment.value,
        "status": "running",
    }


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "healthy",
        "environment": settings.environment.value,
    }