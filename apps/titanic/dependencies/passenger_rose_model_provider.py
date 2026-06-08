from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.passenger_rose_model_pg_repository import PassengerRoseModelPgRepository
from titanic.app.ports.input.passenger_rose_model_use_case import PassengerRoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import PassengerRoseModelRepository
from titanic.app.use_cases.passenger_rose_model_interactor import PassengerRoseModelInteractor


def get_passenger_rose_model_use_case(
    db: AsyncSession = Depends(get_db),
) -> PassengerRoseModelUseCase:
    repository: PassengerRoseModelRepository = PassengerRoseModelPgRepository(session=db)
    return PassengerRoseModelInteractor(repository=repository)
