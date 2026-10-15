"""Admin inventory management endpoints for inline stock editing and threshold monitoring."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_stock_service
from app.core.security import get_current_admin
from app.schemas.admin import BulkStockUpdateRequest, VariantStockUpdateRequest
from app.schemas.catalog import ProductVariant
from app.services.stock_service import StockService

router = APIRouter(prefix="/admin/stock", tags=["Admin Stock"])


@router.patch("/{product_id}/{variant_id}", response_model=ProductVariant, status_code=status.HTTP_200_OK)
async def update_variant_stock(
    product_id: str,
    variant_id: str,
    payload: VariantStockUpdateRequest,
    service: StockService = Depends(get_stock_service),
    _: str = Depends(get_current_admin),
) -> ProductVariant:
    """Set absolute stock quantity for a single product variant."""
    return await service.update_variant_stock(product_id, variant_id, payload.stock_quantity)


@router.post("/bulk", status_code=status.HTTP_200_OK)
async def bulk_update_stock(
    payload: BulkStockUpdateRequest,
    service: StockService = Depends(get_stock_service),
    _: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Batch adjust stock quantities across multiple variants."""
    return await service.bulk_update_stock(payload.updates)


@router.get("/alerts", status_code=status.HTTP_200_OK)
async def get_stock_alerts(
    threshold: int = Query(3, ge=0, description="Warning threshold for low stock"),
    service: StockService = Depends(get_stock_service),
    _: str = Depends(get_current_admin),
) -> List[Dict[str, Any]]:
    """Retrieve all variants with stock at or below threshold."""
    return await service.get_low_stock_alerts(threshold=threshold)
