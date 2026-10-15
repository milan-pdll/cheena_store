"""Aggregation of all v1 API public endpoints."""

from fastapi import APIRouter

from app.api.v1.brands import router as brands_router
from app.api.v1.categories import router as categories_router
from app.api.v1.health import router as health_router
from app.api.v1.products import router as products_router
from app.api.v1.settings import router as settings_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(products_router)
api_v1_router.include_router(categories_router)
api_v1_router.include_router(brands_router)
api_v1_router.include_router(settings_router)
