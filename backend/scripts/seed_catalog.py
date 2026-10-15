"""Database-free seed script populating data/catalog.json with realistic football boots and jerseys."""

import asyncio
from datetime import datetime, timezone
import os
import sys
from uuid import uuid4

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.integrations.catalog_store import LocalJsonCatalogStore
from app.schemas.catalog import (
    Brand,
    CatalogDocument,
    Category,
    GroundType,
    Product,
    ProductImage,
    ProductVariant,
    SiteSettings,
)


def create_sample_catalog() -> CatalogDocument:
    """Generate comprehensive realistic catalogue dataset."""
    now = datetime.now(timezone.utc).isoformat()

    categories = [
        Category(
            slug="boots",
            name="Football Boots",
            description="Match-grade football boots across Firm Ground, Artificial Grass, and Turf configurations.",
            is_active=True,
            display_order=1,
        ),
        Category(
            slug="jerseys",
            name="Official Jerseys",
            description="Authentic matchday and player-issue club and national team football shirts.",
            is_active=True,
            display_order=2,
        ),
        Category(
            slug="accessories",
            name="Accessories & Gear",
            description="Elite grip socks, shinguards, and goalkeeper gloves.",
            is_active=True,
            display_order=3,
        ),
    ]

    brands = [
        Brand(
            slug="nike",
            name="Nike",
            logo_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200&auto=format&fit=crop&q=80",
            is_active=True,
        ),
        Brand(
            slug="adidas",
            name="Adidas",
            logo_url="https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=200&auto=format&fit=crop&q=80",
            is_active=True,
        ),
        Brand(
            slug="puma",
            name="Puma",
            logo_url="https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=200&auto=format&fit=crop&q=80",
            is_active=True,
        ),
        Brand(
            slug="mizuno",
            name="Mizuno",
            logo_url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?w=200&auto=format&fit=crop&q=80",
            is_active=True,
        ),
    ]

    settings = SiteSettings(
        store_name="APEX PITCH | Football Boots & Jerseys",
        whatsapp_number="447123456789",
        instagram_url="https://instagram.com/apexpitch_official",
        facebook_url="https://facebook.com/apexpitch",
        tiktok_url="https://tiktok.com/@apexpitch",
        email="orders@apexpitch.com",
        address="Stamford Bridge Quarter, Fulham Rd, London, UK",
        hero_title="Precision Boots. Legendary Jerseys.",
        hero_subtitle="Handpicked professional-grade boots & match-edition jerseys. Instant WhatsApp consultation and direct ordering.",
        hero_image_url="https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1600&auto=format&fit=crop&q=80",
        announcement_text="⚡ Free express dispatch on all orders over $150. Chat on WhatsApp for custom size advice.",
    )

    products = [
        # --- FOOTBALL BOOTS ---
        Product(
            id=str(uuid4()),
            name="Nike Mercurial Superfly 10 Elite FG",
            slug="nike-mercurial-superfly-10-elite-fg",
            description="Engineered for explosive speed with 3/4 length Zoom Air cushioning unit and Griknit upper for surgical ball control in all weather conditions.",
            category_slug="boots",
            brand_slug="nike",
            price=285.0,
            discount_price=249.99,
            currency="USD",
            ground_type=GroundType.FG,
            is_active=True,
            is_featured=True,
            display_order=1,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1511556532299-8f662fc26c06?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                ),
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=1000&auto=format&fit=crop&q=80",
                    is_primary=False,
                    position=2,
                ),
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="UK 7.5", color="Glacier Blue / Metallic Gold", stock_quantity=4, sku="NKE-MS10-75"),
                ProductVariant(id=str(uuid4()), size="UK 8.0", color="Glacier Blue / Metallic Gold", stock_quantity=6, sku="NKE-MS10-80"),
                ProductVariant(id=str(uuid4()), size="UK 8.5", color="Glacier Blue / Metallic Gold", stock_quantity=5, sku="NKE-MS10-85"),
                ProductVariant(id=str(uuid4()), size="UK 9.0", color="Glacier Blue / Metallic Gold", stock_quantity=3, sku="NKE-MS10-90"),
                ProductVariant(id=str(uuid4()), size="UK 9.5", color="Glacier Blue / Metallic Gold", stock_quantity=0, sku="NKE-MS10-95"),
                ProductVariant(id=str(uuid4()), size="UK 10.0", color="Glacier Blue / Metallic Gold", stock_quantity=2, sku="NKE-MS10-100"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="Adidas Predator Elite FT AG",
            slug="adidas-predator-elite-ft-ag",
            description="The return of the iconic fold-over tongue with modern Strikeskin rubber fins crafted specifically for 3G/4G artificial grass dominance.",
            category_slug="boots",
            brand_slug="adidas",
            price=279.99,
            discount_price=None,
            currency="USD",
            ground_type=GroundType.AG,
            is_active=True,
            is_featured=True,
            display_order=2,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="UK 8.0", color="Core Black / Solar Red", stock_quantity=5, sku="ADI-PRED-80"),
                ProductVariant(id=str(uuid4()), size="UK 8.5", color="Core Black / Solar Red", stock_quantity=4, sku="ADI-PRED-85"),
                ProductVariant(id=str(uuid4()), size="UK 9.0", color="Core Black / Solar Red", stock_quantity=7, sku="ADI-PRED-90"),
                ProductVariant(id=str(uuid4()), size="UK 9.5", color="Core Black / Solar Red", stock_quantity=2, sku="ADI-PRED-95"),
                ProductVariant(id=str(uuid4()), size="UK 10.5", color="Core Black / Solar Red", stock_quantity=1, sku="ADI-PRED-105"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="Puma Future 7 Ultimate FG/AG",
            slug="puma-future-7-ultimate-fg-ag",
            description="FUZIONFIT360 dual mesh upper with PWRTAPE support locks your foot down for adaptive fit with or without laces.",
            category_slug="boots",
            brand_slug="puma",
            price=229.0,
            discount_price=189.99,
            currency="USD",
            ground_type=GroundType.FG,
            is_active=True,
            is_featured=False,
            display_order=3,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="UK 7.5", color="Poison Pink / White", stock_quantity=3, sku="PUM-FUT-75"),
                ProductVariant(id=str(uuid4()), size="UK 8.5", color="Poison Pink / White", stock_quantity=4, sku="PUM-FUT-85"),
                ProductVariant(id=str(uuid4()), size="UK 9.5", color="Poison Pink / White", stock_quantity=0, sku="PUM-FUT-95"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="Mizuno Morelia Neo IV Beta Made In Japan FG",
            slug="mizuno-morelia-neo-iv-beta-japan-fg",
            description="Handcrafted in Japan with the finest Scotchguard K-Leather. Ultra-lightweight bare-foot touch re-engineered for the modern playmaker.",
            category_slug="boots",
            brand_slug="mizuno",
            price=320.0,
            discount_price=None,
            currency="USD",
            ground_type=GroundType.FG,
            is_active=True,
            is_featured=True,
            display_order=4,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="UK 8.0", color="Pearl White / Black / Gold", stock_quantity=2, sku="MIZ-MOR-80"),
                ProductVariant(id=str(uuid4()), size="UK 8.5", color="Pearl White / Black / Gold", stock_quantity=3, sku="MIZ-MOR-85"),
                ProductVariant(id=str(uuid4()), size="UK 9.0", color="Pearl White / Black / Gold", stock_quantity=1, sku="MIZ-MOR-90"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="Nike Phantom GX II Elite SG-Pro Anti-Clog",
            slug="nike-phantom-gx-ii-elite-sg-pro",
            description="Anti-Clog Traction technology on the soleplate sheds mud to ensure maximum grip on waterlogged, muddy pitches.",
            category_slug="boots",
            brand_slug="nike",
            price=295.0,
            discount_price=259.0,
            currency="USD",
            ground_type=GroundType.SG,
            is_active=True,
            is_featured=False,
            display_order=5,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="UK 8.5", color="Metallic Gold / Black", stock_quantity=4, sku="NKE-PGX-85"),
                ProductVariant(id=str(uuid4()), size="UK 9.0", color="Metallic Gold / Black", stock_quantity=2, sku="NKE-PGX-90"),
                ProductVariant(id=str(uuid4()), size="UK 10.0", color="Metallic Gold / Black", stock_quantity=3, sku="NKE-PGX-100"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="Adidas Copa Pure 2 Pro TF Turf",
            slug="adidas-copa-pure-2-pro-tf",
            description="Supple Fusionskin cow leather forefoot with Lightstrike midsole cushioning for premium response on artificial turf pitches.",
            category_slug="boots",
            brand_slug="adidas",
            price=140.0,
            discount_price=119.99,
            currency="USD",
            ground_type=GroundType.TF,
            is_active=True,
            is_featured=False,
            display_order=6,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="UK 7.5", color="Cloud White / Core Black", stock_quantity=6, sku="ADI-COP-75"),
                ProductVariant(id=str(uuid4()), size="UK 8.5", color="Cloud White / Core Black", stock_quantity=8, sku="ADI-COP-85"),
                ProductVariant(id=str(uuid4()), size="UK 9.5", color="Cloud White / Core Black", stock_quantity=4, sku="ADI-COP-95"),
            ],
            created_at=now,
            updated_at=now,
        ),

        # --- OFFICIAL JERSEYS ---
        Product(
            id=str(uuid4()),
            name="Real Madrid 2024/25 Authentic Home Jersey",
            slug="real-madrid-2024-25-authentic-home-jersey",
            description="The official player-version home jersey with woven houndstooth pattern and metallic gold accents. Features HEAT.RDY air-cooling fabric.",
            category_slug="jerseys",
            brand_slug="adidas",
            price=150.0,
            discount_price=135.0,
            currency="USD",
            ground_type=None,
            is_active=True,
            is_featured=True,
            display_order=7,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="S", color="White / Gold", stock_quantity=5, sku="RM-HM24-S"),
                ProductVariant(id=str(uuid4()), size="M", color="White / Gold", stock_quantity=8, sku="RM-HM24-M"),
                ProductVariant(id=str(uuid4()), size="L", color="White / Gold", stock_quantity=7, sku="RM-HM24-L"),
                ProductVariant(id=str(uuid4()), size="XL", color="White / Gold", stock_quantity=4, sku="RM-HM24-XL"),
                ProductVariant(id=str(uuid4()), size="XXL", color="White / Gold", stock_quantity=2, sku="RM-HM24-XXL"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="Arsenal 2024/25 Authentic Away Player Jersey",
            slug="arsenal-2024-25-authentic-away-jersey",
            description="Celebrating North London's diaspora connection with Pan-African color flourishes and heat-applied lightweight Cannon crest.",
            category_slug="jerseys",
            brand_slug="adidas",
            price=145.0,
            discount_price=None,
            currency="USD",
            ground_type=None,
            is_active=True,
            is_featured=True,
            display_order=8,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1516478177764-9fe5bd7e9717?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="M", color="Black / Red / Green", stock_quantity=6, sku="ARS-AW24-M"),
                ProductVariant(id=str(uuid4()), size="L", color="Black / Red / Green", stock_quantity=5, sku="ARS-AW24-L"),
                ProductVariant(id=str(uuid4()), size="XL", color="Black / Red / Green", stock_quantity=3, sku="ARS-AW24-XL"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="France National Team 2024 Match Home Kit",
            slug="france-2024-match-home-kit",
            description="Vintage oversized cockerel crest on bright royal blue Dri-FIT ADV fabric as worn in European Championship matches.",
            category_slug="jerseys",
            brand_slug="nike",
            price=140.0,
            discount_price=120.0,
            currency="USD",
            ground_type=None,
            is_active=True,
            is_featured=False,
            display_order=9,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="S", color="Bright Blue", stock_quantity=3, sku="FRA-HM24-S"),
                ProductVariant(id=str(uuid4()), size="M", color="Bright Blue", stock_quantity=6, sku="FRA-HM24-M"),
                ProductVariant(id=str(uuid4()), size="L", color="Bright Blue", stock_quantity=4, sku="FRA-HM24-L"),
                ProductVariant(id=str(uuid4()), size="XL", color="Bright Blue", stock_quantity=1, sku="FRA-HM24-XL"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="Manchester City 2024/25 Definitely City 4th Kit",
            slug="manchester-city-2024-25-definitely-city-4th-kit",
            description="Co-designed by Noel Gallagher celebrating 30 years of 'Definitely Maybe'. Premium muted tones and signature inner collar detailing.",
            category_slug="jerseys",
            brand_slug="puma",
            price=135.0,
            discount_price=None,
            currency="USD",
            ground_type=None,
            is_active=True,
            is_featured=True,
            display_order=10,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="M", color="Retro Cream / Poppy Pink", stock_quantity=7, sku="MCI-DM24-M"),
                ProductVariant(id=str(uuid4()), size="L", color="Retro Cream / Poppy Pink", stock_quantity=5, sku="MCI-DM24-L"),
                ProductVariant(id=str(uuid4()), size="XL", color="Retro Cream / Poppy Pink", stock_quantity=2, sku="MCI-DM24-XL"),
            ],
            created_at=now,
            updated_at=now,
        ),

        # --- ACCESSORIES ---
        Product(
            id=str(uuid4()),
            name="Apex Grip Pro Performance Socks (3-Pack)",
            slug="apex-grip-pro-performance-socks-3-pack",
            description="Anti-slip rubber suction pads eliminate in-boot slippage, blister formation, and micro-movements during rapid direction changes.",
            category_slug="accessories",
            brand_slug="nike",
            price=45.0,
            discount_price=38.0,
            currency="USD",
            ground_type=None,
            is_active=True,
            is_featured=False,
            display_order=11,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1582588678413-dbf45f4823e9?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="One Size (UK 7-11)", color="White / Black / Gold", stock_quantity=25, sku="APX-GRP-3PK"),
            ],
            created_at=now,
            updated_at=now,
        ),
        Product(
            id=str(uuid4()),
            name="Predator Pro Negative Cut Goalkeeper Gloves",
            slug="predator-pro-negative-cut-goalkeeper-gloves",
            description="URG 2.0 latex palm combines match-level stickiness and high abrasion resistance with High Definition Grip silicone backhand elements.",
            category_slug="accessories",
            brand_slug="adidas",
            price=120.0,
            discount_price=99.0,
            currency="USD",
            ground_type=None,
            is_active=True,
            is_featured=False,
            display_order=12,
            images=[
                ProductImage(
                    id=str(uuid4()),
                    url="https://images.unsplash.com/photo-1543326727-cf6c39e8f84c?w=1000&auto=format&fit=crop&q=80",
                    is_primary=True,
                    position=1,
                )
            ],
            variants=[
                ProductVariant(id=str(uuid4()), size="Size 8.5", color="Lucid Lemon / Black", stock_quantity=3, sku="ADI-GLV-85"),
                ProductVariant(id=str(uuid4()), size="Size 9.0", color="Lucid Lemon / Black", stock_quantity=4, sku="ADI-GLV-90"),
                ProductVariant(id=str(uuid4()), size="Size 10.0", color="Lucid Lemon / Black", stock_quantity=2, sku="ADI-GLV-100"),
            ],
            created_at=now,
            updated_at=now,
        ),
    ]

    return CatalogDocument(
        schema_version="1.0.0",
        products=products,
        categories=categories,
        brands=brands,
        site_settings=settings,
    )


async def seed() -> None:
    """Run seeding routine writing to data/catalog.json."""
    catalog = create_sample_catalog()
    store = LocalJsonCatalogStore(file_path="./data/catalog.json")
    await store.save(catalog)
    print(f"Successfully seeded {len(catalog.products)} products into ./data/catalog.json")


if __name__ == "__main__":
    asyncio.run(seed())
