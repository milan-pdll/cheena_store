# ARCHITECTURAL DECISIONS LOG (ADR)

## 2026-10-15: Monorepo Structure with `backend/` and `frontend/`
- **Context:** Need clean separation of concerns between Python FastAPI backend and Next.js frontend while retaining unified docker-compose, CI/CD, and docs tracking.
- **Decision:** Split into root `/backend` and `/frontend` directories, keeping documentation, docker orchestration, and git hooks in the repository root.
- **Consequences:** Easy independent deployment (e.g. Render for backend, Vercel for frontend) and isolated dependency management.

## 2026-10-15: Pivot to Database-Free Architecture (JSON CatalogStore)
- **Context:** The store has under 1000 products, no online payment transactions, and direct customer contact via WhatsApp. Traditional relational database hosting (e.g. managed PostgreSQL) adds cost, provisioning complexity, and cold-start latency on free-tier compute.
- **Decision:** Remove PostgreSQL, SQLite, SQLAlchemy, and Alembic. Implement an atomic, validated JSON catalogue document (`catalog.json`) managed behind a `CatalogStore` interface (`LocalJsonCatalogStore` for local development, `CloudinaryRawCatalogStore` for ephemeral cloud deployments). All data access is mediated through typed Pydantic v2 schemas and Repository/Service abstractions with an in-memory cache and atomic write locks.
- **Consequences:** Zero database hosting costs, instantaneous boot times, simplified backups (single JSON download/upload), and zero migration headaches. If scaling beyond ~1000 items in the future, a database implementation can be swapped into the Repository layer without breaking API or frontend contracts.

## 2026-10-15: Direct WhatsApp Order Link Generation Strategy
- **Context:** Store does not collect online payments; checkout happens via conversational commerce.
- **Decision:** Pre-generate standardized URL-encoded WhatsApp messages containing Product Name, SKU/Variant Size, Price, and Product Page canonical URL. Keep phone number dynamically managed via `SiteSettings`.
- **Consequences:** Zero payment gateway PCI compliance burdens, high mobile conversion in target markets.

## 2026-10-15: Media Storage Abstraction with Cloudinary Provider
- **Context:** Free tier storage with fast on-the-fly transformations and CDN delivery, but avoiding vendor lock-in.
- **Decision:** Define abstract `ImageStorageProvider` protocol with methods `upload`, `delete`, and `get_optimized_url`. Implement `CloudinaryStorageProvider` first.
- **Consequences:** Easily swap in S3, Cloudflare R2, or Supabase Storage in the future with zero service-layer code changes.
