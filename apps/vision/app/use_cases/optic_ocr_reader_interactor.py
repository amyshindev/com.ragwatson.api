from __future__ import annotations

from vision.adapter.inbound.api.schemas.optic_ocr_reader_schema import OcrReaderSchema
from vision.app.dtos.optic_ocr_reader_dto import OcrReaderQuery, OcrReaderResponse
from vision.app.ports.input.optic_ocr_reader_use_case import OcrReaderUseCase
from vision.app.ports.output.optic_ocr_reader_port import OcrReaderPort


class OcrReaderInteractor(OcrReaderUseCase):
    def __init__(self, repository: OcrReaderPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: OcrReaderSchema) -> OcrReaderResponse:
        return await self._repository.introduce_myself(
            OcrReaderQuery(id=schema.id, name=schema.name)
        )
