"""Health check endpoint probe for monitoring and deployment readiness."""

from typing import Dict
from fastapi import APIRouter, status

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """Return API health status."""
    return {"status": "healthy", "service": "football-store-api", "version": "1.0.0"}
