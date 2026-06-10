from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository

log = logging.getLogger(__name__)


class WalterRoasterPgRepository(WalterRoasterRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        '''월터 로스터의 자기 소개 레포지토리 구현 메소드'''
        log.info("[WalterRoasterPgRepository] introduce_myself id=%s", query.id)
        return WalterRoasterResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )


CrewWalterRoasterPgRepository = WalterRoasterPgRepository
