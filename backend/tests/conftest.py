"""Pytest fixtures providing an in-memory CatalogStore and AsyncClient for API testing."""

from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.dependencies import get_store
from app.integrations.catalog_store import CatalogStore
from app.main import app
from app.schemas.catalog import CatalogDocument
from scripts.seed_catalog import create_sample_catalog


class InMemoryCatalogStore(CatalogStore):
    """In-memory implementation of CatalogStore for isolated, lightning-fast tests."""

    def __init__(self, initial_catalog: CatalogDocument):
        self._catalog = initial_catalog.model_copy(deep=True)

    async def load(self) -> CatalogDocument:
        return self._catalog.model_copy(deep=True)

    async def save(self, catalog: CatalogDocument) -> None:
        self._catalog = catalog.model_copy(deep=True)


@pytest.fixture
def sample_catalog_document() -> CatalogDocument:
    """Fixture providing a fresh sample catalog document."""
    return create_sample_catalog()


@pytest.fixture
def in_memory_store(sample_catalog_document: CatalogDocument) -> InMemoryCatalogStore:
    """Fixture providing an isolated in-memory catalog store."""
    return InMemoryCatalogStore(sample_catalog_document)


@pytest_asyncio.fixture
async def client(in_memory_store: InMemoryCatalogStore) -> AsyncGenerator[AsyncClient, None]:
    """Fixture providing an AsyncClient with overridden catalog store."""
    from app.core.security import _login_attempts
    _login_attempts.clear()

    app.dependency_overrides[get_store] = lambda: in_memory_store
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def admin_headers() -> dict:
    """Fixture providing valid authorization header directly."""
    from app.core.config import get_settings
    from app.core.security import create_access_token

    settings = get_settings()
    token = create_access_token({"sub": settings.ADMIN_EMAIL})
    return {"Authorization": f"Bearer {token}"}

