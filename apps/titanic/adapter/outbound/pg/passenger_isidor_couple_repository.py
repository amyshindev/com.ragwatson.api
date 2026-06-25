from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleQuery, IsidorCoupleResponse
from titanic.app.ports.output.passenger_isidor_couple_port import IsidorCouplePort

log = logging.getLogger(__name__)


class IsidorCouplePgRepository(IsidorCouplePort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: IsidorCoupleQuery) -> IsidorCoupleResponse:
        """이시도르 커플의 자기 소개 레포지토리 구현 메소드"""
        log.info("[IsidorCouplePgRepository] introduce_myself id=%s", query.id)
        return IsidorCoupleResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )


PassengerIsidorCouplePgRepository = IsidorCouplePgRepository
