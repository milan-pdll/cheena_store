"""Settings service providing public contact details and social media channels."""

from app.repositories.settings_repository import SettingsRepository
from app.schemas.catalog import SiteSettings


class SettingsService:
    """Manages site settings, WhatsApp links, and announcement banners."""

    def __init__(self, settings_repo: SettingsRepository):
        self._repo = settings_repo

    async def get_settings(self) -> SiteSettings:
        """Fetch current site settings."""
        return await self._repo.get_settings()

    async def update_settings(self, settings: SiteSettings) -> SiteSettings:
        """Persist new site settings."""
        return await self._repo.update_settings(settings)
