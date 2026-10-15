"""Pydantic v2 schemas for admin authentication, catalogue mutation requests, and inventory payloads."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from app.schemas.catalog import GroundType, ProductImage, ProductVariant


class AdminLoginRequest(BaseModel):
    """Admin login credentials request."""
    email: EmailStr
    password: str = Field(min_length=6)


class TokenResponse(BaseModel):
    """JWT access and refresh token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Token refresh payload."""
    refresh_token: str


class ProductCreateRequest(BaseModel):
    """Payload for creating a new product."""
    name: str = Field(min_length=2)
    slug: str = Field(min_length=2)
    description: str
    category_slug: str
    brand_slug: str
    price: float = Field(gt=0)
    discount_price: Optional[float] = Field(default=None, gt=0)
    currency: str = "USD"
    ground_type: Optional[GroundType] = None
    is_active: bool = True
    is_featured: bool = False
    display_order: int = 0
    images: List[ProductImage] = Field(default_factory=list)
    variants: List[ProductVariant] = Field(default_factory=list)


class ProductUpdateRequest(BaseModel):
    """Payload for updating product details."""
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    category_slug: Optional[str] = None
    brand_slug: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    discount_price: Optional[float] = None
    currency: Optional[str] = None
    ground_type: Optional[GroundType] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    display_order: Optional[int] = None
    images: Optional[List[ProductImage]] = None
    variants: Optional[List[ProductVariant]] = None


class ProductDuplicateRequest(BaseModel):
    """Payload for duplicating an existing product."""
    new_name: str
    new_slug: str


class BulkActionType(str, Enum):
    """Supported bulk operations on products."""
    DELETE = "delete"
    ACTIVATE = "activate"
    DEACTIVATE = "deactivate"
    UPDATE_PRICE = "update_price"


class BulkProductActionRequest(BaseModel):
    """Batch action payload on multiple products."""
    action: BulkActionType
    product_ids: List[str]
    price_modifier: Optional[float] = Field(
        default=None, description="Percentage adjustment for update_price (e.g. 10 for +10% or -10 for -10%)"
    )


class VariantStockUpdateRequest(BaseModel):
    """Inline variant inventory update payload."""
    stock_quantity: int = Field(ge=0)


class BulkStockItemUpdate(BaseModel):
    """Single item stock update descriptor."""
    product_id: str
    variant_id: str
    stock_quantity: int = Field(ge=0)


class BulkStockUpdateRequest(BaseModel):
    """Batch variant inventory adjustment payload."""
    updates: List[BulkStockItemUpdate]


class FeaturedReorderRequest(BaseModel):
    """Payload specifying new ordering of products or featured items."""
    ordered_ids: List[str]


class ImageReorderRequest(BaseModel):
    """Payload for reordering images within a product gallery."""
    ordered_image_ids: List[str]
    primary_image_id: Optional[str] = None


class CategoryUpsertRequest(BaseModel):
    """Category creation or modification payload."""
    slug: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    display_order: int = 0


class BrandUpsertRequest(BaseModel):
    """Brand creation or modification payload."""
    slug: str
    name: str
    logo_url: Optional[str] = None
    is_active: bool = True
