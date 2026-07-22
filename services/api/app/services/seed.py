from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.entities import Product, User, Workspace, WorkspaceMember, WorkspaceRole


def seed_demo_data(db: Session) -> None:
    existing = db.scalar(select(User).where(User.email == "demo@ownly.app"))
    if existing is not None:
        return

    user = User(
        email="demo@ownly.app",
        full_name="Aarav Mehta",
        password_hash=hash_password("ownly-demo-password"),
        locale="en-IN",
        default_currency="INR",
    )
    db.add(user)
    db.flush()

    workspace = Workspace(name="Mehta Family", home_country="IN", default_currency="INR", plan="family", created_by=user.id)
    db.add(workspace)
    db.flush()

    db.add(
        WorkspaceMember(
            workspace_id=workspace.id,
            user_id=user.id,
            role=WorkspaceRole.owner,
            display_name="Aarav",
            joined_at=datetime.now(UTC),
        )
    )

    db.add_all(
        [
            Product(
                workspace_id=workspace.id,
                created_by=user.id,
                name="MacBook Pro 14",
                brand="Apple",
                model="M3 Pro",
                category="Electronics",
                purchase_price=182900,
                purchase_currency="INR",
                seller_name="Apple Store",
                estimated_resale_value=74000,
                ai_summary="Protected item with invoice, warranty, manual, and accessory set.",
            ),
            Product(
                workspace_id=workspace.id,
                created_by=user.id,
                name="Samsung Frame TV 55",
                brand="Samsung",
                model="LS03D",
                category="Electronics",
                purchase_price=94990,
                purchase_currency="INR",
                seller_name="Croma",
                estimated_resale_value=51000,
                ai_summary="Invoice, installation note, and official manual are linked.",
            ),
        ]
    )
    db.commit()

