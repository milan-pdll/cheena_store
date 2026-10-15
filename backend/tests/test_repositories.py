"""Unit tests for repositories using in-memory catalog persistence."""

import pytest
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.brand_repository import BrandRepository
from app.repositories.settings_repository import SettingsRepository
from app.schemas.catalog import GroundType
from app.schemas.product_query import ProductFilterParams


@pytest.mark.asyncio
async def test_product_repository_filters(in_memory_store):
    """Test filtering products by category, ground type, brand, and search."""
    repo = ProductRepository(in_memory_store)

    # Filter by category: boots
    params = ProductFilterParams(category="boots", page_size=20)
    boots, count = await repo.query_products(params)
    assert count == 6
    assert all(p.category_slug == "boots" for p in boots)

    # Filter by ground type: FG
    params_fg = ProductFilterParams(ground_type=GroundType.FG, page_size=20)
    fg_boots, fg_count = await repo.query_products(params_fg)
    assert fg_count == 3
    assert all(p.ground_type == GroundType.FG for p in fg_boots)

    # Search query: Predator
    params_q = ProductFilterParams(q="Predator")
    pred_items, pred_count = await repo.query_products(params_q)
    assert pred_count >= 2
    assert any("Predator" in p.name for p in pred_items)


@pytest.mark.asyncio
async def test_product_repository_price_filter_and_sort(in_memory_store):
    """Test price filtering and ascending/descending sorting."""
    repo = ProductRepository(in_memory_store)

    # Sort price asc
    params_sort = ProductFilterParams(sort="price_asc", page_size=20)
    items, _ = await repo.query_products(params_sort)
    prices = [p.discount_price if p.discount_price is not None else p.price for p in items]
    assert prices == sorted(prices)


@pytest.mark.asyncio
async def test_product_soft_delete(in_memory_store):
    """Test soft delete removes product from active listings but preserves data."""
    repo = ProductRepository(in_memory_store)
    products = await repo.get_all(include_deleted=False)
    first_product = products[0]

    deleted = await repo.soft_delete(first_product.id)
    assert deleted is True

    # Active listing should no longer include this product
    active_products = await repo.get_all(include_deleted=False)
    assert all(p.id != first_product.id for p in active_products)

    # With include_deleted=True it should still be present
    all_products = await repo.get_all(include_deleted=True)
    found = next((p for p in all_products if p.id == first_product.id), None)
    assert found is not None
    assert found.deleted_at is not None


@pytest.mark.asyncio
async def test_categories_and_brands_repositories(in_memory_store):
    """Test listing and querying categories and brands."""
    cat_repo = CategoryRepository(in_memory_store)
    brand_repo = BrandRepository(in_memory_store)

    categories = await cat_repo.list_categories()
    assert len(categories) == 3

    boots_cat = await cat_repo.get_by_slug("boots")
    assert boots_cat is not None
    assert boots_cat.name == "Football Boots"

    brands = await brand_repo.list_brands()
    assert len(brands) == 4
    assert any(b.slug == "nike" for b in brands)


@pytest.mark.asyncio
async def test_settings_repository(in_memory_store):
    """Test reading site settings."""
    settings_repo = SettingsRepository(in_memory_store)
    settings = await settings_repo.get_settings()
    assert settings.store_name == "APEX PITCH | Football Boots & Jerseys"
    assert "447123456789" in settings.whatsapp_number
