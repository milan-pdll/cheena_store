"""Pydantic query parameters and response pagination schemas for public product catalog."""

from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.catalog import GroundType, Product


class ProductFilterParams(BaseModel):
    """Query parameters supported by the public products search and filter endpoint."""
    category: Optional[str] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    ground_type: Optional[GroundType] = None
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    in_stock: Optional[bool] = None
    featured: Optional[bool] = None
    q: Optional[str] = None
    sort: Optional[str] = "featured"  # "featured", "price_asc", "price_desc", "newest", "name_asc"
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=12, ge=1, le=100)


class PaginatedProductsResponse(BaseModel):
    """Structured paginated response for product listings."""
    items: List[Product]
    total: int
    page: int
    page_size: int
    total_pages: int
