"""Public site settings endpoint for contact numbers, socials, and hero banner."""

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_settings_service
from app.schemas.catalog import SiteSettings
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["Public Settings"])


@router.get("/public", response_model=SiteSettings, status_code=status.HTTP_200_OK)
async def get_public_settings(
    service: SettingsService = Depends(get_settings_service),
) -> SiteSettings:
    """Retrieve public store contact information, WhatsApp order number, and hero banner configuration."""
    return await service.get_settings()
