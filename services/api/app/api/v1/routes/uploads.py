from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUser, DbSession
from app.models.entities import Document, DocumentStatus
from app.schemas.upload import DocumentOut, UploadSessionCreate, UploadSessionOut
from app.services.access import require_workspace_write
from app.services.storage import storage_service

router = APIRouter()


@router.post("/sessions", response_model=UploadSessionOut, status_code=status.HTTP_201_CREATED)
def create_upload_session(payload: UploadSessionCreate, current_user: CurrentUser, db: DbSession) -> UploadSessionOut:
    require_workspace_write(db, current_user, payload.workspace_id)
    session = storage_service.create_upload_session(payload.workspace_id, payload.filename, payload.mime_type)
    document = Document(
        workspace_id=payload.workspace_id,
        uploaded_by=current_user.id,
        kind=payload.document_kind,
        status=DocumentStatus.uploaded,
        original_filename=payload.filename,
        mime_type=payload.mime_type,
        byte_size=payload.byte_size,
        checksum_sha256=payload.checksum_sha256,
        object_key=session.object_key,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return UploadSessionOut(
        upload_id=session.upload_id,
        document_id=document.id,
        upload_url=session.upload_url,
        headers=session.headers,
        expires_at=session.expires_at,
    )


@router.post("/{document_id}/complete", response_model=DocumentOut)
def complete_upload(document_id: UUID, current_user: CurrentUser, db: DbSession) -> Document:
    document = db.get(Document, document_id)
    if document is None or document.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    require_workspace_write(db, current_user, document.workspace_id)
    document.status = DocumentStatus.processing
    db.commit()
    db.refresh(document)
    return document

