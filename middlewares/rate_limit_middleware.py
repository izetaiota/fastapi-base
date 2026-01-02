from fastapi import FastAPI
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.config import settings
from middlewares.request_id_middleware import request_id_ctx

limiter = Limiter(key_func=get_remote_address)


def setup_rate_limit(app: FastAPI) -> None:
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "code": "RATE_LIMITED",
                "message": "Too many requests",
                "request_id": request_id_ctx.get(),
            },
        )

    # Apply default rate limit to all routes; per-route overrides can be added later.
    for route in app.router.routes:
        if hasattr(route, "endpoint"):
            limiter.limit(settings.rate_limit)(route.endpoint)
