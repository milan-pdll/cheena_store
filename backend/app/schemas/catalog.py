"""Pydantic v2 schemas for the single source of truth catalogue document and domain entities."""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class GroundType(str, Enum):
    """Football boot ground type specification."""
    FG = "FG"  # Firm Ground
    AG = "AG"  # Artificial Grass
    SG = "SG"  # Soft Ground
    TF = "TF"  # Turf
    IC = "IC"  # Indoor Court


class CategorySlug(str, Enum):
    """Standard store categories."""
    BOOTS = "boots"
    JERSEYS = "jerseys"
    ACCESSORIES = "accessories"


class ProductImage(BaseModel):
    """Product gallery image specification."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    url: str
    public_id: Optional[str] = None
    position: int = 0
    is_primary: bool = False


class ProductVariant(BaseModel):
    """Individual SKU variant specifying size, color, and real-time inventory."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    size: str
    color: str
    stock_quantity: int = Field(ge=0, default=0)
    sku: str


class Product(BaseModel):
    """Full product entity schema."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    slug: str
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
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    deleted_at: Optional[str] = None

    @property
    def in_stock(self) -> bool:
        """Calculate aggregate stock availability across all variants."""
        return any(v.stock_quantity > 0 for v in self.variants)

    @property
    def total_stock(self) -> int:
        """Calculate total units on hand."""
        return sum(v.stock_quantity for v in self.variants)


class Category(BaseModel):
    """Store department category schema."""
    slug: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    display_order: int = 0


class Brand(BaseModel):
    """Manufacturer brand schema."""
    slug: str
    name: str
    logo_url: Optional[str] = None
    is_active: bool = True


class SiteSettings(BaseModel):
    """Store metadata, WhatsApp contact, hero banner, and announcement info."""
    store_name: str = "Apex Pitch Football Store"
    whatsapp_number: str = "1234567890"
    instagram_url: Optional[str] = "https://instagram.com"
    facebook_url: Optional[str] = "https://facebook.com"
    tiktok_url: Optional[str] = "https://tiktok.com"
    email: Optional[str] = "contact@apexpitch.com"
    address: Optional[str] = "10 Downing Pitch, London, UK"
    hero_title: str = "Precision Boots. Legendary Jerseys."
    hero_subtitle: str = (
        "Curated collection of match-grade football boots and authentic player edition jerseys."
    )
    hero_image_url: Optional[str] = None
    announcement_text: Optional[str] = "Worldwide Express Shipping Available"


class CatalogDocument(BaseModel):
    """Single root catalogue document validated before local or cloud storage writes."""
    schema_version: str = "1.0.0"
    products: List[Product] = Field(default_factory=list)
    categories: List[Category] = Field(default_factory=list)
    brands: List[Brand] = Field(default_factory=list)
    site_settings: SiteSettings = Field(default_factory=SiteSettings)
