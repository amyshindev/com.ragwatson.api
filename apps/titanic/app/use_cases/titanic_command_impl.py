import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.impl.passenger_command_repository import PassengerCommandRepository
from titanic.app.ports.input.titanic_command_port import TitanicCommandPort
from titanic.domain.entities.titanic import TitanicPassenger

log = logging.getLogger(__name__)


class TitanicCommandUseCase(TitanicCommandPort):
    def __init__(self, repository: PassengerCommandRepository | None = None) -> None:
        self._repository = repository or PassengerCommandRepository()

    async def create_passenger(
        self,
        session: AsyncSession,
        passenger: TitanicPassenger,
    ) -> tuple[int, TitanicPassenger]:
        db_id = await self._repository.save(session, passenger)
        log.info(
            "[TitanicCommandUseCase] create_passenger 완료 — id=%s passenger_id=%s",
            db_id,
            passenger.passenger_id,
        )
        return db_id, passenger
