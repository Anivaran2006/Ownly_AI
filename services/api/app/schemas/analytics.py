from pydantic import BaseModel


class CategoryBreakdownItem(BaseModel):
    category: str
    value: float
    count: int


class AnalyticsOverview(BaseModel):
    total_assets: int
    total_purchase_value: float
    currency: str
    active_warranties: int
    upcoming_actions: int
    category_breakdown: list[CategoryBreakdownItem]

