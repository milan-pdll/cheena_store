# PROJECT CONTEXT: Football Boots & Jersey E-Commerce (Database-Free)

## 1. Project Summary
A production-ready e-commerce catalogue for football boots and jerseys. Customers browse products, select size/variant, and place orders directly via WhatsApp / social channels (no online payment gateway). Database-free design: single validated JSON catalogue (`catalog.json`) loaded into memory behind a swappable `CatalogStore` interface. Admin access secured with JWT and env-backed credentials.

## 2. Tech Stack
- **Backend:** Python 3.12, FastAPI, Pydantic v2 (async), Uvicorn, NO database
- **Data Storage:** Atomic JSON catalogue via `CatalogStore` (`LocalJsonCatalogStore` / `CloudinaryRawCatalogStore`)
- **Admin Auth:** Single admin credentials in env (`ADMIN_EMAIL`, `ADMIN_PASSWORD_HASH`), JWT access + refresh, bcrypt
- **Media Storage:** Cloudinary free tier behind `ImageStorage` abstraction
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS, Framer Motion, dnd-kit
- **Containerization:** Docker & Docker Compose
- **Code Quality:** Ruff, Black, ESLint, Prettier, Pre-commit hooks, Pytest

## 3. Folder Map
- `/docs`: Project documentation, architectural decisions, task tracking, and handoffs
- `/backend`: FastAPI service following layered architecture
  - `backend/app/main.py`: FastAPI entrypoint, middleware, router mount, global exception handlers
  - `backend/app/api/v1/`: Versioned route controllers (`health.py`, `products.py`, `categories.py`, `brands.py`, `settings.py`)
  - `backend/app/core/`: Application settings, security/JWT, error models, dependencies
  - `backend/app/schemas/`: Pydantic v2 models for catalogue schema, query filters, and API DTOs
  - `backend/app/integrations/`: `CatalogStore` implementations (Local & Cloudinary Raw) and `ImageStorage`
  - `backend/app/repositories/`: In-memory data access repositories (products, categories, brands, settings)
  - `backend/app/services/`: Pure business logic (filtering, stock management, slug lookups)
  - `backend/scripts/seed_catalog.py`: Realistic seed data generator creating `data/catalog.json`
  - `backend/tests/`: Pytest suite using temporary/in-memory `CatalogStore` fixtures
- `/frontend`: Next.js App Router frontend with mobile-first responsive design
  - `frontend/src/app/`: Next.js routes (catalogue, product details, admin)
  - `frontend/src/components/`: Reusable UI elements, filters, gallery, and admin tables
  - `frontend/src/lib/`: API client, WhatsApp link generator, formatters, utilities
  - `frontend/src/types/`: TypeScript domain and API contract types

## 4. How to Run
### Local Dev (Hybrid)
1. **Backend**:
   - `cd backend && python -m venv .venv && .venv\Scripts\activate` (or `source .venv/bin/activate`)
   - `pip install -r requirements.txt`
   - `python scripts/seed_catalog.py` (generates initial `data/catalog.json`)
   - `uvicorn app.main:app --reload --port 8000`
2. **Frontend**:
   - `cd frontend && npm install && npm run dev` (running at `http://localhost:3000`)
### Local Dev (Docker Compose)
- `docker compose up --build`
### Production
- Backend: Run on Render / Railway / Fly.io with `CATALOG_STORE=cloudinary`
- Frontend: Deploy Next.js to Vercel / Cloudflare Pages

## 5. Environment Variables
### Backend (`backend/.env`)
- `ENVIRONMENT` (`development` | `production`)
- `CATALOG_STORE` (`local` | `cloudinary`)
- `CATALOG_FILE_PATH`, `CATALOG_BACKUP_DIR`, `CATALOG_MAX_BACKUPS`
- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- `ADMIN_EMAIL`, `ADMIN_PASSWORD_HASH`
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`, `CLOUDINARY_RAW_CATALOG_ID`
- `CORS_ORIGINS`
### Frontend (`frontend/.env.local`)
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_WHATSAPP_FALLBACK_NUMBER`

## 6. API Endpoint List (v1)
| Method | Path | Purpose | Auth |
|---|---|---|---|
| GET | `/api/v1/health` | Health check probe | Public |
| GET | `/api/v1/products` | Filtered, sorted, paginated catalogue | Public |
| GET | `/api/v1/products/{slug}` | Product detail with variants & images | Public |
| GET | `/api/v1/categories` | Active categories | Public |
| GET | `/api/v1/brands` | Active brands | Public |
| GET | `/api/v1/settings/public` | Public store contact & hero settings | Public |
| POST | `/api/v1/admin/login` | Admin login to get JWT pair | Rate-limited |
| POST | `/api/v1/admin/refresh` | Refresh JWT access token | Admin |
| POST | `/api/v1/admin/products` | Create product | Admin |
| PUT/PATCH | `/api/v1/admin/products/{id}` | Edit product details & status | Admin |
| DELETE | `/api/v1/admin/products/{id}` | Soft delete product | Admin |
| POST | `/api/v1/admin/products/bulk` | Bulk delete, activate, price update | Admin |
| PATCH | `/api/v1/admin/stock/{variant_id}`| Inline stock count update | Admin |
| PUT | `/api/v1/admin/products/reorder` | Reorder featured items | Admin |
| PUT | `/api/v1/admin/settings` | Update WhatsApp, socials, hero | Admin |
| GET | `/api/v1/admin/catalog/export` | Download raw catalogue backup | Admin |
| POST | `/api/v1/admin/catalog/import` | Validated restore from backup | Admin |

## 7. Data Storage Schema (`catalog.json`)
- `schema_version`: string (e.g. "1.0.0")
- `products[]`: `id` (uuid), `name`, `slug`, `description`, `category_slug`, `brand_slug`, `price`, `discount_price`, `currency`, `ground_type` (FG/AG/SG/TF/IC), `is_active`, `is_featured`, `display_order`, `images[]`, `variants[]`, `created_at`, `updated_at`, `deleted_at` (nullable)
- `variants[]`: `id` (uuid), `size`, `color`, `stock_quantity`, `sku`
- `images[]`: `id` (uuid), `url`, `public_id`, `position`, `is_primary`
- `categories[]`: `slug`, `name`, `description`, `is_active`, `display_order`
- `brands[]`: `slug`, `name`, `logo_url`, `is_active`
- `site_settings`: `store_name`, `whatsapp_number`, `instagram_url`, `facebook_url`, `tiktok_url`, `email`, `address`, `hero_title`, `hero_subtitle`, `hero_image_url`, `announcement_text`

## 8. Current Status
- **Phase 1 & 2 Completed:** Database-free `CatalogStore` (Local + Cloudinary raw), Pydantic v2 domain schemas, repositories, services, public storefront API, admin JWT auth with rate limiting, product/variant CRUD with cloning and bulk actions, stock update endpoints, Cloudinary media signature provider, taxonomy manager, backup export/restore, and 24 passing tests.
- **Phase 3 Ready:** Public Frontend (design system tokens, home page, catalogue with filters, product detail gallery, and dynamic WhatsApp order CTA).

## 9. Known Issues & Watchouts
- Ensure atomic writes on `LocalJsonCatalogStore` (write to `.tmp` file, then `os.replace`).
- Maintain thread-safe `asyncio.Lock` for writes.
- `CloudinaryRawCatalogStore` uses Cloudinary `uploader.upload_large` / `api.resource` for raw JSON syncing.
