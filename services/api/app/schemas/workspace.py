from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.entities import WorkspaceRole


class WorkspaceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    home_country: str
    default_currency: str
    plan: str
    private_ai_mode: bool
    role: WorkspaceRole | None = None


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=240)
    home_country: str = Field(default="IN", min_length=2, max_length=2)
    default_currency: str = Field(default="INR", min_length=3, max_length=3)


class WorkspaceMemberOut(BaseModel):
    id: UUID
    user_id: UUID
    email: str
    display_name: str | None = None
    role: WorkspaceRole

