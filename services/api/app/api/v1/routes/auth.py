from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DbSession
from app.core.security import create_access_token, hash_password, verify_password
from app.models.entities import User, Workspace, WorkspaceMember, WorkspaceRole
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserOut

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: DbSession) -> AuthResponse:
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        locale="en-IN",
        default_currency="INR",
    )
    db.add(user)
    db.flush()

    workspace = Workspace(
        name=payload.workspace_name or f"{payload.full_name}'s Home",
        home_country="IN",
        default_currency="INR",
        plan="free",
        created_by=user.id,
    )
    db.add(workspace)
    db.flush()

    db.add(
        WorkspaceMember(
            workspace_id=workspace.id,
            user_id=user.id,
            role=WorkspaceRole.owner,
            display_name=payload.full_name,
            joined_at=datetime.now(UTC),
        )
    )
    db.commit()
    db.refresh(user)

    return AuthResponse(
        access_token=create_access_token(user.id, workspace.id),
        user=UserOut.model_validate(user),
        workspace_id=workspace.id,
    )


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: DbSession) -> AuthResponse:
    user = db.scalar(select(User).where(User.email == payload.email.lower(), User.deleted_at.is_(None)))
    if user is None or user.password_hash is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    membership = db.scalar(select(WorkspaceMember).where(WorkspaceMember.user_id == user.id))
    if membership is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No workspace access")

    return AuthResponse(
        access_token=create_access_token(user.id, membership.workspace_id),
        user=UserOut.model_validate(user),
        workspace_id=membership.workspace_id,
    )


@router.get("/session", response_model=UserOut)
def session(current_user: CurrentUser) -> UserOut:
    return UserOut.model_validate(current_user)
