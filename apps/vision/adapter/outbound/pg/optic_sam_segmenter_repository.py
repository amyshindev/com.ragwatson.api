from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from vision.app.dtos.optic_sam_segmenter_dto import SamSegmenterQuery, SamSegmenterResponse
from vision.app.ports.output.optic_sam_segmenter_port import SamSegmenterPort

log = logging.getLogger(__name__)


class SamSegmenterPgRepository(SamSegmenterPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: SamSegmenterQuery) -> SamSegmenterResponse:
        log.info("[SamSegmenterPgRepository] introduce_myself id=%s", query.id)
        return SamSegmenterResponse(
            id=query.id,
            name=f"{query.name} — 세그멘테이션",
        )
