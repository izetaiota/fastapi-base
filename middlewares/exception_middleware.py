from fastapi import FastAPI

from core.handlers import setup_exception_handlers as setup_core_exception_handlers


def setup_exception_handlers(app: FastAPI) -> None:
    setup_core_exception_handlers(app)
