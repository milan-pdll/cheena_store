"""Public category endpoints for store navigation."""

from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_taxonomy_service
from app.schemas.catalog import Category
from app.services.taxonomy_service import TaxonomyService

router = APIRouter(prefix="/categories", tags=["Public Categories"])


@router.get("", response_model=List[Category], status_code=status.HTTP_200_OK)
async def list_categories(
    service: TaxonomyService = Depends(get_taxonomy_service),
) -> List[Category]:
    """Retrieve all active product categories."""
    return await service.list_public_categories()
