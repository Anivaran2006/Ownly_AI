from uuid import UUID

from app.core.db import SessionLocal
from app.models.entities import Document
from app.services.scanner import start_scan


def process_document_scan(workspace_id: UUID, document_id: UUID) -> UUID:
    """Queue worker entrypoint for OCR plus AI extraction.

    The synchronous route uses the same service today. Move route-triggered work to Redis/RQ,
    Celery, Dramatiq, or cloud queues when processing gets expensive.
    """

    with SessionLocal() as db:
        document = db.get(Document, document_id)
        if document is None:
            raise ValueError(f"Document not found: {document_id}")
        run = start_scan(db, workspace_id, document)
        return run.id

