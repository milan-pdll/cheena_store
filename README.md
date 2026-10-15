# Cheena Store (APEX PITCH)

A production-ready e-commerce catalogue website for football boots and jerseys with direct WhatsApp purchasing and zero payment processing overhead. Built with a fast, database-free architecture utilizing validated atomic JSON storage and in-memory caching.

## Tech Stack
- **Backend:** Python 3.12, FastAPI, Pydantic v2, Uvicorn (Database-Free)
- **Data Persistence:** `CatalogStore` abstraction (`LocalJsonCatalogStore` with atomic writes & backup rotation, `CloudinaryRawCatalogStore` for ephemeral cloud deployments)
- **Authentication:** Admin-only JWT access + refresh tokens, bcrypt password verification
- **Media:** Cloudinary image storage with client-side direct upload signatures
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS, Framer Motion, dnd-kit

## Documentation
Full context and operational guides are documented in `/docs`:
- [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md): Single source of truth, tech stack, API endpoints, data model
- [docs/TASKS.md](docs/TASKS.md): Phased roadmap and active task checklist
- [docs/DECISIONS.md](docs/DECISIONS.md): Architectural decision records (ADR)
- [docs/CHANGELOG.md](docs/CHANGELOG.md): Change history
- [docs/HANDOFF.md](docs/HANDOFF.md): Session handoff and next steps

## Quick Start
### Backend
```bash
cd backend
python -m venv .venv
# On Windows: .venv\Scripts\activate | On Unix: source .venv/bin/activate
pip install -r requirements.txt
python scripts/seed_catalog.py
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:3000` for the storefront and `http://localhost:8000/api/v1/docs` for the interactive OpenAPI documentation.
