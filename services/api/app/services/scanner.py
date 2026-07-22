from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.entities import Document, DocumentStatus, ExtractionRun, ExtractionStatus
from app.schemas.scan import ProductCandidateOut, ScanOut
from app.services.ai import model_gateway
from app.services.ocr import get_ocr_provider


def start_scan(db: Session, workspace_id: UUID, document: Document) -> ExtractionRun:
    run = ExtractionRun(
        workspace_id=workspace_id,
        document_id=document.id,
        status=ExtractionStatus.running,
        ocr_provider=settings.ocr_provider,
        model_provider=settings.ai_provider,
        model_name=settings.ai_model or "configured-at-runtime",
        prompt_version="ownership-extraction-v1",
        started_at=datetime.now(UTC),
    )
    db.add(run)
    db.flush()

    ocr_provider = get_ocr_provider(settings.ocr_provider)
    ocr_result = ocr_provider.extract(document.object_key, document.mime_type)
    extracted = model_gateway.extract_ownership_record(ocr_result.text)

    document.status = DocumentStatus.processed
    document.ocr_text = ocr_result.text
    document.ocr_layout = ocr_result.layout
    run.status = ExtractionStatus.needs_review
    run.raw_output = {"ocr_text": ocr_result.text, "fields": extracted.fields}
    run.normalized_output = {
        "product_candidates": [
            {"name": extracted.name, "confidence": extracted.confidence, "fields": extracted.fields}
        ]
    }
    run.average_confidence = extracted.confidence
    run.completed_at = datetime.now(UTC)
    db.commit()
    db.refresh(run)
    return run


def scan_to_schema(run: ExtractionRun) -> ScanOut:
    payload = run.normalized_output or {}
    candidates = [
        ProductCandidateOut.model_validate(candidate)
        for candidate in payload.get("product_candidates", [])
    ]
    return ScanOut(
        id=run.id,
        workspace_id=run.workspace_id,
        document_id=run.document_id,
        status=run.status,
        average_confidence=float(run.average_confidence or 0),
        product_candidates=candidates,
    )

