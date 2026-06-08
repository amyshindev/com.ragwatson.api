import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_lowe_boat_dto import CrewLoweBoatQuery, CrewLoweBoatResponse
from titanic.app.ports.output.crew_lowe_boat_repository import CrewLoweBoatRepository

log = logging.getLogger(__name__)


class CrewLoweBoatPgRepository(CrewLoweBoatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: CrewLoweBoatQuery) -> CrewLoweBoatResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "CrewLoweBoat", query.id)
        return CrewLoweBoatResponse(id=query.id, name=query.name)
