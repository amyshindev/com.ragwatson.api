"""S3 업로드 헬퍼 — vision_gateway_router에서 사용."""

from __future__ import annotations

from core.config import is_vision_s3_configured
from vision.app.dtos.vision_gateway_dto import VisionUploadCommand, VisionUploadResult


def vision_s3_enabled() -> bool:
    return is_vision_s3_configured()


async def save_vision_image_to_s3(command: VisionUploadCommand) -> VisionUploadResult:
    """이미지 바이트를 AWS S3 버킷에 저장합니다."""
    from vision.adapter.outbound.s3.vision_upload_s3_repository import (
        VisionUploadS3Repository,
    )

    repository = VisionUploadS3Repository()
    return await repository.save_upload(command)
