from datetime import date
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUser, DbSession
from app.models.entities import Document, DocumentKind, ExtractionRun, Product, ProductDocument
from app.schemas.scan import ScanConfirmRequest, ScanCreate, ScanOut
from app.services.access import require_workspace_write
from app.services.scanner import scan_to_schema, start_scan

router = APIRouter()


def _date_or_none(value: object) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _float_or_none(value: object) -> float | None:
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return None
    return None


@router.post("", response_model=ScanOut, status_code=status.HTTP_202_ACCEPTED)
def create_scan(payload: ScanCreate, current_user: CurrentUser, db: DbSession) -> ScanOut:
    require_workspace_write(db, current_user, payload.workspace_id)
    document = db.get(Document, payload.document_id)
    if document is None or document.workspace_id != payload.workspace_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    run = start_scan(db, payload.workspace_id, document)
    return scan_to_schema(run)


@router.get("/{scan_id}", response_model=ScanOut)
def get_scan(scan_id: UUID, current_user: CurrentUser, db: DbSession) -> ScanOut:
    run = db.get(ExtractionRun, scan_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    require_workspace_write(db, current_user, run.workspace_id)
    return scan_to_schema(run)


@router.post("/{scan_id}/confirm", response_model=list[UUID], status_code=status.HTTP_201_CREATED)
def confirm_scan(scan_id: UUID, payload: ScanConfirmRequest, current_user: CurrentUser, db: DbSession) -> list[UUID]:
    run = db.get(ExtractionRun, scan_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    require_workspace_write(db, current_user, run.workspace_id)

    scan = scan_to_schema(run)
    candidates = payload.product_candidates or scan.product_candidates
    created_ids: list[UUID] = []
    for candidate in candidates:
        fields = {field.field_name: field.value for field in candidate.fields}
        product = Product(
            workspace_id=run.workspace_id,
            created_by=current_user.id,
            name=str(fields.get("product_name") or candidate.name),
            brand=str(fields.get("brand") or "") or None,
            model=str(fields.get("model") or "") or None,
            purchase_date=_date_or_none(fields.get("purchase_date")),
            purchase_price=_float_or_none(fields.get("price")),
            tax_amount=_float_or_none(fields.get("gst")),
            seller_name=str(fields.get("seller") or "") or None,
            payment_method=str(fields.get("payment_method") or "") or None,
            purchase_currency="INR",
            ai_summary=f"Created from scan with {candidate.confidence:.0%} confidence.",
        )
        db.add(product)
        db.flush()
        db.add(
            ProductDocument(
                workspace_id=run.workspace_id,
                product_id=product.id,
                document_id=run.document_id,
                relationship=DocumentKind.invoice,
                is_primary=True,
            )
        )
        created_ids.append(product.id)
    db.commit()
    return created_ids
