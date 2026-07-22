from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.entities import Product
from app.schemas.search import ChatResponse, SearchResponse, SearchResultOut
from app.services.ai import model_gateway


def search_inventory(db: Session, workspace_id, query: str, limit: int) -> SearchResponse:
    like_query = f"%{query}%"
    products = db.scalars(
        select(Product)
        .where(
            Product.workspace_id == workspace_id,
            Product.deleted_at.is_(None),
            or_(
                Product.name.ilike(like_query),
                Product.brand.ilike(like_query),
                Product.model.ilike(like_query),
                Product.seller_name.ilike(like_query),
                Product.category.ilike(like_query),
            ),
        )
        .limit(limit)
    ).all()

    results = [
        SearchResultOut(
            type="product",
            id=product.id,
            title=product.name,
            snippet=product.ai_summary or f"{product.brand or ''} {product.model or ''}".strip(),
            score=0.87,
            citations=[{"entity": "product", "id": str(product.id)}],
        )
        for product in products
    ]
    return SearchResponse(query=query, interpreted_intent="hybrid_product_search", results=results)


def chat_with_inventory(db: Session, workspace_id, message: str) -> ChatResponse:
    search_response = search_inventory(db, workspace_id, message, limit=5)
    snippets = [result.snippet for result in search_response.results]
    answer = model_gateway.answer_inventory_question(message, snippets)
    return ChatResponse(
        conversation_id=uuid4(),
        answer=answer,
        actions=[],
        citations=[citation for result in search_response.results for citation in result.citations],
    )

