from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DbSession
from app.models.entities import Reminder
from app.schemas.reminder import ReminderCreate, ReminderOut
from app.services.access import require_workspace_member, require_workspace_write

router = APIRouter()
WorkspaceQuery = Annotated[UUID, Query()]


@router.get("", response_model=list[ReminderOut])
def list_reminders(current_user: CurrentUser, db: DbSession, workspace_id: WorkspaceQuery) -> list[Reminder]:
    require_workspace_member(db, current_user, workspace_id)
    return list(
        db.scalars(select(Reminder).where(Reminder.workspace_id == workspace_id).order_by(Reminder.send_at.asc())).all()
    )


@router.post("", response_model=ReminderOut, status_code=status.HTTP_201_CREATED)
def create_reminder(payload: ReminderCreate, current_user: CurrentUser, db: DbSession) -> Reminder:
    require_workspace_write(db, current_user, payload.workspace_id)
    reminder = Reminder(**payload.model_dump(), user_id=current_user.id)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder
