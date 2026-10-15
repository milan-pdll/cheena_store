"""Category repository for managing store departments and navigation hierarchies."""

from typing import List, Optional
from app.integrations.catalog_store import CatalogStore
from app.schemas.catalog import Category


class CategoryRepository:
    """Encapsulates querying and updating product categories."""

    def __init__(self, store: CatalogStore):
        self._store = store

    async def list_categories(self, include_inactive: bool = False) -> List[Category]:
        """List all categories, ordered by display_order."""
        catalog = await self._store.load()
        categories = catalog.categories
        if not include_inactive:
            categories = [c for c in categories if c.is_active]
        return sorted(categories, key=lambda c: c.display_order)

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        """Find a single category by slug."""
        categories = await self.list_categories(include_inactive=True)
        for cat in categories:
            if cat.slug.lower() == slug.lower():
                return cat
        return None

    async def upsert(self, category: Category) -> Category:
        """Create or update a category by slug."""
        catalog = await self._store.load()
        existing_idx = next(
            (i for i, c in enumerate(catalog.categories) if c.slug == category.slug),
            None,
        )
        if existing_idx is not None:
            catalog.categories[existing_idx] = category
        else:
            catalog.categories.append(category)

        await self._store.save(catalog)
        return category

    async def delete(self, slug: str) -> bool:
        """Delete a category by slug."""
        catalog = await self._store.load()
        initial_len = len(catalog.categories)
        catalog.categories = [c for c in catalog.categories if c.slug != slug]
        if len(catalog.categories) < initial_len:
            await self._store.save(catalog)
            return True
        return False
