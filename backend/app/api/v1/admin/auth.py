"""Admin authentication routes including login with rate-limiting and silent token refresh."""

from datetime import timedelta
from fastapi import APIRouter, Depends, Request, status

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException
from app.core.security import (
    check_login_rate_limit,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_admin,
    verify_password,
)
from app.schemas.admin import AdminLoginRequest, RefreshTokenRequest, TokenResponse

router = APIRouter(prefix="/admin", tags=["Admin Authentication"])
settings = get_settings()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: AdminLoginRequest,
    request: Request,
) -> TokenResponse:
    """Authenticate administrator and return signed JWT access and refresh token pair."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    check_login_rate_limit(client_ip)

    if payload.email.lower() != settings.ADMIN_EMAIL.lower() or not verify_password(
        payload.password, settings.ADMIN_PASSWORD_HASH
    ):
        raise UnauthorizedException("Invalid email or password.")

    token_data = {"sub": settings.ADMIN_EMAIL}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    payload: RefreshTokenRequest,
) -> TokenResponse:
    """Issue a new access token using a valid refresh token."""
    decoded = decode_token(payload.refresh_token)
    if decoded.get("type") != "refresh":
        raise UnauthorizedException("Invalid token type. Refresh token required.")

    sub = decoded.get("sub")
    if not sub or sub != settings.ADMIN_EMAIL:
        raise UnauthorizedException("Invalid refresh token credentials.")

    token_data = {"sub": sub}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(
    admin_email: str = Depends(get_current_admin),
):
    """Return currently authenticated administrator identity."""
    return {"email": admin_email, "role": "admin"}
