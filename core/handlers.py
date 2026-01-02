from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from core.constant import ErrorCode
from core.exceptions import BusinessError
from middlewares.request_id_middleware import request_id_ctx


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BusinessError)
    async def business_error_handler(request: Request, exc: BusinessError):
        return JSONResponse(
            status_code=400,
            content={
                "code": exc.code,
                "message": getattr(exc, "message", str(exc)),
                "request_id": request_id_ctx.get(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.bind(request_id=request_id_ctx.get()).exception("unhandled")
        return JSONResponse(
            status_code=500,
            content={
                "code": ErrorCode.INTERNAL_ERROR,
                "message": "Internal server error",
                "request_id": request_id_ctx.get(),
            },
        )
