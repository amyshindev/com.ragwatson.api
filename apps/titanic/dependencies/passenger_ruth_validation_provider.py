from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.passenger_ruth_validation_pg_repository import PassengerRuthValidationPgRepository
from titanic.app.ports.input.passenger_ruth_validation_use_case import PassengerRuthValidationUseCase
from titanic.app.ports.output.passenger_ruth_validation_repository import PassengerRuthValidationRepository
from titanic.app.use_cases.passenger_ruth_validation_interactor import PassengerRuthValidationInteractor


def get_passenger_ruth_validation_use_case(
    db: AsyncSession = Depends(get_db),
) -> PassengerRuthValidationUseCase:
    repository: PassengerRuthValidationRepository = PassengerRuthValidationPgRepository(session=db)
    return PassengerRuthValidationInteractor(repository=repository)
