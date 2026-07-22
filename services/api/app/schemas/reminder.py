from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.entities import ReminderKind, ReminderStatus


class ReminderCreate(BaseModel):
    workspace_id: UUID
    product_id: UUID | None = None
    kind: ReminderKind
    title: str = Field(min_length=1, max_length=320)
    due_at: datetime
    send_at: datetime
    channel: str = Field(default="email", max_length=40)


class ReminderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    product_id: UUID | None = None
    kind: ReminderKind
    status: ReminderStatus
    title: str
    due_at: datetime
    send_at: datetime
    channel: str

