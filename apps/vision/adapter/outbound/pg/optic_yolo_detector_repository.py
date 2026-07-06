from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from vision.app.dtos.optic_yolo_detector_dto import YoloDetectorQuery, YoloDetectorResponse
from vision.app.ports.output.optic_yolo_detector_port import YoloDetectorPort

log = logging.getLogger(__name__)


class YoloDetectorPgRepository(YoloDetectorPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: YoloDetectorQuery) -> YoloDetectorResponse:
        log.info("[YoloDetectorPgRepository] introduce_myself id=%s", query.id)
        return YoloDetectorResponse(
            id=query.id,
            name=f"{query.name} — 실시간 객체 탐지",
        )
