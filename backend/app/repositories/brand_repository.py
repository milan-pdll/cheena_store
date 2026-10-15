"""Brand repository for managing sportswear manufacturers and badge assets."""

from typing import List, Optional
from app.integrations.catalog_store import CatalogStore
from app.schemas.catalog import Brand


class BrandRepository:
    """Encapsulates querying and updating brands."""

    def __init__(self, store: CatalogStore):
        self._store = store

    async def list_brands(self, include_inactive: bool = False) -> List[Brand]:
        """List all brands alphabetically."""
        catalog = await self._store.load()
        brands = catalog.brands
        if not include_inactive:
            brands = [b for b in brands if b.is_active]
        return sorted(brands, key=lambda b: b.name.lower())

    async def get_by_slug(self, slug: str) -> Optional[Brand]:
        """Find a single brand by slug."""
        brands = await self.list_brands(include_inactive=True)
        for brand in brands:
            if brand.slug.lower() == slug.lower():
                return brand
        return None

    async def upsert(self, brand: Brand) -> Brand:
        """Create or update a brand by slug."""
        catalog = await self._store.load()
        existing_idx = next(
            (i for i, b in enumerate(catalog.brands) if b.slug == brand.slug), None
        )
        if existing_idx is not None:
            catalog.brands[existing_idx] = brand
        else:
            catalog.brands.append(brand)

        await self._store.save(catalog)
        return brand

    async def delete(self, slug: str) -> bool:
        """Delete a brand by slug."""
        catalog = await self._store.load()
        initial_len = len(catalog.brands)
        catalog.brands = [b for b in catalog.brands if b.slug != slug]
        if len(catalog.brands) < initial_len:
            await self._store.save(catalog)
            return True
        return False
