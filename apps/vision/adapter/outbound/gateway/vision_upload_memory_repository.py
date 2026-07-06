from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from threading import Lock

from vision.app.dtos.vision_gateway_dto import VisionUploadCommand, VisionUploadResult
from vision.app.ports.output.vision_upload_port import VisionUploadPort

log = logging.getLogger(__name__)

_MAX_STORED = 100


class VisionUploadMemoryRepository(VisionUploadPort):
    def __init__(self) -> None:
        self._lock = Lock()
        self._uploads: dict[str, VisionUploadResult] = {}

    async def save_upload(self, command: VisionUploadCommand) -> VisionUploadResult:
        file_id = uuid.uuid4().hex
        result = VisionUploadResult(
            file_id=file_id,
            filename=command.filename,
            content_type=command.content_type,
            size_bytes=command.size_bytes,
            uploaded_at=datetime.now(UTC).isoformat(),
        )
        with self._lock:
            self._uploads[file_id] = result
            if len(self._uploads) > _MAX_STORED:
                oldest = next(iter(self._uploads))
                del self._uploads[oldest]
        log.info(
            "[VisionUploadMemoryRepository] saved file_id=%s filename=%s",
            file_id,
            command.filename,
        )
        return result
