"""Product repository performing in-memory query, filter, sort, and atomic updates on catalog."""

from datetime import datetime, timezone
import math
from typing import List, Optional, Tuple

from app.integrations.catalog_store import CatalogStore
from app.schemas.catalog import Product
from app.schemas.product_query import ProductFilterParams


class ProductRepository:
    """Encapsulates in-memory querying, filtering, and mutation of products."""

    def __init__(self, store: CatalogStore):
        self._store = store

    async def get_all(self, include_deleted: bool = False) -> List[Product]:
        """Return all products with optional inclusion of soft-deleted items."""
        catalog = await self._store.load()
        if include_deleted:
            return list(catalog.products)
        return [p for p in catalog.products if p.deleted_at is None]

    async def get_by_id(
        self, product_id: str, include_deleted: bool = False
    ) -> Optional[Product]:
        """Find a single product by UUID."""
        products = await self.get_all(include_deleted=include_deleted)
        for p in products:
            if p.id == product_id:
                return p
        return None

    async def get_by_slug(self, slug: str) -> Optional[Product]:
        """Find an active, non-deleted product by slug."""
        products = await self.get_all(include_deleted=False)
        for p in products:
            if p.slug == slug and p.is_active:
                return p
        return None

    async def query_products(
        self, params: ProductFilterParams
    ) -> Tuple[List[Product], int]:
        """Filter, search, sort, and paginate products in-memory."""
        products = await self.get_all(include_deleted=False)

        # 1. Base filter: only active products for public listing
        filtered = [p for p in products if p.is_active]

        # 2. Filter by category slug
        if params.category:
            filtered = [
                p for p in filtered if p.category_slug.lower() == params.category.lower()
            ]

        # 3. Filter by brand slug
        if params.brand:
            filtered = [
                p for p in filtered if p.brand_slug.lower() == params.brand.lower()
            ]

        # 4. Filter by ground type (boots only)
        if params.ground_type:
            filtered = [
                p for p in filtered if p.ground_type == params.ground_type
            ]

        # 5. Filter by price bounds (effective price considers discount_price if set)
        if params.min_price is not None:
            filtered = [
                p
                for p in filtered
                if (p.discount_price if p.discount_price is not None else p.price)
                >= params.min_price
            ]
        if params.max_price is not None:
            filtered = [
                p
                for p in filtered
                if (p.discount_price if p.discount_price is not None else p.price)
                <= params.max_price
            ]

        # 6. Filter by stock status
        if params.in_stock is not None:
            filtered = [p for p in filtered if p.in_stock == params.in_stock]

        # 7. Filter by specific variant size
        if params.size:
            target_size = params.size.strip().lower()
            filtered = [
                p
                for p in filtered
                if any(
                    v.size.lower() == target_size and v.stock_quantity > 0
                    for v in p.variants
                )
            ]

        # 8. Filter by featured flag
        if params.featured is not None:
            filtered = [p for p in filtered if p.is_featured == params.featured]

        # 9. Free-text search (name, description, brand)
        if params.q:
            query = params.q.strip().lower()
            filtered = [
                p
                for p in filtered
                if query in p.name.lower()
                or query in p.description.lower()
                or query in p.brand_slug.lower()
            ]

        # 10. Sorting
        sort_mode = params.sort or "featured"
        if sort_mode == "price_asc":
            filtered.sort(
                key=lambda p: (
                    p.discount_price if p.discount_price is not None else p.price
                )
            )
        elif sort_mode == "price_desc":
            filtered.sort(
                key=lambda p: (
                    p.discount_price if p.discount_price is not None else p.price
                ),
                reverse=True,
            )
        elif sort_mode == "newest":
            filtered.sort(key=lambda p: p.created_at, reverse=True)
        elif sort_mode == "name_asc":
            filtered.sort(key=lambda p: p.name.lower())
        else:
            # Default: Featured first, then display_order, then newest
            filtered.sort(
                key=lambda p: (
                    not p.is_featured,
                    p.display_order,
                    p.created_at,
                )
            )

        total_count = len(filtered)

        # 11. Pagination
        start_idx = (params.page - 1) * params.page_size
        end_idx = start_idx + params.page_size
        paginated_items = filtered[start_idx:end_idx]

        return paginated_items, total_count

    async def save_product(self, product: Product) -> Product:
        """Create or update a product in the catalog document."""
        catalog = await self._store.load()
        existing_idx = next(
            (i for i, p in enumerate(catalog.products) if p.id == product.id), None
        )

        product.updated_at = datetime.now(timezone.utc).isoformat()

        if existing_idx is not None:
            catalog.products[existing_idx] = product
        else:
            catalog.products.append(product)

        await self._store.save(catalog)
        return product

    async def soft_delete(self, product_id: str) -> bool:
        """Mark product as soft-deleted by setting deleted_at timestamp."""
        catalog = await self._store.load()
        product = next((p for p in catalog.products if p.id == product_id), None)
        if not product:
            return False

        product.deleted_at = datetime.now(timezone.utc).isoformat()
        product.is_active = False
        await self._store.save(catalog)
        return True
