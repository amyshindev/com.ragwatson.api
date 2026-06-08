from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import PassengerJackTrainerPgRepository
from titanic.app.ports.input.passenger_jack_trainer_use_case import PassengerJackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import PassengerJackTrainerRepository
from titanic.app.use_cases.passenger_jack_trainer_interactor import PassengerJackTrainerInteractor


def get_passenger_jack_trainer_use_case(
    db: AsyncSession = Depends(get_db),
) -> PassengerJackTrainerUseCase:
    repository: PassengerJackTrainerRepository = PassengerJackTrainerPgRepository(session=db)
    return PassengerJackTrainerInteractor(repository=repository)
