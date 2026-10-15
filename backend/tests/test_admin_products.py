"""Integration tests for admin product mutations, duplication, bulk actions, and ordering."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_create_update_and_delete_product(client: AsyncClient, admin_headers: dict):
    """Test product creation, update, and soft deletion."""
    # 1. Create product
    create_payload = {
        "name": "New Test Boot Elite",
        "slug": "new-test-boot-elite",
        "description": "Top tier football boot for testing",
        "category_slug": "boots",
        "brand_slug": "nike",
        "price": 250.0,
        "discount_price": 220.0,
        "currency": "USD",
        "ground_type": "FG",
        "is_active": True,
        "is_featured": False,
        "display_order": 99,
        "images": [],
        "variants": [
            {"size": "UK 9", "color": "Black", "stock_quantity": 5, "sku": "TST-BOOT-09"}
        ],
    }
    create_res = await client.post("/api/v1/admin/products", json=create_payload, headers=admin_headers)
    assert create_res.status_code == 201
    created = create_res.json()
    product_id = created["id"]
    assert created["slug"] == "new-test-boot-elite"

    # 2. Update product
    update_res = await client.patch(
        f"/api/v1/admin/products/{product_id}",
        json={"price": 270.0, "is_featured": True},
        headers=admin_headers,
    )
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["price"] == 270.0
    assert updated["is_featured"] is True

    # 3. Duplicate product
    dup_res = await client.post(
        f"/api/v1/admin/products/{product_id}/duplicate",
        json={"new_name": "New Test Boot Elite (Special)", "new_slug": "new-test-boot-elite-special"},
        headers=admin_headers,
    )
    assert dup_res.status_code == 201
    assert dup_res.json()["slug"] == "new-test-boot-elite-special"

    # 4. Soft delete product
    del_res = await client.delete(f"/api/v1/admin/products/{product_id}", headers=admin_headers)
    assert del_res.status_code == 200

    # 5. Verify public endpoint does not list it
    pub_res = await client.get(f"/api/v1/products/{created['slug']}")
    assert pub_res.status_code == 404


@pytest.mark.asyncio
async def test_admin_bulk_actions(client: AsyncClient, admin_headers: dict):
    """Test bulk product operations."""
    list_res = await client.get("/api/v1/admin/products", headers=admin_headers)
    products = list_res.json()
    p1, p2 = products[0], products[1]

    # Bulk deactivate
    bulk_res = await client.post(
        "/api/v1/admin/products/bulk",
        json={"action": "deactivate", "product_ids": [p1["id"], p2["id"]]},
        headers=admin_headers,
    )
    assert bulk_res.status_code == 200
    assert bulk_res.json()["affected_count"] == 2
