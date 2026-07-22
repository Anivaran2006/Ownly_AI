from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.analytics import AnalyticsOverview
from app.services.access import require_workspace_member
from app.services.analytics import build_overview

router = APIRouter()
WorkspaceQuery = Annotated[UUID, Query()]


@router.get("/overview", response_model=AnalyticsOverview)
def overview(current_user: CurrentUser, db: DbSession, workspace_id: WorkspaceQuery) -> AnalyticsOverview:
    require_workspace_member(db, current_user, workspace_id)
    return build_overview(db, workspace_id)
