from __future__ import annotations

from abc import ABC, abstractmethod

from vision.adapter.inbound.api.schemas.optic_yolo_detector_schema import YoloDetectorSchema
from vision.app.dtos.optic_yolo_detector_dto import YoloDetectorResponse


class YoloDetectorUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: YoloDetectorSchema) -> YoloDetectorResponse:
        pass
