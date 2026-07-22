from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.entities import ProductStatus


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=320)
    brand: str | None = Field(default=None, max_length=160)
    model: str | None = Field(default=None, max_length=160)
    category: str | None = Field(default=None, max_length=120)
    status: ProductStatus = ProductStatus.active
    purchase_date: date | None = None
    purchase_price: float | None = Field(default=None, ge=0)
    purchase_currency: str = Field(default="INR", min_length=3, max_length=3)
    seller_name: str | None = Field(default=None, max_length=240)
    tax_amount: float | None = Field(default=None, ge=0)
    payment_method: str | None = Field(default=None, max_length=120)
    order_id: str | None = Field(default=None, max_length=160)
    invoice_number: str | None = Field(default=None, max_length=160)
    estimated_resale_value: float | None = Field(default=None, ge=0)
    ai_summary: str | None = None


class ProductCreate(ProductBase):
    workspace_id: UUID


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=320)
    brand: str | None = Field(default=None, max_length=160)
    model: str | None = Field(default=None, max_length=160)
    category: str | None = Field(default=None, max_length=120)
    status: ProductStatus | None = None
    purchase_date: date | None = None
    purchase_price: float | None = Field(default=None, ge=0)
    seller_name: str | None = Field(default=None, max_length=240)
    estimated_resale_value: float | None = Field(default=None, ge=0)
    ai_summary: str | None = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID

