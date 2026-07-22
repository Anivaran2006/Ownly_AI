from uuid import UUID

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    workspace_id: UUID
    query: str = Field(min_length=1)
    filters: dict[str, object] = Field(default_factory=dict)
    limit: int = Field(default=20, ge=1, le=50)


class SearchResultOut(BaseModel):
    type: str
    id: UUID
    title: str
    snippet: str
    score: float
    citations: list[dict[str, object]] = Field(default_factory=list)


class SearchResponse(BaseModel):
    query: str
    interpreted_intent: str | None = None
    results: list[SearchResultOut]


class ChatRequest(BaseModel):
    workspace_id: UUID
    conversation_id: UUID | None = None
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    conversation_id: UUID
    answer: str
    actions: list[dict[str, object]] = Field(default_factory=list)
    citations: list[dict[str, object]] = Field(default_factory=list)

