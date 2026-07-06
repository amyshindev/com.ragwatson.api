from __future__ import annotations

from vision.adapter.inbound.api.schemas.optic_yolo_detector_schema import YoloDetectorSchema
from vision.app.dtos.optic_yolo_detector_dto import YoloDetectorResponse
from vision.app.ports.input.optic_yolo_detector_use_case import YoloDetectorUseCase


class YoloDetectorInteractor(YoloDetectorUseCase):
    async def introduce_myself(self, schema: YoloDetectorSchema) -> YoloDetectorResponse:
        return YoloDetectorResponse(id=schema.id, name=schema.name)
