"""Stock inventory business service managing SKU stock adjustments and low-stock alerts."""

from typing import Any, Dict, List
from app.core.exceptions import NotFoundException
from app.repositories.product_repository import ProductRepository
from app.schemas.catalog import ProductVariant


class StockService:
    """Business logic for SKU variant inventory levels and alerts."""

    def __init__(self, product_repo: ProductRepository):
        self._repo = product_repo

    async def update_variant_stock(
        self, product_id: str, variant_id: str, new_quantity: int
    ) -> ProductVariant:
        """Set absolute stock quantity for a variant."""
        product = await self._repo.get_by_id(product_id, include_deleted=True)
        if not product:
            raise NotFoundException(f"Product '{product_id}' not found.")

        variant = next((v for v in product.variants if v.id == variant_id), None)
        if not variant:
            raise NotFoundException(f"Variant '{variant_id}' not found on product.")

        variant.stock_quantity = max(0, new_quantity)
        await self._repo.save_product(product)
        return variant

    async def get_low_stock_alerts(
        self, threshold: int = 3
    ) -> List[Dict[str, Any]]:
        """Identify items with inventory at or below the warning threshold."""
        products = await self._repo.get_all(include_deleted=False)
        alerts = []

        for p in products:
            for v in p.variants:
                if v.stock_quantity <= threshold:
                    alerts.append(
                        {
                            "product_id": p.id,
                            "product_name": p.name,
                            "variant_id": v.id,
                            "sku": v.sku,
                            "size": v.size,
                            "color": v.color,
                            "stock_quantity": v.stock_quantity,
                            "is_out_of_stock": v.stock_quantity == 0,
                        }
                    )
        return alerts
