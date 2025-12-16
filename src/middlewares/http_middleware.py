from __future__ import annotations

from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

class HttpMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            if scope["type"] != "http":
                await self.app(scope, receive, send)
                return
            
            headers = Headers(scope=scope)
            
            await self.app(scope, receive, send)
            
        except Exception as e:
            print(e)
