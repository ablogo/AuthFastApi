from __future__ import annotations

from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from src.services.jwt_service import verify_token

class JWTMiddleware:
    def __init__(self, app: ASGIApp, secret_key: str, algorithm: str) -> None:
        self.app = app
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        request_token = headers.get("Authorization")
        email, is_token_valid = await verify_token(request_token.__str__())

        await self.app(scope, receive, send)
        