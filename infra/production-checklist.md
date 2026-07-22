# Production Checklist

## Security

- Rotate `JWT_SECRET` through a managed secret store.
- Use HTTPS-only cookies for refresh tokens.
- Enable MFA and passkey support.
- Enforce workspace authorization on every query and job.
- Add audit logs for document access and destructive actions.
- Encrypt object storage with per-workspace envelope keys.
- Redact sensitive payment and address data before AI calls when possible.

## Reliability

- Move OCR and AI work to queue workers.
- Make scans idempotent by document checksum and prompt/schema version.
- Add retry policies for OCR, AI, storage, email, and reminders.
- Use dead-letter queues for failed extraction jobs.
- Add backup restore drills for Postgres and object storage.

## Observability

- Add OpenTelemetry traces across upload, scan, extract, confirm, index, and notify.
- Track extraction accuracy by seller/template/provider.
- Alert on queue latency, OCR failures, model JSON failures, search latency, and notification failures.

## Compliance

- Publish privacy policy and terms.
- Add user data export and account deletion flows.
- Prepare vendor DPAs for OCR, AI, email, and storage providers.
- Start SOC 2 gap assessment before private beta.

