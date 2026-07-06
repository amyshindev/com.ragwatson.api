from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from vision.app.dtos.optic_ocr_reader_dto import OcrReaderQuery, OcrReaderResponse
from vision.app.ports.output.optic_ocr_reader_port import OcrReaderPort

log = logging.getLogger(__name__)


class OcrReaderPgRepository(OcrReaderPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: OcrReaderQuery) -> OcrReaderResponse:
        log.info("[OcrReaderPgRepository] introduce_myself id=%s", query.id)
        return OcrReaderResponse(
            id=query.id,
            name=f"{query.name} — 문자·텍스트 인식",
        )
