from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_holmes.app.dtos.inspector_lestrade_official_dto import LestradeOfficialQuery, LestradeOfficialResponse
from sherlock_holmes.app.ports.output.inspector_lestrade_official_port import LestradeOfficialPort

log = logging.getLogger(__name__)


class LestradeOfficialPgRepository(LestradeOfficialPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: LestradeOfficialQuery) -> LestradeOfficialResponse:
        log.info("[LestradeOfficialPgRepository] introduce_myself id=%s", query.id)
        return LestradeOfficialResponse(
            id=query.id,
            name=f"{query.name} — 스코트랜드야드 공식 수사",
        )


InspectorLestradeOfficialPgRepository = LestradeOfficialPgRepository
