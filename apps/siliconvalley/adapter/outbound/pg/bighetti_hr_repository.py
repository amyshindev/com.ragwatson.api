from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from siliconvalley.app.dtos.bighetti_hr_dto import BighettiHrQuery, BighettiHrResponse
from siliconvalley.app.ports.output.bighetti_hr_port import BighettiHrPort

log = logging.getLogger(__name__)


class BighettiHrPgRepository(BighettiHrPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: BighettiHrQuery) -> BighettiHrResponse:
        log.info("[BighettiHrPgRepository] introduce_myself id=%s", query.id)
        return BighettiHrResponse(id=query.id, name=query.name)
