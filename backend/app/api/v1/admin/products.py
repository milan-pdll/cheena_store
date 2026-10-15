"""Admin product management endpoints: CRUD, duplicate, bulk actions, and ordering."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_product_service
from app.core.security import get_current_admin
from app.schemas.admin import (
    BulkProductActionRequest,
    FeaturedReorderRequest,
    ImageReorderRequest,
    ProductCreateRequest,
    ProductDuplicateRequest,
    ProductUpdateRequest,
)
from app.schemas.catalog import Product
from app.services.product_service import ProductService

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])


@router.get("", response_model=List[Product], status_code=status.HTTP_200_OK)
async def list_admin_products(
    include_deleted: bool = Query(False, description="Include soft-deleted products"),
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> List[Product]:
    """List all products for admin dashboard table."""
    return await service.list_admin_products(include_deleted=include_deleted)


@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreateRequest,
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> Product:
    """Create a new product in the catalog."""
    return await service.create_product(payload)


@router.get("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> Product:
    """Retrieve full product detail by ID."""
    return await service.get_by_id(product_id, include_deleted=True)


@router.put("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
@router.patch("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> Product:
    """Update product details, status, or pricing."""
    return await service.update_product(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Soft-delete a product."""
    await service.soft_delete(product_id)
    return {"message": "Product successfully deleted.", "product_id": product_id}


@router.post("/{product_id}/duplicate", response_model=Product, status_code=status.HTTP_201_CREATED)
async def duplicate_product(
    product_id: str,
    payload: ProductDuplicateRequest,
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> Product:
    """Clone a product as a draft with a new name and slug."""
    return await service.duplicate_product(product_id, payload.new_name, payload.new_slug)


@router.post("/bulk", status_code=status.HTTP_200_OK)
async def bulk_action(
    payload: BulkProductActionRequest,
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Execute bulk delete, activate, deactivate, or price adjustments."""
    return await service.bulk_action(payload)


@router.put("/reorder", response_model=List[Product], status_code=status.HTTP_200_OK)
async def reorder_featured(
    payload: FeaturedReorderRequest,
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> List[Product]:
    """Reorder featured products by ID sequence."""
    return await service.reorder_featured(payload.ordered_ids)


@router.put("/{product_id}/images/reorder", response_model=Product, status_code=status.HTTP_200_OK)
async def reorder_images(
    product_id: str,
    payload: ImageReorderRequest,
    service: ProductService = Depends(get_product_service),
    _: str = Depends(get_current_admin),
) -> Product:
    """Reorder product gallery images and optionally assign new primary thumbnail."""
    return await service.reorder_images(
        product_id, payload.ordered_image_ids, payload.primary_image_id
    )
