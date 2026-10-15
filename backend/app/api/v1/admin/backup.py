"""Admin catalog export and restore endpoints for backup management."""

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_store
from app.core.security import get_current_admin
from app.integrations.catalog_store import CatalogStore
from app.schemas.catalog import CatalogDocument

router = APIRouter(prefix="/admin/catalog", tags=["Admin Backup"])


@router.get("/export", response_model=CatalogDocument, status_code=status.HTTP_200_OK)
async def export_catalog(
    store: CatalogStore = Depends(get_store),
    _: str = Depends(get_current_admin),
) -> CatalogDocument:
    """Download entire validated catalog document for offline backup."""
    return await store.load()


@router.post("/import", response_model=CatalogDocument, status_code=status.HTTP_200_OK)
async def import_catalog(
    payload: CatalogDocument,
    store: CatalogStore = Depends(get_store),
    _: str = Depends(get_current_admin),
) -> CatalogDocument:
    """Restore catalogue from a validated backup document."""
    await store.save(payload)
    return payload
