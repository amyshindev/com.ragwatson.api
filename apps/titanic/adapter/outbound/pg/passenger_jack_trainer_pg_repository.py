import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_jack_trainer_dto import PassengerJackTrainerQuery, PassengerJackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_repository import PassengerJackTrainerRepository

log = logging.getLogger(__name__)


class PassengerJackTrainerPgRepository(PassengerJackTrainerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: PassengerJackTrainerQuery) -> PassengerJackTrainerResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "PassengerJackTrainer", query.id)
        return PassengerJackTrainerResponse(id=query.id, name=query.name)
