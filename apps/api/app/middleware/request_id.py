"""
Request ID middleware.

Provides a unique correlation ID for every HTTP request.
"""

from __future__ import annotations

from typing import cast
from uuid import uuid4

from starlette.types import ASGIApp, Message, Receive, Scope, Send

REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware:
    """ASGI middleware that assigns a request correlation ID."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = self._get_request_id(scope)

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append(
                    (
                        REQUEST_ID_HEADER.lower().encode("latin-1"),
                        request_id.encode("latin-1"),
                    )
                )
                message["headers"] = headers

            await send(message)

        await self.app(scope, receive, send_with_request_id)

    @staticmethod
    def _get_request_id(scope: Scope) -> str:
        """Return an incoming request ID or generate one."""

        headers = cast(
            list[tuple[bytes, bytes]],
            scope.get("headers", []),
        )

        for name, value in headers:
            if name.lower() == REQUEST_ID_HEADER.lower().encode("latin-1"):
                try:
                    decoded = value.decode("latin-1").strip()
                except UnicodeDecodeError:
                    break

                if decoded:
                    return decoded

        return str(uuid4())
