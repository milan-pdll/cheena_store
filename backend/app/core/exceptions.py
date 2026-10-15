"""Custom application exceptions and centralized error representations."""

from typing import Any, Optional
from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception with error codes and optional details."""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = "APP_ERROR",
        details: Optional[Any] = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={"message": message, "error_code": error_code, "details": details},
        )


class NotFoundException(AppException):
    """Resource not found exception."""

    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error_code="NOT_FOUND",
            details=details,
        )


class UnauthorizedException(AppException):
    """Authentication failed or missing token."""

    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="UNAUTHORIZED",
        )


class BadRequestException(AppException):
    """Invalid client request data."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            error_code="BAD_REQUEST",
            details=details,
        )
