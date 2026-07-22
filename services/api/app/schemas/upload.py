from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.entities import DocumentKind, DocumentStatus


class UploadSessionCreate(BaseModel):
    workspace_id: UUID
    filename: str = Field(min_length=1, max_length=512)
    mime_type: str = Field(min_length=1, max_length=160)
    byte_size: int = Field(gt=0)
    checksum_sha256: str | None = Field(default=None, max_length=64)
    document_kind: DocumentKind = DocumentKind.other


class UploadSessionOut(BaseModel):
    upload_id: UUID
    document_id: UUID
    upload_url: str
    headers: dict[str, str]
    expires_at: datetime


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    kind: DocumentKind
    status: DocumentStatus
    original_filename: str
    mime_type: str
    byte_size: int
    object_key: str
