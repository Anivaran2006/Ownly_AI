from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import Product, ProductStatus, Reminder, ReminderStatus, Warranty
from app.schemas.analytics import AnalyticsOverview, CategoryBreakdownItem


def build_overview(db: Session, workspace_id) -> AnalyticsOverview:
    total_assets = db.scalar(
        select(func.count()).select_from(Product).where(Product.workspace_id == workspace_id, Product.deleted_at.is_(None))
    ) or 0
    total_purchase_value = db.scalar(
        select(func.coalesce(func.sum(Product.purchase_price), 0)).where(
            Product.workspace_id == workspace_id,
            Product.status == ProductStatus.active,
            Product.deleted_at.is_(None),
        )
    ) or 0
    active_warranties = db.scalar(select(func.count()).select_from(Warranty).where(Warranty.workspace_id == workspace_id)) or 0
    upcoming_actions = db.scalar(
        select(func.count()).select_from(Reminder).where(
            Reminder.workspace_id == workspace_id,
            Reminder.status == ReminderStatus.scheduled,
        )
    ) or 0
    category_rows = db.execute(
        select(Product.category, func.coalesce(func.sum(Product.purchase_price), 0), func.count())
        .where(Product.workspace_id == workspace_id, Product.deleted_at.is_(None))
        .group_by(Product.category)
        .order_by(func.coalesce(func.sum(Product.purchase_price), 0).desc())
    ).all()
    return AnalyticsOverview(
        total_assets=int(total_assets),
        total_purchase_value=float(total_purchase_value),
        currency="INR",
        active_warranties=int(active_warranties),
        upcoming_actions=int(upcoming_actions),
        category_breakdown=[
            CategoryBreakdownItem(category=row[0] or "Uncategorized", value=float(row[1]), count=int(row[2]))
            for row in category_rows
        ],
    )

