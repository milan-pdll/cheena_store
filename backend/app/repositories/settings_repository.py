"""Settings repository for reading and updating global store contact info and hero metadata."""

from app.integrations.catalog_store import CatalogStore
from app.schemas.catalog import SiteSettings


class SettingsRepository:
    """Encapsulates querying and modifying site settings in the catalog document."""

    def __init__(self, store: CatalogStore):
        self._store = store

    async def get_settings(self) -> SiteSettings:
        """Fetch current site settings."""
        catalog = await self._store.load()
        return catalog.site_settings

    async def update_settings(self, settings: SiteSettings) -> SiteSettings:
        """Save updated site settings to catalog."""
        catalog = await self._store.load()
        catalog.site_settings = settings
        await self._store.save(catalog)
        return settings
