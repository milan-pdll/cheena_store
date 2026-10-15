"""Integration tests for admin authentication, token refresh, and route protection."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_login_success_and_refresh(client: AsyncClient):
    """Test successful admin login and token refresh flow."""
    # 1. Login
    login_res = await client.post(
        "/api/v1/admin/login",
        json={"email": "admin@footballstore.com", "password": "AdminSecurePassword123!"},
    )
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    assert "refresh_token" in data

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    # 2. Access /admin/me with access token
    me_res = await client.get(
        "/api/v1/admin/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "admin@footballstore.com"

    # 3. Refresh access token
    ref_res = await client.post(
        "/api/v1/admin/refresh",
        json={"refresh_token": refresh_token},
    )
    assert ref_res.status_code == 200
    ref_data = ref_res.json()
    assert "access_token" in ref_data


@pytest.mark.asyncio
async def test_admin_login_invalid_password(client: AsyncClient):
    """Test login failure with wrong password."""
    res = await client.post(
        "/api/v1/admin/login",
        json={"email": "admin@footballstore.com", "password": "WrongPassword999!"},
    )
    assert res.status_code == 401
    assert res.json()["error_code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_protected_route_rejects_missing_token(client: AsyncClient):
    """Test that protected admin route denies access without Bearer token."""
    res = await client.get("/api/v1/admin/me")
    assert res.status_code == 401
