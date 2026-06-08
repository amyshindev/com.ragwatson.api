import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_andrews_architect_dto import CrewAndrewsArchitectQuery, CrewAndrewsArchitectResponse
from titanic.app.ports.output.crew_andrews_architect_repository import CrewAndrewsArchitectRepository

log = logging.getLogger(__name__)


class CrewAndrewsArchitectPgRepository(CrewAndrewsArchitectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: CrewAndrewsArchitectQuery) -> CrewAndrewsArchitectResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "CrewAndrewsArchitect", query.id)
        return CrewAndrewsArchitectResponse(id=query.id, name=query.name)
