from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Hook queue consumers, telemetry, and provider health checks here.
    yield


app = FastAPI(
    title="Ownly API",
    version="0.1.0",
    description="Personal Ownership Management Platform API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(settings.app_url), "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "ownly-api", "docs": "/docs", "health": "/v1/healthz"}

