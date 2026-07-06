from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_holmes.app.dtos.mrs_hudson_housekeeper_dto import HudsonHousekeeperQuery, HudsonHousekeeperResponse
from sherlock_holmes.app.ports.output.mrs_hudson_housekeeper_port import HudsonHousekeeperPort

log = logging.getLogger(__name__)


class HudsonHousekeeperPgRepository(HudsonHousekeeperPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: HudsonHousekeeperQuery) -> HudsonHousekeeperResponse:
        log.info("[HudsonHousekeeperPgRepository] introduce_myself id=%s", query.id)
        return HudsonHousekeeperResponse(
            id=query.id,
            name=f"{query.name} — 221B 하우스키퍼·현장 접수",
        )


MrsHudsonHousekeeperPgRepository = HudsonHousekeeperPgRepository
