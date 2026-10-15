"""Product business logic service handling catalog filtering, slug lookups, admin mutations, and bulk actions."""

from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.core.exceptions import BadRequestException, NotFoundException
from app.repositories.product_repository import ProductRepository
from app.schemas.admin import (
    BulkActionType,
    BulkProductActionRequest,
    ProductCreateRequest,
    ProductUpdateRequest,
)
from app.schemas.catalog import Product, ProductImage
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

    async def list_admin_products(
        self, include_deleted: bool = False
    ) -> List[Product]:
        """Fetch all products for the admin table view."""
        return await self._repo.get_all(include_deleted=include_deleted)

    async def get_by_slug(self, slug: str) -> Product:
        """Retrieve single active product by slug, or raise NotFoundException."""
        product = await self._repo.get_by_slug(slug)
        if not product:
            raise NotFoundException(f"Product with slug '{slug}' not found.")
        return product

    async def get_by_id(self, product_id: str, include_deleted: bool = False) -> Product:
        """Retrieve product by UUID, or raise NotFoundException."""
        product = await self._repo.get_by_id(product_id, include_deleted=include_deleted)
        if not product:
            raise NotFoundException(f"Product with id '{product_id}' not found.")
        return product

    async def create_product(self, req: ProductCreateRequest) -> Product:
        """Create new product ensuring slug uniqueness."""
        existing = await self._repo.get_by_slug(req.slug)
        if existing:
            raise BadRequestException(f"A product with slug '{req.slug}' already exists.")

        now = datetime.now(timezone.utc).isoformat()
        product = Product(
            id=str(uuid4()),
            name=req.name,
            slug=req.slug,
            description=req.description,
            category_slug=req.category_slug,
            brand_slug=req.brand_slug,
            price=req.price,
            discount_price=req.discount_price,
            currency=req.currency,
            ground_type=req.ground_type,
            is_active=req.is_active,
            is_featured=req.is_featured,
            display_order=req.display_order,
            images=req.images,
            variants=req.variants,
            created_at=now,
            updated_at=now,
        )
        return await self._repo.save_product(product)

    async def update_product(
        self, product_id: str, req: ProductUpdateRequest
    ) -> Product:
        """Update fields on an existing product."""
        product = await self.get_by_id(product_id, include_deleted=True)

        if req.slug and req.slug != product.slug:
            existing = await self._repo.get_by_slug(req.slug)
            if existing and existing.id != product_id:
                raise BadRequestException(f"Slug '{req.slug}' is already taken.")
            product.slug = req.slug

        if req.name is not None:
            product.name = req.name
        if req.description is not None:
            product.description = req.description
        if req.category_slug is not None:
            product.category_slug = req.category_slug
        if req.brand_slug is not None:
            product.brand_slug = req.brand_slug
        if req.price is not None:
            product.price = req.price
        if req.discount_price is not None:
            product.discount_price = req.discount_price
        if req.currency is not None:
            product.currency = req.currency
        if req.ground_type is not None:
            product.ground_type = req.ground_type
        if req.is_active is not None:
            product.is_active = req.is_active
        if req.is_featured is not None:
            product.is_featured = req.is_featured
        if req.display_order is not None:
            product.display_order = req.display_order
        if req.images is not None:
            product.images = req.images
        if req.variants is not None:
            product.variants = req.variants

        return await self._repo.save_product(product)

    async def soft_delete(self, product_id: str) -> bool:
        """Soft-delete product by setting deleted_at."""
        success = await self._repo.soft_delete(product_id)
        if not success:
            raise NotFoundException(f"Product '{product_id}' not found.")
        return True

    async def duplicate_product(
        self, product_id: str, new_name: str, new_slug: str
    ) -> Product:
        """Clone an existing product with new IDs, name, and slug."""
        source = await self.get_by_id(product_id, include_deleted=True)
        existing = await self._repo.get_by_slug(new_slug)
        if existing:
            raise BadRequestException(f"Slug '{new_slug}' is already taken.")

        now = datetime.now(timezone.utc).isoformat()
        cloned_images = [
            ProductImage(
                id=str(uuid4()),
                url=img.url,
                public_id=img.public_id,
                position=img.position,
                is_primary=img.is_primary,
            )
            for img in source.images
        ]
        cloned_variants = [
            v.model_copy(update={"id": str(uuid4()), "sku": f"{v.sku}-COPY"})
            for v in source.variants
        ]

        cloned = Product(
            id=str(uuid4()),
            name=new_name,
            slug=new_slug,
            description=source.description,
            category_slug=source.category_slug,
            brand_slug=source.brand_slug,
            price=source.price,
            discount_price=source.discount_price,
            currency=source.currency,
            ground_type=source.ground_type,
            is_active=False,  # Draft by default upon duplication
            is_featured=False,
            display_order=source.display_order + 1,
            images=cloned_images,
            variants=cloned_variants,
            created_at=now,
            updated_at=now,
        )
        return await self._repo.save_product(cloned)

    async def bulk_action(self, req: BulkProductActionRequest) -> Dict[str, Any]:
        """Perform batch operations on products."""
        all_products = await self._repo.get_all(include_deleted=True)
        id_set = set(req.product_ids)
        affected = 0

        for p in all_products:
            if p.id in id_set:
                if req.action == BulkActionType.DELETE:
                    p.deleted_at = datetime.now(timezone.utc).isoformat()
                    p.is_active = False
                    affected += 1
                elif req.action == BulkActionType.ACTIVATE:
                    p.is_active = True
                    p.deleted_at = None
                    affected += 1
                elif req.action == BulkActionType.DEACTIVATE:
                    p.is_active = False
                    affected += 1
                elif req.action == BulkActionType.UPDATE_PRICE and req.price_modifier:
                    multiplier = 1.0 + (req.price_modifier / 100.0)
                    p.price = round(p.price * multiplier, 2)
                    if p.discount_price:
                        p.discount_price = round(p.discount_price * multiplier, 2)
                    affected += 1
                await self._repo.save_product(p)

        return {"action": req.action.value, "affected_count": affected}

    async def reorder_featured(self, ordered_ids: List[str]) -> List[Product]:
        """Update display ordering for products."""
        all_products = await self._repo.get_all(include_deleted=False)
        order_map = {pid: idx for idx, pid in enumerate(ordered_ids)}

        for p in all_products:
            if p.id in order_map:
                p.display_order = order_map[p.id]
                p.is_featured = True
                await self._repo.save_product(p)

        return await self._repo.get_all(include_deleted=False)

    async def reorder_images(
        self, product_id: str, ordered_image_ids: List[str], primary_image_id: Optional[str] = None
    ) -> Product:
        """Reorder gallery images and designate primary display image."""
        product = await self.get_by_id(product_id, include_deleted=True)
        img_map = {img.id: img for img in product.images}

        reordered: List[ProductImage] = []
        for idx, img_id in enumerate(ordered_image_ids):
            if img_id in img_map:
                img = img_map[img_id]
                img.position = idx
                img.is_primary = (img.id == primary_image_id) if primary_image_id else (idx == 0)
                reordered.append(img)

        # Append any unmentioned images at the end
        mentioned_ids = set(ordered_image_ids)
        for img in product.images:
            if img.id not in mentioned_ids:
                img.position = len(reordered)
                img.is_primary = False
                reordered.append(img)

        product.images = reordered
        return await self._repo.save_product(product)
