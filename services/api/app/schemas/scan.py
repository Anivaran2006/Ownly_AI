from uuid import UUID

from pydantic import BaseModel, Field

from app.models.entities import ExtractionStatus


class ExtractionFieldOut(BaseModel):
    field_name: str
    value: str | float | int | bool | None
    confidence: float = Field(ge=0, le=1)
    evidence: str | None = None


class ProductCandidateOut(BaseModel):
    name: str
    confidence: float = Field(ge=0, le=1)
    fields: list[ExtractionFieldOut]


class ScanCreate(BaseModel):
    workspace_id: UUID
    document_id: UUID


class ScanOut(BaseModel):
    id: UUID
    workspace_id: UUID
    document_id: UUID
    status: ExtractionStatus
    average_confidence: float | None = None
    product_candidates: list[ProductCandidateOut] = []


class ScanConfirmRequest(BaseModel):
    product_candidates: list[ProductCandidateOut] | None = None

