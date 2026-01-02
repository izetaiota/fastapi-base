import time
from typing import Callable

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from middlewares.request_id_middleware import request_id_ctx


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        latency_ms = (time.perf_counter() - start) * 1000
        logger.bind(
            request_id=request_id_ctx.get(),
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            latency_ms=round(latency_ms, 3),
        ).info("request")
        return response
