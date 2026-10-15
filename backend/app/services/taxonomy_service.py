"""Taxonomy service managing active store categories and sportswear brands."""

from typing import List
from app.repositories.brand_repository import BrandRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.catalog import Brand, Category


class TaxonomyService:
    """Business service coordinating categories and brand manufacturer catalogs."""

    def __init__(
        self,
        category_repo: CategoryRepository,
        brand_repo: BrandRepository,
    ):
        self._cat_repo = category_repo
        self._brand_repo = brand_repo

    async def list_public_categories(self) -> List[Category]:
        """Fetch active categories for storefront navigation."""
        return await self._cat_repo.list_categories(include_inactive=False)

    async def list_public_brands(self) -> List[Brand]:
        """Fetch active brands for storefront filter bar."""
        return await self._brand_repo.list_brands(include_inactive=False)
