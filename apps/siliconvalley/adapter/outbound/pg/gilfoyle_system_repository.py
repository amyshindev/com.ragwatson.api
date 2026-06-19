from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from siliconvalley.app.dtos.gilfoyle_system_dto import GilfoyleSystemQuery, GilfoyleSystemResponse
from siliconvalley.app.ports.output.gilfoyle_system_port import GilfoyleSystemPort

log = logging.getLogger(__name__)


class GilfoyleSystemPgRepository(GilfoyleSystemPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: GilfoyleSystemQuery) -> GilfoyleSystemResponse:
        log.info("[GilfoyleSystemPgRepository] introduce_myself id=%s", query.id)
        return GilfoyleSystemResponse(
            id=query.id * 10000,
            name=query.name + " (repository)",
        )
