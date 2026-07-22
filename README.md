# Ownly SaaS Starter

Ownly is a Personal Ownership Management Platform.

Tagline: Own everything. Find anything.

This starter turns the product architecture into an implementation-ready monorepo:

- `apps/web`: Next.js, React, TypeScript, Tailwind CSS, shadcn-style UI components.
- `services/api`: FastAPI, SQLAlchemy, Alembic, JWT auth, product/upload/search/scanner foundations.
- `packages/shared`: shared TypeScript domain types.
- `infra`: Docker Compose and deployment notes.
- `docs`: MVP scope and engineering decisions.

## MVP Scope

The MVP includes:

1. Auth with email/password, JWT sessions, Google OAuth-ready hooks, and MFA-ready schema.
2. Workspaces and role-based access.
3. Encrypted document upload sessions.
4. Product profile CRUD.
5. OCR and AI extraction pipeline interfaces.
6. Natural language search endpoint with hybrid-search-ready contract.
7. Warranty and return reminder data model.
8. Dashboard UI based on the Ownly prototype.

## Quick Start

Copy the environment file:

```bash
cp .env.example .env
```

Start local infrastructure:

```bash
docker compose up -d postgres redis minio
```

Install dependencies:

```bash
npm install
cd services/api
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"
```

Run the API:

```bash
cd services/api
uvicorn app.main:app --reload --port 8000
```

Run the web app:

```bash
npm run dev --workspace @ownly/web
```

Open:

- Web: http://localhost:3000
- API docs: http://localhost:8000/docs

## Production Path

Recommended deployment:

- Vercel for `apps/web`.
- Railway, Fly.io, AWS ECS, or Kubernetes for `services/api`.
- Managed PostgreSQL with pgvector.
- Redis or a managed queue for async jobs.
- Cloudflare R2 or AWS S3 for encrypted documents.
- OpenTelemetry collector for traces and metrics.

## Push To GitHub

From this folder:

```bash
git init
git add .
git commit -m "Initial Ownly SaaS starter"
git branch -M main
git remote add origin https://github.com/Anivaran2006/Ownly_AI.git
git push -u origin main
```

Do not commit `.env`, `node_modules`, `.next`, `.venv`, local caches, or logs. They are covered by `.gitignore`.

## Security Defaults

- Access JWTs are short-lived.
- Refresh tokens are rotation-ready.
- Document storage is designed for envelope encryption.
- Sensitive fields are hash/encryption-ready.
- Every document access and destructive action should create an audit log.
- AI provider calls should use redacted or consented document text.

## What To Build Next

1. Run Alembic migrations against local Postgres.
2. Wire object storage signed upload URLs to S3 or R2.
3. Connect OCR provider adapter.
4. Connect AI model gateway.
5. Add frontend API calls to replace seeded dashboard data.
6. Add billing, exports, deletion workflows, and audit log views before public beta.
