from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_holmes.app.dtos.doctor_watson_chronicler_dto import WatsonChroniclerQuery, WatsonChroniclerResponse
from sherlock_holmes.app.ports.output.doctor_watson_chronicler_port import WatsonChroniclerPort

log = logging.getLogger(__name__)


class WatsonChroniclerPgRepository(WatsonChroniclerPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: WatsonChroniclerQuery) -> WatsonChroniclerResponse:
        log.info("[WatsonChroniclerPgRepository] introduce_myself id=%s", query.id)
        return WatsonChroniclerResponse(
            id=query.id,
            name=f"{query.name} — 동반자·사건 기록자",
        )


DoctorWatsonChroniclerPgRepository = WatsonChroniclerPgRepository
