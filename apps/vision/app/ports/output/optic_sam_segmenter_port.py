from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.optic_sam_segmenter_dto import SamSegmenterQuery, SamSegmenterResponse


class SamSegmenterPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: SamSegmenterQuery) -> SamSegmenterResponse:
        """샘 (SAM) 저장소"""
        pass
