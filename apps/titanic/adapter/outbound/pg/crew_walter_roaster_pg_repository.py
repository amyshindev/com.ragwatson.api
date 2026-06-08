import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_walter_roaster_dto import CrewWalterRoasterQuery, CrewWalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_repository import CrewWalterRoasterRepository

log = logging.getLogger(__name__)


class CrewWalterRoasterPgRepository(CrewWalterRoasterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: CrewWalterRoasterQuery) -> CrewWalterRoasterResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "CrewWalterRoaster", query.id)
        return CrewWalterRoasterResponse(
            id=query.id * 10000,
            name=query.name + "\uac00 \ub808\ud3ec\uc9c0\ud1a0\ub9ac\uc5d0 \ub2e4\ub155\uc634",
        )
