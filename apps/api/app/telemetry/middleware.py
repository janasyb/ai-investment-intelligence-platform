from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.telemetry.metrics import metrics


class TelemetryMiddleware(BaseHTTPMiddleware):
    """Collect application-level request metrics."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        metrics.record_request()

        response = await call_next(request)

        if response.status_code >= 500:
            metrics.record_5xx_response()

        return response
