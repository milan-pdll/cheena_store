"""Integration tests for all public REST API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_products_list(client: AsyncClient):
    """Test public listing of products with pagination."""
    response = await client.get("/api/v1/products?page=1&page_size=6")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) == 6
    assert data["total"] == 12


@pytest.mark.asyncio
async def test_get_products_filtered_by_category(client: AsyncClient):
    """Test filtering public products by category."""
    response = await client.get("/api/v1/products?category=jerseys")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 4
    for item in data["items"]:
        assert item["category_slug"] == "jerseys"


@pytest.mark.asyncio
async def test_get_products_filtered_by_ground_type(client: AsyncClient):
    """Test filtering boots by ground configuration."""
    response = await client.get("/api/v1/products?ground_type=AG")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["ground_type"] == "AG"


@pytest.mark.asyncio
async def test_get_product_detail_success(client: AsyncClient):
    """Test fetching product detail by slug."""
    slug = "real-madrid-2024-25-authentic-home-jersey"
    response = await client.get(f"/api/v1/products/{slug}")
    assert response.status_code == 200
    product = response.json()
    assert product["slug"] == slug
    assert product["brand_slug"] == "adidas"
    assert len(product["variants"]) > 0


@pytest.mark.asyncio
async def test_get_product_detail_not_found(client: AsyncClient):
    """Test 404 response on non-existent product slug."""
    response = await client.get("/api/v1/products/does-not-exist")
    assert response.status_code == 404
    error = response.json()
    assert error["error_code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    """Test fetching public categories."""
    response = await client.get("/api/v1/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 3
    slugs = [c["slug"] for c in categories]
    assert "boots" in slugs
    assert "jerseys" in slugs


@pytest.mark.asyncio
async def test_get_brands(client: AsyncClient):
    """Test fetching public brands."""
    response = await client.get("/api/v1/brands")
    assert response.status_code == 200
    brands = response.json()
    assert len(brands) == 4
    slugs = [b["slug"] for b in brands]
    assert "nike" in slugs
    assert "adidas" in slugs


@pytest.mark.asyncio
async def test_get_public_settings(client: AsyncClient):
    """Test fetching public site settings."""
    response = await client.get("/api/v1/settings/public")
    assert response.status_code == 200
    settings = response.json()
    assert "whatsapp_number" in settings
    assert settings["whatsapp_number"] == "447123456789"
    assert "hero_title" in settings
