from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository

log = logging.getLogger(__name__)


class HartleyViolinPgRepository(HartleyViolinRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: HartleyViolinQuery) -> HartleyViolinResponse:
        '''하틀리 바이올리니스트의 자기 소개 레포지토리 구현 메소드'''
        log.info("[HartleyViolinPgRepository] introduce_myself id=%s", query.id)
        return HartleyViolinResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )


CrewHartleyViolinPgRepository = HartleyViolinPgRepository
