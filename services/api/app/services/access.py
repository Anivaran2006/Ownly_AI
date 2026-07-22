from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import User, WorkspaceMember, WorkspaceRole

WRITE_ROLES = {WorkspaceRole.owner, WorkspaceRole.admin, WorkspaceRole.member}
ADMIN_ROLES = {WorkspaceRole.owner, WorkspaceRole.admin}


def require_workspace_member(db: Session, user: User, workspace_id: UUID) -> WorkspaceMember:
    membership = db.scalar(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user.id,
            WorkspaceMember.revoked_at.is_(None),
        )
    )
    if membership is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Workspace access denied")
    return membership


def require_workspace_write(db: Session, user: User, workspace_id: UUID) -> WorkspaceMember:
    membership = require_workspace_member(db, user, workspace_id)
    if membership.role not in WRITE_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Write access denied")
    return membership


def require_workspace_admin(db: Session, user: User, workspace_id: UUID) -> WorkspaceMember:
    membership = require_workspace_member(db, user, workspace_id)
    if membership.role not in ADMIN_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access denied")
    return membership

