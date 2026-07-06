from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from vision.app.dtos.optic_clip_embedder_dto import ClipEmbedderQuery, ClipEmbedderResponse
from vision.app.ports.output.optic_clip_embedder_port import ClipEmbedderPort

log = logging.getLogger(__name__)


class ClipEmbedderPgRepository(ClipEmbedderPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: ClipEmbedderQuery) -> ClipEmbedderResponse:
        log.info("[ClipEmbedderPgRepository] introduce_myself id=%s", query.id)
        return ClipEmbedderResponse(
            id=query.id,
            name=f"{query.name} — 멀티모달 임베딩·유사도",
        )
