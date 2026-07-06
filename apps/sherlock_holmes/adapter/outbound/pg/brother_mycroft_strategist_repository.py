from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_holmes.app.dtos.brother_mycroft_strategist_dto import MycroftStrategistQuery, MycroftStrategistResponse
from sherlock_holmes.app.ports.output.brother_mycroft_strategist_port import MycroftStrategistPort

log = logging.getLogger(__name__)


class MycroftStrategistPgRepository(MycroftStrategistPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: MycroftStrategistQuery) -> MycroftStrategistResponse:
        log.info("[MycroftStrategistPgRepository] introduce_myself id=%s", query.id)
        return MycroftStrategistResponse(
            id=query.id,
            name=f"{query.name} — 전략·정보 조율",
        )


BrotherMycroftStrategistPgRepository = MycroftStrategistPgRepository
