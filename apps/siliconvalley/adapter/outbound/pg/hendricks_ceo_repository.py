from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from siliconvalley.app.dtos.hendricks_ceo_dto import HendricksCeoQuery, HendricksCeoResponse
from siliconvalley.app.ports.output.hendricks_ceo_port import HendricksCeoPort

log = logging.getLogger(__name__)


class HendricksCeoPgRepository(HendricksCeoPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: HendricksCeoQuery) -> HendricksCeoResponse:
        log.info("[HendricksCeoPgRepository] introduce_myself id=%s", query.id)
        return HendricksCeoResponse(id=query.id, name=query.name)
