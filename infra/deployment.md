# Deployment Strategy

## Local

Use Docker Compose for Postgres, Redis, and MinIO. Run the web and API processes directly for fast iteration.

## Staging

- Managed Postgres with pgvector.
- Object storage bucket with lifecycle policies.
- API container deployed from `services/api`.
- Web deployed from `apps/web`.
- OCR and AI keys scoped to staging.
- Synthetic receipt corpus for regression tests.

## Production

- Vercel for web or containerized Next.js behind CDN.
- FastAPI on Railway, Fly.io, AWS ECS, or Kubernetes.
- Managed PostgreSQL with PITR backups.
- Redis or managed queue for async extraction jobs.
- S3 or Cloudflare R2 for encrypted documents.
- OpenTelemetry collector and alerting.
- WAF and bot protection at the edge.

## Release Safety

- Run migrations in expand-and-contract style.
- Keep OCR and AI jobs idempotent.
- Drain workers during deploys.
- Alert on queue latency, extraction failure rate, model JSON schema failures, notification failures, and auth anomalies.

