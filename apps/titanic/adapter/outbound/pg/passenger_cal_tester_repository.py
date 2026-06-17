from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.output.passenger_cal_tester_port import CalTesterPort

log = logging.getLogger(__name__)


class CalTesterPgRepository(CalTesterPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        '''칼 테스터의 자기 소개 레포지토리 구현 메소드'''
        log.info("[CalTesterPgRepository] introduce_myself id=%s", query.id)
        return CalTesterResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )


PassengerCalTesterPgRepository = CalTesterPgRepository
