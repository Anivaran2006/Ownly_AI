from fastapi import APIRouter

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.search import ChatRequest, ChatResponse, SearchRequest, SearchResponse
from app.services.access import require_workspace_member
from app.services.search import chat_with_inventory, search_inventory

router = APIRouter()
chat_router = APIRouter()


@router.post("", response_model=SearchResponse)
def search(payload: SearchRequest, current_user: CurrentUser, db: DbSession) -> SearchResponse:
    require_workspace_member(db, current_user, payload.workspace_id)
    return search_inventory(db, payload.workspace_id, payload.query, payload.limit)


@chat_router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, current_user: CurrentUser, db: DbSession) -> ChatResponse:
    require_workspace_member(db, current_user, payload.workspace_id)
    return chat_with_inventory(db, payload.workspace_id, payload.message)

