"""Integration tests for admin stock management and low inventory alerts."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_stock_patch_and_alerts(client: AsyncClient, admin_headers: dict):
    """Test updating variant stock and checking low stock alerts."""
    # 1. Fetch product to get product and variant ID
    list_res = await client.get("/api/v1/admin/products", headers=admin_headers)
    products = list_res.json()
    first_prod = products[0]
    first_variant = first_prod["variants"][0]

    # 2. Patch variant stock to 1
    patch_res = await client.patch(
        f"/api/v1/admin/stock/{first_prod['id']}/{first_variant['id']}",
        json={"stock_quantity": 1},
        headers=admin_headers,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["stock_quantity"] == 1

    # 3. Check low stock alerts
    alerts_res = await client.get("/api/v1/admin/stock/alerts?threshold=2", headers=admin_headers)
    assert alerts_res.status_code == 200
    alerts = alerts_res.json()
    assert any(a["variant_id"] == first_variant["id"] for a in alerts)


@pytest.mark.asyncio
async def test_admin_bulk_stock_update(client: AsyncClient, admin_headers: dict):
    """Test bulk updating multiple variant stock levels."""
    list_res = await client.get("/api/v1/admin/products", headers=admin_headers)
    products = list_res.json()
    v1 = products[0]["variants"][0]
    v2 = products[1]["variants"][0]

    payload = {
        "updates": [
            {"product_id": products[0]["id"], "variant_id": v1["id"], "stock_quantity": 15},
            {"product_id": products[1]["id"], "variant_id": v2["id"], "stock_quantity": 20},
        ]
    }
    bulk_res = await client.post("/api/v1/admin/stock/bulk", json=payload, headers=admin_headers)
    assert bulk_res.status_code == 200
    assert bulk_res.json()["updated_count"] == 2
