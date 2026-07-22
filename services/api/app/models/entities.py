from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.models.base import Base, IdMixin, TimestampMixin


class WorkspaceRole(StrEnum):
    owner = "owner"
    admin = "admin"
    member = "member"
    viewer = "viewer"
    limited = "limited"


class ProductStatus(StrEnum):
    active = "active"
    returned = "returned"
    sold = "sold"
    lost = "lost"
    disposed = "disposed"
    archived = "archived"


class DocumentKind(StrEnum):
    invoice = "invoice"
    warranty = "warranty"
    manual = "manual"
    receipt = "receipt"
    photo = "photo"
    service_record = "service_record"
    insurance = "insurance"
    other = "other"


class DocumentStatus(StrEnum):
    uploaded = "uploaded"
    processing = "processing"
    processed = "processed"
    failed = "failed"
    archived = "archived"


class ExtractionStatus(StrEnum):
    queued = "queued"
    running = "running"
    needs_review = "needs_review"
    completed = "completed"
    failed = "failed"


class ReminderKind(StrEnum):
    warranty_expiry = "warranty_expiry"
    return_deadline = "return_deadline"
    replacement_deadline = "replacement_deadline"
    amc_renewal = "amc_renewal"
    insurance_renewal = "insurance_renewal"
    service_due = "service_due"
    custom = "custom"


class ReminderStatus(StrEnum):
    scheduled = "scheduled"
    sent = "sent"
    dismissed = "dismissed"
    failed = "failed"
    cancelled = "cancelled"


class User(IdMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(240))
    avatar_url: Mapped[str | None] = mapped_column(String(1024))
    locale: Mapped[str] = mapped_column(String(16), default="en-IN")
    default_currency: Mapped[str] = mapped_column(String(3), default="INR")
    password_hash: Mapped[str | None] = mapped_column(String(512))
    google_sub: Mapped[str | None] = mapped_column(String(255), unique=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    memberships: Mapped[list[WorkspaceMember]] = relationship(back_populates="user")


class Workspace(IdMixin, TimestampMixin, Base):
    __tablename__ = "workspaces"

    name: Mapped[str] = mapped_column(String(240))
    slug: Mapped[str | None] = mapped_column(String(160), unique=True)
    home_country: Mapped[str] = mapped_column(String(2), default="IN")
    default_currency: Mapped[str] = mapped_column(String(3), default="INR")
    plan: Mapped[str] = mapped_column(String(40), default="free")
    private_ai_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    members: Mapped[list[WorkspaceMember]] = relationship(back_populates="workspace", cascade="all, delete-orphan")
    products: Mapped[list[Product]] = relationship(back_populates="workspace")


class WorkspaceMember(IdMixin, Base):
    __tablename__ = "workspace_members"
    __table_args__ = (UniqueConstraint("workspace_id", "user_id", name="uq_workspace_member"),)

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[WorkspaceRole] = mapped_column(Enum(WorkspaceRole, name="workspace_role"), default=WorkspaceRole.member)
    display_name: Mapped[str | None] = mapped_column(String(160))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    workspace: Mapped[Workspace] = relationship(back_populates="members")
    user: Mapped[User] = relationship(back_populates="memberships")


class Product(IdMixin, TimestampMixin, Base):
    __tablename__ = "products"
    __table_args__ = (
        Index("idx_products_workspace_status", "workspace_id", "status"),
        Index("idx_products_workspace_category", "workspace_id", "category"),
    )

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    created_by: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(320))
    brand: Mapped[str | None] = mapped_column(String(160))
    model: Mapped[str | None] = mapped_column(String(160))
    category: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus, name="product_status"), default=ProductStatus.active)
    condition_grade: Mapped[str] = mapped_column(String(40), default="good")
    purchase_date: Mapped[date | None] = mapped_column(Date)
    purchase_price: Mapped[float | None] = mapped_column(Numeric(14, 2))
    purchase_currency: Mapped[str] = mapped_column(String(3), default="INR")
    tax_amount: Mapped[float | None] = mapped_column(Numeric(14, 2))
    tax_label: Mapped[str | None] = mapped_column(String(40), default="GST")
    seller_name: Mapped[str | None] = mapped_column(String(240))
    seller_domain: Mapped[str | None] = mapped_column(String(240))
    payment_method: Mapped[str | None] = mapped_column(String(120))
    order_id: Mapped[str | None] = mapped_column(String(160))
    invoice_number: Mapped[str | None] = mapped_column(String(160))
    estimated_resale_value: Mapped[float | None] = mapped_column(Numeric(14, 2))
    resale_currency: Mapped[str | None] = mapped_column(String(3))
    image_object_key: Mapped[str | None] = mapped_column(String(1024))
    ai_summary: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    workspace: Mapped[Workspace] = relationship(back_populates="products")


class Document(IdMixin, TimestampMixin, Base):
    __tablename__ = "documents"
    __table_args__ = (Index("idx_documents_workspace_kind", "workspace_id", "kind"),)

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    uploaded_by: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"))
    kind: Mapped[DocumentKind] = mapped_column(Enum(DocumentKind, name="document_kind"), default=DocumentKind.other)
    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus, name="document_status"), default=DocumentStatus.uploaded
    )
    original_filename: Mapped[str] = mapped_column(String(512))
    mime_type: Mapped[str] = mapped_column(String(160))
    byte_size: Mapped[int]
    checksum_sha256: Mapped[str | None] = mapped_column(String(64))
    object_key: Mapped[str] = mapped_column(String(1024))
    source_channel: Mapped[str] = mapped_column(String(80), default="upload")
    ocr_text: Mapped[str | None] = mapped_column(Text)
    ocr_layout: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    error_message: Mapped[str | None] = mapped_column(Text)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ProductDocument(IdMixin, Base):
    __tablename__ = "product_documents"
    __table_args__ = (UniqueConstraint("product_id", "document_id", "relationship", name="uq_product_document"),)

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    product_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"))
    document_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    relationship: Mapped[DocumentKind] = mapped_column(Enum(DocumentKind, name="document_kind"))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)


class ExtractionRun(IdMixin, Base):
    __tablename__ = "extraction_runs"

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    document_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    status: Mapped[ExtractionStatus] = mapped_column(
        Enum(ExtractionStatus, name="extraction_status"), default=ExtractionStatus.queued
    )
    ocr_provider: Mapped[str | None] = mapped_column(String(80))
    model_provider: Mapped[str | None] = mapped_column(String(80))
    model_name: Mapped[str | None] = mapped_column(String(160))
    prompt_version: Mapped[str | None] = mapped_column(String(80))
    schema_version: Mapped[str] = mapped_column(String(80), default="ownership-extraction-v1")
    raw_output: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    normalized_output: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    average_confidence: Mapped[float | None] = mapped_column(Numeric(4, 3))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Warranty(IdMixin, TimestampMixin, Base):
    __tablename__ = "warranties"
    __table_args__ = (Index("idx_warranties_expiry", "workspace_id", "end_date"),)

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    product_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(String(80), default="manufacturer")
    provider_name: Mapped[str | None] = mapped_column(String(240))
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    duration_months: Mapped[int | None]
    source_document_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("documents.id"))
    confidence: Mapped[float | None] = mapped_column(Numeric(4, 3))
    is_extended: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)


class ReturnWindow(IdMixin, TimestampMixin, Base):
    __tablename__ = "return_windows"

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    product_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"))
    seller_name: Mapped[str | None] = mapped_column(String(240))
    return_deadline: Mapped[date | None] = mapped_column(Date)
    replacement_deadline: Mapped[date | None] = mapped_column(Date)
    policy_source: Mapped[str | None] = mapped_column(String(240))
    confidence: Mapped[float | None] = mapped_column(Numeric(4, 3))
    status: Mapped[str] = mapped_column(String(40), default="open")


class Reminder(IdMixin, TimestampMixin, Base):
    __tablename__ = "reminders"
    __table_args__ = (Index("idx_reminders_send", "status", "send_at"),)

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    product_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"))
    user_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"))
    kind: Mapped[ReminderKind] = mapped_column(Enum(ReminderKind, name="reminder_kind"))
    status: Mapped[ReminderStatus] = mapped_column(
        Enum(ReminderStatus, name="reminder_status"), default=ReminderStatus.scheduled
    )
    title: Mapped[str] = mapped_column(String(320))
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    send_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    channel: Mapped[str] = mapped_column(String(40), default="email")
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SearchEmbedding(IdMixin, TimestampMixin, Base):
    __tablename__ = "search_embeddings"
    __table_args__ = (Index("idx_search_embeddings_entity", "workspace_id", "entity_type", "entity_id"),)

    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    entity_type: Mapped[str] = mapped_column(String(80))
    entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True))
    chunk_kind: Mapped[str] = mapped_column(String(80))
    chunk_text: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    embedding: Mapped[Any] = mapped_column(Vector(1536))


class AuditLog(IdMixin, Base):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("idx_audit_logs_workspace_time", "workspace_id", "created_at"),)

    workspace_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("workspaces.id"))
    actor_user_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(160))
    entity_type: Mapped[str | None] = mapped_column(String(80))
    entity_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True))
    ip_hash: Mapped[str | None] = mapped_column(String(128))
    user_agent_hash: Mapped[str | None] = mapped_column(String(128))
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
