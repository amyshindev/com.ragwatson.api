from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.optic_yolo_detector_dto import YoloDetectorQuery, YoloDetectorResponse


class YoloDetectorPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: YoloDetectorQuery) -> YoloDetectorResponse:
        """요로 (YOLO) 저장소"""
        pass
