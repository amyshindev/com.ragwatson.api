from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from siliconvalley.app.dtos.dinesh_dash_dto import DineshDashQuery, DineshDashResponse
from siliconvalley.app.ports.output.dinesh_dash_port import DineshDashPort

log = logging.getLogger(__name__)


class DineshDashPgRepository(DineshDashPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: DineshDashQuery) -> DineshDashResponse:
        log.info("[DineshDashPgRepository] introduce_myself id=%s", query.id)
        return DineshDashResponse(
            id=query.id * 10000,
            name=query.name + " (repository)",
        )
