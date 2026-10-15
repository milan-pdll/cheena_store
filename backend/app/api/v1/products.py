"""Public product catalogue and single product detail endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_product_service
from app.schemas.catalog import GroundType, Product
from app.schemas.product_query import PaginatedProductsResponse, ProductFilterParams
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Public Products"])


@router.get("", response_model=PaginatedProductsResponse, status_code=status.HTTP_200_OK)
async def list_products(
    category: Optional[str] = Query(None, description="Category slug: boots, jerseys, accessories"),
    brand: Optional[str] = Query(None, description="Brand slug: nike, adidas, puma, etc."),
    size: Optional[str] = Query(None, description="Specific variant size: UK 9, L, etc."),
    ground_type: Optional[GroundType] = Query(None, description="Boot stud configuration: FG, AG, SG, TF, IC"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum effective price in USD"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum effective price in USD"),
    in_stock: Optional[bool] = Query(None, description="Filter for products currently in stock"),
    featured: Optional[bool] = Query(None, description="Filter for featured storefront products"),
    q: Optional[str] = Query(None, description="Free text search query across title, description, brand"),
    sort: Optional[str] = Query("featured", description="Sort order: featured, price_asc, price_desc, newest, name_asc"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(12, ge=1, le=100, description="Items per page"),
    service: ProductService = Depends(get_product_service),
) -> PaginatedProductsResponse:
    """List active products with multi-dimensional filtering, search, sorting, and pagination."""
    params = ProductFilterParams(
        category=category,
        brand=brand,
        size=size,
        ground_type=ground_type,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        featured=featured,
        q=q,
        sort=sort,
        page=page,
        page_size=page_size,
    )
    return await service.list_products(params)


@router.get("/{slug}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product_by_slug(
    slug: str,
    service: ProductService = Depends(get_product_service),
) -> Product:
    """Retrieve full detail for a single active product by slug."""
    return await service.get_by_slug(slug)
