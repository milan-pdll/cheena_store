"""Unit tests for business services including stock alerts and slug lookup."""

import pytest
from app.core.exceptions import NotFoundException
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.services.stock_service import StockService


@pytest.mark.asyncio
async def test_product_service_get_by_slug(in_memory_store):
    """Test retrieving product by valid and invalid slug."""
    repo = ProductRepository(in_memory_store)
    service = ProductService(repo)

    product = await service.get_by_slug("nike-mercurial-superfly-10-elite-fg")
    assert product.name == "Nike Mercurial Superfly 10 Elite FG"

    with pytest.raises(NotFoundException):
        await service.get_by_slug("non-existent-product-slug")


@pytest.mark.asyncio
async def test_stock_service_update_and_alerts(in_memory_store):
    """Test stock adjustments and low-stock threshold queries."""
    repo = ProductRepository(in_memory_store)
    stock_service = StockService(repo)

    products = await repo.get_all()
    first_product = products[0]
    variant = first_product.variants[0]

    # Update variant stock to 1
    updated_variant = await stock_service.update_variant_stock(
        first_product.id, variant.id, 1
    )
    assert updated_variant.stock_quantity == 1

    # Check that it appears in low stock alerts (threshold = 2)
    alerts = await stock_service.get_low_stock_alerts(threshold=2)
    assert any(a["variant_id"] == variant.id for a in alerts)
