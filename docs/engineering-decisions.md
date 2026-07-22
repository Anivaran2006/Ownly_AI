# Engineering Decisions

## Product Model

Ownly treats products as first-class assets. Documents are source evidence, extraction runs are versioned, and product profiles stay editable as ownership changes over time.

## Search

Use hybrid search:

- SQL filters for dates, sellers, category, price, owner, and warranty state.
- Full-text search over normalized product fields and OCR text.
- pgvector embeddings over summaries, document chunks, notes, and timeline events.
- AI answer synthesis only after permission-filtered retrieval.

## AI And OCR

Providers sit behind adapters:

- OCR: Google Document AI, Azure Document Intelligence, Tesseract.
- AI: OpenAI-compatible models, Gemini-compatible models, local fallback for simple classification.

The application stores provider, model, prompt version, schema version, raw output, normalized output, and field-level confidence for every extraction.

## Security

- Keep workspace isolation at the database and application layers.
- Use envelope encryption for uploaded objects.
- Never log raw document text by default.
- Use short-lived signed URLs.
- Treat model calls as consented data processing events.
- Audit document downloads, exports, deletion, member changes, and key security events.

