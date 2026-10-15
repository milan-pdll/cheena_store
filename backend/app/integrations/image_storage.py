"""Image storage provider abstraction and Cloudinary implementation for direct client signatures and media deletion."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
import time
from typing import Any, Dict, Optional

from app.core.config import get_settings


class ImageStorage(ABC):
    """Abstract interface for image upload signatures, transformations, and deletion."""

    @abstractmethod
    def generate_upload_signature(self, folder: str = "products") -> Dict[str, Any]:
        """Generate secure timestamped signature for client-side direct upload."""
        pass

    @abstractmethod
    async def delete_image(self, public_id: str) -> bool:
        """Delete image from remote storage provider."""
        pass

    @abstractmethod
    def get_optimized_url(
        self, public_id: str, width: Optional[int] = None, height: Optional[int] = None
    ) -> str:
        """Generate CDN delivery URL with transformations."""
        pass


class CloudinaryImageStorage(ImageStorage):
    """Cloudinary implementation supporting direct client upload signatures and asset management."""

    def __init__(self):
        self.settings = get_settings()
        import cloudinary
        import cloudinary.utils
        import cloudinary.uploader

        cloudinary.config(
            cloud_name=self.settings.CLOUDINARY_CLOUD_NAME,
            api_key=self.settings.CLOUDINARY_API_KEY,
            api_secret=self.settings.CLOUDINARY_API_SECRET,
            secure=True,
        )

    def generate_upload_signature(self, folder: str = "products") -> Dict[str, Any]:
        """Generate API signature for secure client-side direct upload to Cloudinary."""
        import cloudinary.utils

        timestamp = int(time.time())
        params_to_sign = {
            "timestamp": timestamp,
            "folder": folder,
        }
        signature = cloudinary.utils.api_sign_request(
            params_to_sign, self.settings.CLOUDINARY_API_SECRET
        )

        return {
            "signature": signature,
            "timestamp": timestamp,
            "api_key": self.settings.CLOUDINARY_API_KEY,
            "cloud_name": self.settings.CLOUDINARY_CLOUD_NAME,
            "folder": folder,
            "upload_url": f"https://api.cloudinary.com/v1_1/{self.settings.CLOUDINARY_CLOUD_NAME}/image/upload",
        }

    async def delete_image(self, public_id: str) -> bool:
        """Delete image asset from Cloudinary."""
        import asyncio
        import cloudinary.uploader

        def _sync_destroy():
            result = cloudinary.uploader.destroy(public_id, invalidate=True)
            return result.get("result") in ["ok", "not found"]

        return await asyncio.to_thread(_sync_destroy)

    def get_optimized_url(
        self, public_id: str, width: Optional[int] = None, height: Optional[int] = None
    ) -> str:
        """Build optimized responsive Cloudinary CDN URL."""
        import cloudinary.utils

        transformations = {"fetch_format": "auto", "quality": "auto"}
        if width:
            transformations["width"] = width
        if height:
            transformations["height"] = height
            transformations["crop"] = "fill"

        url, _ = cloudinary.utils.cloudinary_url(public_id, **transformations)
        return url
