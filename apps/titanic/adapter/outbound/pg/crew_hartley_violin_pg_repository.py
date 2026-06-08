import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_hartley_violin_dto import CrewHartleyViolinQuery, CrewHartleyViolinResponse
from titanic.app.ports.output.crew_hartley_violin_repository import CrewHartleyViolinRepository

log = logging.getLogger(__name__)


class CrewHartleyViolinPgRepository(CrewHartleyViolinRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: CrewHartleyViolinQuery) -> CrewHartleyViolinResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "CrewHartleyViolin", query.id)
        return CrewHartleyViolinResponse(id=query.id, name=query.name)
