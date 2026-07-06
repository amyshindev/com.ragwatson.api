from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from threading import Lock

from vision.adapter.inbound.api.schemas.gateway_schema import (
    VisionCharacterListSchema,
    VisionCharacterSchema,
    VisionUploadResponseSchema,
)
from vision.app.constants.vision_characters import VISION_CHARACTERS
from vision.app.dtos.vision_gateway_dto import VisionUploadCommand
from vision.app.ports.output.vision_upload_port import VisionUploadPort

log = logging.getLogger(__name__)

_MAX_BYTES = 10 * 1024 * 1024
_ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/bmp",
}


class VisionGatewayInteractor:
    def __init__(self, upload_repository: VisionUploadPort) -> None:
        self._upload_repository = upload_repository

    async def list_characters(self) -> VisionCharacterListSchema:
        items = [
            VisionCharacterSchema(
                id=row["id"],
                route=row["route"],
                name=row["name"],
                role=row["role"],
                myself_path=f"/vision/{row['route']}/myself",
            )
            for row in VISION_CHARACTERS
        ]
        return VisionCharacterListSchema(items=items)

    async def upload_image(
        self,
        *,
        filename: str,
        content_type: str,
        data: bytes,
    ) -> VisionUploadResponseSchema:
        normalized_type = (content_type or "").split(";")[0].strip().lower()
        if normalized_type not in _ALLOWED_IMAGE_TYPES and not normalized_type.startswith("image/"):
            raise ValueError("이미지 파일만 업로드할 수 있습니다.")
        if len(data) == 0:
            raise ValueError("빈 파일입니다.")
        if len(data) > _MAX_BYTES:
            raise ValueError("이미지 크기는 10MB 이하여야 합니다.")

        saved = await self._upload_repository.save_upload(
            VisionUploadCommand(
                filename=filename,
                content_type=normalized_type or "application/octet-stream",
                size_bytes=len(data),
                data=data,
            ),
        )
        return VisionUploadResponseSchema(
            file_id=saved.file_id,
            filename=saved.filename,
            content_type=saved.content_type,
            size_bytes=saved.size_bytes,
            storage=saved.storage,
            message="이미지 업로드가 완료되었습니다.",
        )
