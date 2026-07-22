from fastapi import APIRouter

from app.api.v1.routes import analytics, auth, health, products, reminders, scans, search, uploads, workspaces

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(scans.router, prefix="/scans", tags=["scans"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(search.chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

