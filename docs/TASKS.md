# PROJECT TASKS TRACKER

**Next task:** Phase 3: Public Frontend (royal gold design system, home hero, catalogue with filters, product detail gallery, and dynamic WhatsApp order CTA).

---

## Phase 0: Repo Scaffold & Setup
- [x] Create documentation structure (`/docs`)
- [x] Backend directory structure (`api`, `core`, `models`, `schemas`, `repositories`, `services`, `integrations`)
- [x] Frontend directory structure (Next.js App router, components, lib, types)
- [x] Root configuration: `.env.example`, `.gitignore`, `.pre-commit-config.yaml`
- [x] Backend config: `pyproject.toml`, `requirements.txt`, `alembic.ini`, `Dockerfile`
- [x] Frontend config: `package.json`, `tsconfig.json`, `tailwind.config.ts`, `Dockerfile`, `.eslintrc.json`, `.prettierrc`
- [x] Docker Compose orchestration (`docker-compose.yml`)
- [x] Verify tooling and test runs

## Phase 1: Database-Free Store, Public API & Seed Script
- [x] Remove database & Alembic leftovers (SQLAlchemy, PostgreSQL config, Alembic migrations)
- [x] Define comprehensive Pydantic v2 schemas (`Product`, `ProductVariant`, `ProductImage`, `Category`, `Brand`, `SiteSettings`, `CatalogDocument`)
- [x] Implement `CatalogStore` interface with `LocalJsonCatalogStore` (atomic write + backups + lock) and `CloudinaryRawCatalogStore`
- [x] Implement Repositories (`ProductRepository`, `CategoryRepository`, `BrandRepository`, `SettingsRepository`) with in-memory cache
- [x] Implement Services (`ProductService`, `StockService`, `SettingsService`, `TaxonomyService`)
- [x] Build Public API endpoints (`/products`, `/products/{slug}`, `/categories`, `/brands`, `/settings/public`)
- [x] Seed script (`backend/scripts/seed_catalog.py`) with ~12 realistic boots and jerseys
- [x] Pytest test suite for repositories, services, and public endpoints (16 tests passing)

## Phase 2: Admin Auth, CRUD APIs & Media Storage Abstraction
- [x] Admin authentication (JWT access + refresh tokens, bcrypt hashing, rate limiting)
- [x] Abstract `ImageStorage` interface + Cloudinary implementation (upload signature + media deletion)
- [x] Product and Variant CRUD endpoints (with soft-delete, duplicate, bulk actions)
- [x] Batch & inline stock update endpoints
- [x] Featured product & image reordering endpoints
- [x] SiteSettings update endpoint & Taxonomy manager (Categories & Brands CRUD)
- [x] Catalog backup export and validated restore endpoints
- [x] Admin test suite with mocked auth & storage (24/24 tests passing)

## Phase 3: Public Frontend
- [ ] Design system tokens in Tailwind (deep charcoal base, off-white, royal gold accent)
- [ ] Base layout (header with navigation, footer, floating WhatsApp button)
- [ ] Homepage (hero banner, featured boots & jerseys, brand strip, why choose us)
- [ ] Catalogue page (filters: ground type, size, brand, price, stock; sorting; search)
- [ ] Product detail page (gallery with zoom, variant selector, stock indicator, dynamic WhatsApp direct order CTA)
- [ ] Static pages: About, Contact, Shipping/FAQ
- [ ] Responsive testing across 360px, 768px, 1280px, 1920px

## Phase 4: Admin Panel
- [ ] Admin login page with JWT handling and auto-refresh
- [ ] Dashboard with stock alerts, product summary cards, quick actions
- [ ] Product management view (table, filter, create/edit modal/page, soft-delete, duplicate)
- [ ] Drag-and-drop media upload zone with preview, compression, and ordering (`dnd-kit`)
- [ ] Inline stock management table with +/- counters
- [ ] Drag-and-drop featured product reordering
- [ ] SiteSettings editor (WhatsApp number, social links, hero banner)
- [ ] Mobile-responsive admin layouts and optimistic UI toasts

## Phase 5: SEO, Performance, Accessibility & Hardening
- [ ] Next.js Metadata API, OpenGraph tags, sitemap.xml, robots.txt
- [ ] JSON-LD schema for Products
- [ ] Image optimization with Cloudinary transforms and next/image
- [ ] Accessibility audit (WCAG AA, focus visible, ARIA labels, 44px touch targets)
- [ ] Backend security hardening (CORS, trusted host, rate limiting, request size limits)
- [ ] Lighthouse score optimization

## Phase 6: Deployment & Handover Guide
- [ ] `docs/DEPLOYMENT.md` for Vercel/Cloudflare Pages (frontend) & Render/Railway/Fly.io (backend)
- [ ] Neon / Supabase PostgreSQL setup guide
- [ ] Production environment checklist & backup strategies
- [ ] Final project verification
