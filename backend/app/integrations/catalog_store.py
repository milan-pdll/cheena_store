"""Storage abstractions and implementations for single-file JSON catalog persistence."""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timezone
import json
import logging
import os
import shutil
from typing import Optional

from app.core.config import get_settings
from app.schemas.catalog import CatalogDocument

logger = logging.getLogger(__name__)


class CatalogStore(ABC):
    """Abstract interface for catalogue document persistence."""

    @abstractmethod
    async def load(self) -> CatalogDocument:
        """Load and parse the catalogue document."""
        pass

    @abstractmethod
    async def save(self, catalog: CatalogDocument) -> None:
        """Validate and persist the catalogue document."""
        pass


class LocalJsonCatalogStore(CatalogStore):
    """Local filesystem catalogue store with atomic writes and timestamped rotating backups."""

    def __init__(
        self,
        file_path: Optional[str] = None,
        backup_dir: Optional[str] = None,
        max_backups: Optional[int] = None,
    ):
        settings = get_settings()
        self.file_path = file_path or settings.CATALOG_FILE_PATH
        self.backup_dir = backup_dir or settings.CATALOG_BACKUP_DIR
        self.max_backups = max_backups or settings.CATALOG_MAX_BACKUPS
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure destination and backup directories exist."""
        os.makedirs(os.path.dirname(os.path.abspath(self.file_path)), exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def _sync_read(self) -> str:
        with open(self.file_path, mode="r", encoding="utf-8") as f:
            return f.read()

    def _sync_write(self, payload: str) -> None:
        # Atomic file write via temp file then atomic rename
        temp_path = f"{self.file_path}.tmp"
        with open(temp_path, mode="w", encoding="utf-8") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, self.file_path)

    async def load(self) -> CatalogDocument:
        """Read catalog JSON from local file or return empty document if not yet initialized."""
        if not os.path.exists(self.file_path):
            logger.info("Catalog file %s not found. Initializing empty catalog.", self.file_path)
            empty_doc = CatalogDocument()
            await self.save(empty_doc)
            return empty_doc

        raw_text = await asyncio.to_thread(self._sync_read)
        data = json.loads(raw_text)
        return CatalogDocument.model_validate(data)

    async def save(self, catalog: CatalogDocument) -> None:
        """Atomically write validated catalog to disk and rotate backups."""
        # 1. Validate through Pydantic
        payload = catalog.model_dump_json(indent=2)

        # 2. Backup existing file if present
        if os.path.exists(self.file_path):
            await asyncio.to_thread(self._create_backup)

        # 3. Non-blocking atomic write
        await asyncio.to_thread(self._sync_write, payload)
        logger.info("Catalog saved atomically to %s", self.file_path)

    def _create_backup(self) -> None:
        """Create timestamped snapshot and maintain max backup count."""
        try:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            backup_filename = f"catalog_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            shutil.copy2(self.file_path, backup_path)

            # Cleanup older backups
            existing_backups = sorted(
                [
                    os.path.join(self.backup_dir, f)
                    for f in os.listdir(self.backup_dir)
                    if f.startswith("catalog_") and f.endswith(".json")
                ]
            )
            while len(existing_backups) > self.max_backups:
                oldest = existing_backups.pop(0)
                try:
                    os.remove(oldest)
                except OSError:
                    pass
        except Exception as e:
            logger.warning("Failed to rotate catalog backup: %s", e)


class CloudinaryRawCatalogStore(CatalogStore):
    """Cloudinary raw asset store for ephemeral server environments."""

    def __init__(self):
        settings = get_settings()
        import cloudinary

        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )
        self.raw_id = settings.CLOUDINARY_RAW_CATALOG_ID

    async def load(self) -> CatalogDocument:
        """Download raw JSON file from Cloudinary CDN."""
        import httpx
        import cloudinary.utils

        url, _ = cloudinary.utils.cloudinary_url(
            self.raw_id, resource_type="raw", type="upload"
        )
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url)
                if res.status_code == 404:
                    logger.info("Cloudinary raw catalog not found. Initializing empty.")
                    doc = CatalogDocument()
                    await self.save(doc)
                    return doc
                res.raise_for_status()
                data = res.json()
                return CatalogDocument.model_validate(data)
        except Exception as e:
            logger.error("Error reading raw catalog from Cloudinary: %s. Using default.", e)
            return CatalogDocument()

    async def save(self, catalog: CatalogDocument) -> None:
        """Upload raw JSON payload to Cloudinary with fixed public_id and overwrite."""
        import cloudinary.uploader

        payload = catalog.model_dump_json(indent=2)

        def _sync_upload():
            return cloudinary.uploader.upload(
                payload.encode("utf-8"),
                public_id=self.raw_id,
                resource_type="raw",
                overwrite=True,
                invalidate=True,
            )

        await asyncio.to_thread(_sync_upload)
        logger.info("Saved catalog to Cloudinary raw asset %s", self.raw_id)


class CachedCatalogStore(CatalogStore):
    """Thread-safe, in-memory caching decorator around any underlying CatalogStore."""

    def __init__(self, backend_store: CatalogStore):
        self._backend = backend_store
        self._cache: Optional[CatalogDocument] = None
        self._lock = asyncio.Lock()

    async def load(self) -> CatalogDocument:
        """Return cached copy or load from backend store if not yet cached."""
        if self._cache is not None:
            return self._cache

        async with self._lock:
            # Double-check lock pattern
            if self._cache is None:
                self._cache = await self._backend.load()
            return self._cache

    async def save(self, catalog: CatalogDocument) -> None:
        """Acquire lock, validate, persist to underlying store, and update memory cache."""
        async with self._lock:
            await self._backend.save(catalog)
            self._cache = catalog

    async def invalidate(self) -> None:
        """Force cache invalidation."""
        async with self._lock:
            self._cache = None


_global_catalog_store: Optional[CachedCatalogStore] = None


def get_catalog_store() -> CachedCatalogStore:
    """Singleton provider for the configured CachedCatalogStore."""
    global _global_catalog_store
    if _global_catalog_store is None:
        settings = get_settings()
        if settings.CATALOG_STORE == "cloudinary":
            backend = CloudinaryRawCatalogStore()
        else:
            backend = LocalJsonCatalogStore()
        _global_catalog_store = CachedCatalogStore(backend)
    return _global_catalog_store
