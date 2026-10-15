"""Admin media endpoints providing client-side direct upload signatures and asset removal."""

from typing import Any, Dict
from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_image_storage
from app.core.security import get_current_admin
from app.integrations.image_storage import ImageStorage

router = APIRouter(prefix="/admin/media", tags=["Admin Media"])


@router.post("/upload-signature", status_code=status.HTTP_200_OK)
async def generate_upload_signature(
    folder: str = Query("products", description="Cloudinary destination folder"),
    storage: ImageStorage = Depends(get_image_storage),
    _: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Generate signature and credentials for client-side direct upload to Cloudinary."""
    return storage.generate_upload_signature(folder=folder)


@router.delete("/{public_id:path}", status_code=status.HTTP_200_OK)
async def delete_image(
    public_id: str,
    storage: ImageStorage = Depends(get_image_storage),
    _: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Delete an image asset from Cloudinary storage."""
    success = await storage.delete_image(public_id)
    return {"public_id": public_id, "deleted": success}
