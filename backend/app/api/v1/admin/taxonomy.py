"""Admin categories and brands management endpoints."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_taxonomy_service
from app.core.security import get_current_admin
from app.schemas.admin import BrandUpsertRequest, CategoryUpsertRequest
from app.schemas.catalog import Brand, Category
from app.services.taxonomy_service import TaxonomyService

router = APIRouter(prefix="/admin", tags=["Admin Taxonomy"])


@router.get("/categories", response_model=List[Category], status_code=status.HTTP_200_OK)
async def list_admin_categories(
    service: TaxonomyService = Depends(get_taxonomy_service),
    _: str = Depends(get_current_admin),
) -> List[Category]:
    """List all categories for admin manager."""
    return await service.list_all_categories()


@router.post("/categories", response_model=Category, status_code=status.HTTP_200_OK)
@router.put("/categories", response_model=Category, status_code=status.HTTP_200_OK)
async def upsert_category(
    payload: CategoryUpsertRequest,
    service: TaxonomyService = Depends(get_taxonomy_service),
    _: str = Depends(get_current_admin),
) -> Category:
    """Create or update a category."""
    return await service.upsert_category(payload)


@router.delete("/categories/{slug}", status_code=status.HTTP_200_OK)
async def delete_category(
    slug: str,
    service: TaxonomyService = Depends(get_taxonomy_service),
    _: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Delete a category by slug."""
    await service.delete_category(slug)
    return {"slug": slug, "deleted": True}


@router.get("/brands", response_model=List[Brand], status_code=status.HTTP_200_OK)
async def list_admin_brands(
    service: TaxonomyService = Depends(get_taxonomy_service),
    _: str = Depends(get_current_admin),
) -> List[Brand]:
    """List all brands for admin manager."""
    return await service.list_all_brands()


@router.post("/brands", response_model=Brand, status_code=status.HTTP_200_OK)
@router.put("/brands", response_model=Brand, status_code=status.HTTP_200_OK)
async def upsert_brand(
    payload: BrandUpsertRequest,
    service: TaxonomyService = Depends(get_taxonomy_service),
    _: str = Depends(get_current_admin),
) -> Brand:
    """Create or update a brand."""
    return await service.upsert_brand(payload)


@router.delete("/brands/{slug}", status_code=status.HTTP_200_OK)
async def delete_brand(
    slug: str,
    service: TaxonomyService = Depends(get_taxonomy_service),
    _: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Delete a brand by slug."""
    await service.delete_brand(slug)
    return {"slug": slug, "deleted": True}
