"""FastAPI dependency injection providers for repositories, services, and storage instances."""

from fastapi import Depends

from app.integrations.catalog_store import CatalogStore, get_catalog_store
from app.repositories.brand_repository import BrandRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.settings_repository import SettingsRepository
from app.services.product_service import ProductService
from app.services.settings_service import SettingsService
from app.services.stock_service import StockService
from app.services.taxonomy_service import TaxonomyService


def get_store() -> CatalogStore:
    """Provide the singleton CatalogStore instance."""
    return get_catalog_store()


def get_product_repository(
    store: CatalogStore = Depends(get_store),
) -> ProductRepository:
    """Provide ProductRepository instance."""
    return ProductRepository(store)


def get_category_repository(
    store: CatalogStore = Depends(get_store),
) -> CategoryRepository:
    """Provide CategoryRepository instance."""
    return CategoryRepository(store)


def get_brand_repository(
    store: CatalogStore = Depends(get_store),
) -> BrandRepository:
    """Provide BrandRepository instance."""
    return BrandRepository(store)


def get_settings_repository(
    store: CatalogStore = Depends(get_store),
) -> SettingsRepository:
    """Provide SettingsRepository instance."""
    return SettingsRepository(store)


def get_product_service(
    repo: ProductRepository = Depends(get_product_repository),
) -> ProductService:
    """Provide ProductService instance."""
    return ProductService(repo)


def get_stock_service(
    repo: ProductRepository = Depends(get_product_repository),
) -> StockService:
    """Provide StockService instance."""
    return StockService(repo)


def get_settings_service(
    repo: SettingsRepository = Depends(get_settings_repository),
) -> SettingsService:
    """Provide SettingsService instance."""
    return SettingsService(repo)


def get_taxonomy_service(
    cat_repo: CategoryRepository = Depends(get_category_repository),
    brand_repo: BrandRepository = Depends(get_brand_repository),
) -> TaxonomyService:
    """Provide TaxonomyService instance."""
    return TaxonomyService(cat_repo, brand_repo)
