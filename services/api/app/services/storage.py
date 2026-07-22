from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from app.core.config import settings


@dataclass(frozen=True)
class UploadSession:
    upload_id: UUID
    object_key: str
    upload_url: str
    headers: dict[str, str]
    expires_at: datetime


class ObjectStorageService:
    """Storage adapter boundary for S3, Cloudflare R2, MinIO, or future local dev storage."""

    def create_upload_session(self, workspace_id: UUID, filename: str, mime_type: str) -> UploadSession:
        upload_id = uuid4()
        object_key = f"workspaces/{workspace_id}/uploads/{upload_id}/{filename}"
        expires_at = datetime.now(UTC) + timedelta(minutes=10)

        # In production, replace this deterministic local URL with boto3.generate_presigned_url.
        upload_url = f"{settings.s3_endpoint_url or settings.api_url}/ownly-upload/{object_key}"
        return UploadSession(
            upload_id=upload_id,
            object_key=object_key,
            upload_url=upload_url,
            headers={"Content-Type": mime_type, "x-ownly-upload-id": str(upload_id)},
            expires_at=expires_at,
        )


storage_service = ObjectStorageService()

