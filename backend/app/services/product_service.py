"""Product business logic service handling catalog filtering, slug lookups, and presentation DTOs."""

import math
from typing import Optional

from app.core.exceptions import NotFoundException
from app.repositories.product_repository import ProductRepository
from app.schemas.catalog import Product
from app.schemas.product_query import PaginatedProductsResponse, ProductFilterParams


class ProductService:
    """Coordinates product catalogue queries and business validation rules."""

    def __init__(self, product_repo: ProductRepository):
        self._repo = product_repo

    async def list_products(
        self, params: ProductFilterParams
    ) -> PaginatedProductsResponse:
        """Fetch filtered and paginated product items for public or admin catalog."""
        items, total = await self._repo.query_products(params)
        total_pages = math.ceil(total / params.page_size) if total > 0 else 1

        return PaginatedProductsResponse(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
        )

    async def get_by_slug(self, slug: str) -> Product:
        """Retrieve single active product by slug, or raise NotFoundException."""
        product = await self._repo.get_by_slug(slug)
        if not product:
            raise NotFoundException(f"Product with slug '{slug}' not found.")
        return product

    async def get_by_id(self, product_id: str) -> Product:
        """Retrieve product by UUID, or raise NotFoundException."""
        product = await self._repo.get_by_id(product_id, include_deleted=False)
        if not product:
            raise NotFoundException(f"Product with id '{product_id}' not found.")
        return product
