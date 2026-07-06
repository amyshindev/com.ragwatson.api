from __future__ import annotations

from abc import ABC, abstractmethod

from vision.adapter.inbound.api.schemas.optic_sam_segmenter_schema import SamSegmenterSchema
from vision.app.dtos.optic_sam_segmenter_dto import SamSegmenterResponse


class SamSegmenterUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: SamSegmenterSchema) -> SamSegmenterResponse:
        """샘 (SAM) 자기소개"""
        pass
