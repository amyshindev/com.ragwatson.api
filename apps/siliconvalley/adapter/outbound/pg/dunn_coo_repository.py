from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from siliconvalley.app.dtos.dunn_coo_dto import DunnCooQuery, DunnCooResponse
from siliconvalley.app.ports.output.dunn_coo_port import DunnCooPort

log = logging.getLogger(__name__)


class DunnCooPgRepository(DunnCooPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: DunnCooQuery) -> DunnCooResponse:
        log.info("[DunnCooPgRepository] introduce_myself id=%s", query.id)
        return DunnCooResponse(id=query.id, name=query.name)
