"""Cryptographic utilities for password hashing, JWT token management, and admin authentication."""

from datetime import datetime, timedelta, timezone
import time
from typing import Any, Dict, Optional

import bcrypt
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException

settings = get_settings()
security_scheme = HTTPBearer(auto_error=False)

# In-memory simple sliding-window rate limiter for login attempts: ip -> list of timestamps
_login_attempts: Dict[str, list[float]] = {}
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 60


def check_login_rate_limit(client_ip: str = "default") -> None:
    """Enforce rate limits on admin login endpoint to prevent brute force attacks."""
    now = time.time()
    attempts = _login_attempts.get(client_ip, [])
    # Filter attempts within the sliding window
    attempts = [t for t in attempts if now - t < LOGIN_WINDOW_SECONDS]
    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Too many login attempts. Please wait 60 seconds before trying again.",
                "error_code": "RATE_LIMITED",
            },
        )
    attempts.append(now)
    _login_attempts[client_ip] = attempts


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Generate a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Generate a signed JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a signed JWT token."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Authentication token has expired.")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid authentication token.")


async def get_current_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> str:
    """FastAPI dependency validating the caller has an active admin JWT."""
    if not credentials or not credentials.credentials:
        raise UnauthorizedException("Missing authentication credentials.")

    payload = decode_token(credentials.credentials)
    if payload.get("type") != "access":
        raise UnauthorizedException("Invalid token type. Access token required.")

    sub = payload.get("sub")
    if not sub or sub != settings.ADMIN_EMAIL:
        raise UnauthorizedException("Token does not match authorized admin.")

    return sub
