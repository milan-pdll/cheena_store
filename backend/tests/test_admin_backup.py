"""Integration tests for catalog export and validated backup restore."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_export_and_import_backup(client: AsyncClient, admin_headers: dict):
    """Test downloading catalog backup and restoring it."""
    # 1. Export backup
    export_res = await client.get("/api/v1/admin/catalog/export", headers=admin_headers)
    assert export_res.status_code == 200
    catalog_backup = export_res.json()
    assert catalog_backup["schema_version"] == "1.0.0"
    assert len(catalog_backup["products"]) >= 12

    # 2. Modify title and import backup
    catalog_backup["site_settings"]["hero_title"] = "Custom Backup Restored Title"
    import_res = await client.post(
        "/api/v1/admin/catalog/import",
        json=catalog_backup,
        headers=admin_headers,
    )
    assert import_res.status_code == 200

    # 3. Verify public settings reflect the restored backup
    pub_settings = await client.get("/api/v1/settings/public")
    assert pub_settings.status_code == 200
    assert pub_settings.json()["hero_title"] == "Custom Backup Restored Title"
