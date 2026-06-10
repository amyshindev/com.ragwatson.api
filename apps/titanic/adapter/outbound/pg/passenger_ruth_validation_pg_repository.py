from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse
from titanic.app.ports.output.passenger_ruth_validation_repository import RuthValidationRepository

log = logging.getLogger(__name__)


class RuthValidationPgRepository(RuthValidationRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RuthValidationQuery) -> RuthValidationResponse:
        '''루스 검증의 자기 소개 레포지토리 구현 메소드'''
        log.info("[RuthValidationPgRepository] introduce_myself id=%s", query.id)
        return RuthValidationResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )


PassengerRuthValidationPgRepository = RuthValidationPgRepository
