"""Taxonomy service managing active store categories and sportswear brands."""

from typing import List
from app.core.exceptions import NotFoundException
from app.repositories.brand_repository import BrandRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.admin import BrandUpsertRequest, CategoryUpsertRequest
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

    async def list_all_categories(self) -> List[Category]:
        """Fetch all categories including inactive ones for admin manager."""
        return await self._cat_repo.list_categories(include_inactive=True)

    async def upsert_category(self, req: CategoryUpsertRequest) -> Category:
        """Create or update category metadata."""
        category = Category(
            slug=req.slug,
            name=req.name,
            description=req.description,
            is_active=req.is_active,
            display_order=req.display_order,
        )
        return await self._cat_repo.upsert(category)

    async def delete_category(self, slug: str) -> bool:
        """Delete category by slug."""
        deleted = await self._cat_repo.delete(slug)
        if not deleted:
            raise NotFoundException(f"Category '{slug}' not found.")
        return True

    async def list_public_brands(self) -> List[Brand]:
        """Fetch active brands for storefront filter bar."""
        return await self._brand_repo.list_brands(include_inactive=False)

    async def list_all_brands(self) -> List[Brand]:
        """Fetch all brands for admin manager."""
        return await self._brand_repo.list_brands(include_inactive=True)

    async def upsert_brand(self, req: BrandUpsertRequest) -> Brand:
        """Create or update brand."""
        brand = Brand(
            slug=req.slug,
            name=req.name,
            logo_url=req.logo_url,
            is_active=req.is_active,
        )
        return await self._brand_repo.upsert(brand)

    async def delete_brand(self, slug: str) -> bool:
        """Delete brand by slug."""
        deleted = await self._brand_repo.delete(slug)
        if not deleted:
            raise NotFoundException(f"Brand '{slug}' not found.")
        return True
