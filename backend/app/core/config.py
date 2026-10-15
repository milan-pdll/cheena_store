"""Application configuration and environment settings management using Pydantic Settings."""

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "Football Store API"
    API_V1_STR: str = "/api/v1"

    # Catalog Storage Settings (Database-Free)
    CATALOG_STORE: str = "local"  # "local" or "cloudinary"
    CATALOG_FILE_PATH: str = "./data/catalog.json"
    CATALOG_BACKUP_DIR: str = "./data/backups"
    CATALOG_MAX_BACKUPS: int = 10

    # Single Admin Security & Auth
    ADMIN_EMAIL: str = "admin@footballstore.com"
    ADMIN_PASSWORD_HASH: str = (
        "$2b$12$e6xU7O2B5O7Wl2rSvyFz4eKqvM1hF4yQ0N8sE4uP4nZ5h6g7j8k9l"
    )
    SECRET_KEY: str = "dev_secret_key_change_in_production_32chars_min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Cloudinary Integration (used for raw catalog sync in cloud and images)
    CLOUDINARY_CLOUD_NAME: str = "demo"
    CLOUDINARY_API_KEY: str = "123456789012345"
    CLOUDINARY_API_SECRET: str = "sample_secret_key"
    CLOUDINARY_RAW_CATALOG_ID: str = "catalog/catalog.json"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v  # type: ignore
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()
