import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_smith_captain_dto import CrewSmithCaptainQuery, CrewSmithCaptainResponse
from titanic.app.ports.output.crew_smith_captain_repository import CrewSmithCaptainRepository

log = logging.getLogger(__name__)


class CrewSmithCaptainPgRepository(CrewSmithCaptainRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: CrewSmithCaptainQuery) -> CrewSmithCaptainResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "CrewSmithCaptain", query.id)
        return CrewSmithCaptainResponse(id=query.id, name=query.name)
