from fastapi import FastAPI

from middlewares.cache_middleware import setup_cache
from middlewares.cors_middleware import setup_cors
from middlewares.exception_middleware import setup_exception_handlers
from middlewares.log_middleware import AccessLogMiddleware
from middlewares.rate_limit_middleware import setup_rate_limit
from middlewares.request_id_middleware import RequestIdMiddleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(AccessLogMiddleware)
    setup_exception_handlers(app)
    setup_cors(app)
    setup_rate_limit(app)
    setup_cache(app)
