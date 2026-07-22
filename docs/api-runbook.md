# API Runbook

## Local Startup

1. Start Postgres, Redis, and MinIO:

```bash
docker compose up -d postgres redis minio
```

2. Install API dependencies:

```bash
cd services/api
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"
```

3. Run migrations:

```bash
alembic upgrade head
```

4. Start FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

## Core Flow

1. Register or login.
2. Create an upload session.
3. Upload a file to object storage using the returned signed URL.
4. Mark the upload complete.
5. Start a scan.
6. Review extracted product candidates.
7. Confirm the scan to create product profiles.
8. Query products, search, dashboard analytics, and reminders.

## Demo Account

The seed helper creates:

- Email: `demo@ownly.app`
- Password: `ownly-demo-password`
- Workspace: `Mehta Family`

Run it from a Python shell after migrations:

```python
from app.core.db import SessionLocal
from app.services.seed import seed_demo_data

with SessionLocal() as db:
    seed_demo_data(db)
```

## Production Notes

- Replace deterministic upload URLs in `ObjectStorageService` with real S3/R2 presigned URLs.
- Move scanner execution from request/response into the queue worker.
- Store model prompts and schema versions in source control.
- Add extraction evals before connecting paid OCR/model providers.
- Add audit log writes for document downloads, exports, member changes, deletion, and AI consent events.

