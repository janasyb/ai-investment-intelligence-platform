from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.access_requests import router as access_requests_router
from app.api.routes.auth import router as auth_router
from app.api.routes.operations_access_requests import (
    router as operations_access_requests_router,
)

router = APIRouter(prefix="/v1", tags=["API v1"])

router.include_router(auth_router)
router.include_router(access_requests_router)
router.include_router(operations_access_requests_router)
