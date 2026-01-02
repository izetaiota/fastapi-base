import sys

from loguru import logger

from middlewares.request_id_middleware import request_id_ctx


def configure_logging() -> None:
    logger.remove()

    def _patch(record):
        record["extra"]["request_id"] = request_id_ctx.get()
        return record

    logger.configure(patcher=_patch)
    logger.add(sys.stdout, enqueue=True, backtrace=False, diagnose=False)
