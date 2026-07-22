from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DbSession
from app.models.entities import Workspace, WorkspaceMember, WorkspaceRole
from app.schemas.workspace import WorkspaceCreate, WorkspaceMemberOut, WorkspaceOut
from app.services.access import require_workspace_admin, require_workspace_member

router = APIRouter()


@router.get("", response_model=list[WorkspaceOut])
def list_workspaces(current_user: CurrentUser, db: DbSession) -> list[WorkspaceOut]:
    memberships = db.scalars(
        select(WorkspaceMember).where(WorkspaceMember.user_id == current_user.id, WorkspaceMember.revoked_at.is_(None))
    ).all()
    workspaces: list[WorkspaceOut] = []
    for membership in memberships:
        workspace = db.get(Workspace, membership.workspace_id)
        if workspace is not None and workspace.deleted_at is None:
            workspaces.append(
                WorkspaceOut(
                    id=workspace.id,
                    name=workspace.name,
                    home_country=workspace.home_country,
                    default_currency=workspace.default_currency,
                    plan=workspace.plan,
                    private_ai_mode=workspace.private_ai_mode,
                    role=membership.role,
                )
            )
    return workspaces


@router.post("", response_model=WorkspaceOut, status_code=status.HTTP_201_CREATED)
def create_workspace(payload: WorkspaceCreate, current_user: CurrentUser, db: DbSession) -> WorkspaceOut:
    workspace = Workspace(
        name=payload.name,
        home_country=payload.home_country,
        default_currency=payload.default_currency,
        plan="free",
        created_by=current_user.id,
    )
    db.add(workspace)
    db.flush()
    db.add(WorkspaceMember(workspace_id=workspace.id, user_id=current_user.id, role=WorkspaceRole.owner))
    db.commit()
    db.refresh(workspace)
    return WorkspaceOut(
        id=workspace.id,
        name=workspace.name,
        home_country=workspace.home_country,
        default_currency=workspace.default_currency,
        plan=workspace.plan,
        private_ai_mode=workspace.private_ai_mode,
        role=WorkspaceRole.owner,
    )


@router.get("/{workspace_id}", response_model=WorkspaceOut)
def get_workspace(workspace_id: UUID, current_user: CurrentUser, db: DbSession) -> WorkspaceOut:
    membership = require_workspace_member(db, current_user, workspace_id)
    workspace = db.get(Workspace, workspace_id)
    if workspace is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return WorkspaceOut(
        id=workspace.id,
        name=workspace.name,
        home_country=workspace.home_country,
        default_currency=workspace.default_currency,
        plan=workspace.plan,
        private_ai_mode=workspace.private_ai_mode,
        role=membership.role,
    )


@router.get("/{workspace_id}/members", response_model=list[WorkspaceMemberOut])
def list_members(workspace_id: UUID, current_user: CurrentUser, db: DbSession) -> list[WorkspaceMemberOut]:
    require_workspace_admin(db, current_user, workspace_id)
    memberships = db.scalars(select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id)).all()
    members: list[WorkspaceMemberOut] = []
    for membership in memberships:
        user = membership.user
        members.append(
            WorkspaceMemberOut(
                id=membership.id,
                user_id=membership.user_id,
                email=user.email,
                display_name=membership.display_name,
                role=membership.role,
            )
        )
    return members
