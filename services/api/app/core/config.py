from functools import lru_cache

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    app_url: AnyHttpUrl | str = "http://localhost:3000"
    api_url: AnyHttpUrl | str = "http://localhost:8000"

    database_url: str = "postgresql+psycopg://ownly:ownly@localhost:5432/ownly"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = Field(default="replace-with-a-long-random-secret")
    jwt_issuer: str = "ownly-local"
    access_token_minutes: int = 15
    refresh_token_days: int = 30

    s3_endpoint_url: str | None = "http://localhost:9000"
    s3_region: str = "us-east-1"
    s3_bucket: str = "ownly-documents"
    s3_access_key_id: str = "ownly"
    s3_secret_access_key: str = "change-me-local-minio-secret"

    ai_provider: str = "openai"
    ai_model: str = ""
    openai_api_key: str = ""
    gemini_api_key: str = ""

    ocr_provider: str = "tesseract"
    google_document_ai_processor: str = ""
    azure_document_intelligence_endpoint: str = ""
    azure_document_intelligence_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
