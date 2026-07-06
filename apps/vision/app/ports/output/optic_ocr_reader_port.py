from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.optic_ocr_reader_dto import OcrReaderQuery, OcrReaderResponse


class OcrReaderPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: OcrReaderQuery) -> OcrReaderResponse:
        """OCR 리더 저장소"""
        pass
