from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DbSession
from app.models.entities import Product
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.access import require_workspace_member, require_workspace_write

router = APIRouter()
WorkspaceQuery = Annotated[UUID, Query()]


@router.get("", response_model=list[ProductOut])
def list_products(
    current_user: CurrentUser,
    db: DbSession,
    workspace_id: WorkspaceQuery,
    category: str | None = None,
    seller: str | None = None,
) -> list[Product]:
    require_workspace_member(db, current_user, workspace_id)
    statement = select(Product).where(Product.workspace_id == workspace_id, Product.deleted_at.is_(None))
    if category:
        statement = statement.where(Product.category == category)
    if seller:
        statement = statement.where(Product.seller_name.ilike(f"%{seller}%"))
    return list(db.scalars(statement.order_by(Product.created_at.desc())).all())


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, current_user: CurrentUser, db: DbSession) -> Product:
    require_workspace_write(db, current_user, payload.workspace_id)
    product = Product(**payload.model_dump(), created_by=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: UUID, current_user: CurrentUser, db: DbSession) -> Product:
    product = db.get(Product, product_id)
    if product is None or product.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    require_workspace_member(db, current_user, product.workspace_id)
    return product


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: UUID, payload: ProductUpdate, current_user: CurrentUser, db: DbSession) -> Product:
    product = db.get(Product, product_id)
    if product is None or product.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    require_workspace_write(db, current_user, product.workspace_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, current_user: CurrentUser, db: DbSession) -> None:
    product = db.get(Product, product_id)
    if product is None or product.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    require_workspace_write(db, current_user, product.workspace_id)
    product.deleted_at = datetime.now(UTC)
    db.commit()
