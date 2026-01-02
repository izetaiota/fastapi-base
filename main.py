from fastapi import FastAPI

from app.v1 import api_v1_router
from core.config import settings
from middlewares import setup_middlewares
from utils.logger import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title=settings.project_name)
    setup_middlewares(app)
    app.include_router(api_v1_router, prefix="/api/v1")
    return app


app = create_app()
