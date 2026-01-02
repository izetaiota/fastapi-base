from fastapi import APIRouter

from app.v1.order_router import router as order_router
from app.v1.product_router import router as product_router
from app.v1.user_router import router as user_router

api_v1_router = APIRouter()
api_v1_router.include_router(user_router, tags=["user"])
api_v1_router.include_router(order_router, tags=["order"])
api_v1_router.include_router(product_router, tags=["product"])
