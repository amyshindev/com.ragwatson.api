from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_holmes.app.dtos.professor_moriarty_rival_dto import MoriartyRivalQuery, MoriartyRivalResponse
from sherlock_holmes.app.ports.output.professor_moriarty_rival_port import MoriartyRivalPort

log = logging.getLogger(__name__)


class MoriartyRivalPgRepository(MoriartyRivalPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: MoriartyRivalQuery) -> MoriartyRivalResponse:
        log.info("[MoriartyRivalPgRepository] introduce_myself id=%s", query.id)
        return MoriartyRivalResponse(
            id=query.id,
            name=f"{query.name} — 적대 검증·리스크 시나리오",
        )


ProfessorMoriartyRivalPgRepository = MoriartyRivalPgRepository
