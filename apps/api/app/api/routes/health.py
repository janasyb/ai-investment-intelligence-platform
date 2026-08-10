from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.telemetry import check_liveness, check_readiness, metrics

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
async def liveness() -> dict[str, object]:
    """Return application liveness status."""

    check = check_liveness()

    return {
        "status": check.status,
        "service": check.name,
        "details": check.details,
    }


@router.get("/ready")
async def readiness() -> JSONResponse:
    """Return application readiness status."""

    check = check_readiness()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": check.status,
            "service": check.name,
            "details": check.details,
        },
    )


@router.get("/metrics")
async def application_metrics() -> dict[str, object]:
    """Return application telemetry metrics."""

    return {
        "metrics": metrics.snapshot(),
    }
