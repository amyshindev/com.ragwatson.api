from __future__ import annotations

from abc import ABC, abstractmethod

from vision.adapter.inbound.api.schemas.optic_ocr_reader_schema import OcrReaderSchema
from vision.app.dtos.optic_ocr_reader_dto import OcrReaderResponse


class OcrReaderUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: OcrReaderSchema) -> OcrReaderResponse:
        """OCR 리더 자기소개"""
        pass
