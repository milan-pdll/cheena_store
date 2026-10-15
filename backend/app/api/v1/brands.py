"""Public brand endpoints for brand filtering and logo strip presentation."""

from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_taxonomy_service
from app.schemas.catalog import Brand
from app.services.taxonomy_service import TaxonomyService

router = APIRouter(prefix="/brands", tags=["Public Brands"])


@router.get("", response_model=List[Brand], status_code=status.HTTP_200_OK)
async def list_brands(
    service: TaxonomyService = Depends(get_taxonomy_service),
) -> List[Brand]:
    """Retrieve all active manufacturer brands."""
    return await service.list_public_brands()
