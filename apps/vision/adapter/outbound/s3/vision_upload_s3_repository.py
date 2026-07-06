from __future__ import annotations

import asyncio
import logging
import re
import uuid
from datetime import UTC, datetime

from core.config import VisionS3Settings, get_vision_s3_settings
from vision.app.dtos.vision_gateway_dto import VisionUploadCommand, VisionUploadResult
from vision.app.ports.output.vision_upload_port import VisionUploadPort

log = logging.getLogger(__name__)

_SAFE_FILENAME_RE = re.compile(r"[^a-zA-Z0-9._-]+")


def _sanitize_filename(filename: str) -> str:
    base = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1].strip() or "upload.bin"
    cleaned = _SAFE_FILENAME_RE.sub("_", base)
    return cleaned[:180]


def _build_s3_client(settings: VisionS3Settings):
    import boto3

    kwargs: dict[str, str] = {"region_name": settings.region}
    if settings.access_key_id and settings.secret_access_key:
        kwargs["aws_access_key_id"] = settings.access_key_id
        kwargs["aws_secret_access_key"] = settings.secret_access_key
    return boto3.client("s3", **kwargs)


def _put_object_sync(
    settings: VisionS3Settings,
    *,
    key: str,
    body: bytes,
    content_type: str,
) -> str:
    client = _build_s3_client(settings)
    client.put_object(
        Bucket=settings.bucket,
        Key=key,
        Body=body,
        ContentType=content_type,
    )
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.bucket, "Key": key},
        ExpiresIn=3600,
    )


class VisionUploadS3Repository(VisionUploadPort):
    async def save_upload(self, command: VisionUploadCommand) -> VisionUploadResult:
        from botocore.exceptions import BotoCoreError, ClientError

        settings = get_vision_s3_settings()
        file_id = uuid.uuid4().hex
        safe_name = _sanitize_filename(command.filename)
        key = f"{settings.prefix}/{file_id}/{safe_name}"

        try:
            s3_url = await asyncio.to_thread(
                _put_object_sync,
                settings,
                key=key,
                body=command.data,
                content_type=command.content_type,
            )
        except (ClientError, BotoCoreError) as exc:
            log.exception("[VisionUploadS3Repository] S3 upload failed key=%s", key)
            raise RuntimeError(f"S3 업로드에 실패했습니다: {exc}") from exc

        log.info(
            "[VisionUploadS3Repository] saved bucket=%s key=%s bytes=%s",
            settings.bucket,
            key,
            command.size_bytes,
        )
        return VisionUploadResult(
            file_id=file_id,
            filename=command.filename,
            content_type=command.content_type,
            size_bytes=command.size_bytes,
            uploaded_at=datetime.now(UTC).isoformat(),
            storage="s3",
            s3_bucket=settings.bucket,
            s3_key=key,
            s3_url=s3_url,
        )
