"""Admin settings management endpoints for updating store info, WhatsApp numbers, and banners."""

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_settings_service
from app.core.security import get_current_admin
from app.schemas.catalog import SiteSettings
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/admin/settings", tags=["Admin Settings"])


@router.get("", response_model=SiteSettings, status_code=status.HTTP_200_OK)
async def get_admin_settings(
    service: SettingsService = Depends(get_settings_service),
    _: str = Depends(get_current_admin),
) -> SiteSettings:
    """Retrieve all site settings for admin configuration."""
    return await service.get_settings()


@router.put("", response_model=SiteSettings, status_code=status.HTTP_200_OK)
async def update_admin_settings(
    payload: SiteSettings,
    service: SettingsService = Depends(get_settings_service),
    _: str = Depends(get_current_admin),
) -> SiteSettings:
    """Update store contact channels, WhatsApp number, and hero banner."""
    return await service.update_settings(payload)
