from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.vision_gateway_dto import VisionUploadCommand, VisionUploadResult


class VisionUploadPort(ABC):
    @abstractmethod
    async def save_upload(self, command: VisionUploadCommand) -> VisionUploadResult:
        pass
