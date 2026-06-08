import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_rose_model_dto import PassengerRoseModelQuery, PassengerRoseModelResponse
from titanic.app.ports.output.passenger_rose_model_repository import PassengerRoseModelRepository

log = logging.getLogger(__name__)


class PassengerRoseModelPgRepository(PassengerRoseModelRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: PassengerRoseModelQuery) -> PassengerRoseModelResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "PassengerRoseModel", query.id)
        return PassengerRoseModelResponse(id=query.id, name=query.name)
