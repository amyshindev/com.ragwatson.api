from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from vision.app.dtos.optic_resnet_classifier_dto import ResnetClassifierQuery, ResnetClassifierResponse
from vision.app.ports.output.optic_resnet_classifier_port import ResnetClassifierPort

log = logging.getLogger(__name__)


class ResnetClassifierPgRepository(ResnetClassifierPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: ResnetClassifierQuery) -> ResnetClassifierResponse:
        log.info("[ResnetClassifierPgRepository] introduce_myself id=%s", query.id)
        return ResnetClassifierResponse(
            id=query.id,
            name=f"{query.name} — 이미지 분류",
        )
