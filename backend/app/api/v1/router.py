"""Aggregation of all v1 API public and protected admin endpoints."""

from fastapi import APIRouter

from app.api.v1.admin.auth import router as admin_auth_router
from app.api.v1.admin.backup import router as admin_backup_router
from app.api.v1.admin.media import router as admin_media_router
from app.api.v1.admin.products import router as admin_products_router
from app.api.v1.admin.settings import router as admin_settings_router
from app.api.v1.admin.stock import router as admin_stock_router
from app.api.v1.admin.taxonomy import router as admin_taxonomy_router
from app.api.v1.brands import router as brands_router
from app.api.v1.categories import router as categories_router
from app.api.v1.health import router as health_router
from app.api.v1.products import router as products_router
from app.api.v1.settings import router as settings_router

api_v1_router = APIRouter()

# Public storefront endpoints
api_v1_router.include_router(health_router)
api_v1_router.include_router(products_router)
api_v1_router.include_router(categories_router)
api_v1_router.include_router(brands_router)
api_v1_router.include_router(settings_router)

# Protected administrative endpoints
api_v1_router.include_router(admin_auth_router)
api_v1_router.include_router(admin_products_router)
api_v1_router.include_router(admin_stock_router)
api_v1_router.include_router(admin_media_router)
api_v1_router.include_router(admin_taxonomy_router)
api_v1_router.include_router(admin_settings_router)
api_v1_router.include_router(admin_backup_router)
