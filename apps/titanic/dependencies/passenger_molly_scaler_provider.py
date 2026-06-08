from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.passenger_molly_scaler_pg_repository import PassengerMollyScalerPgRepository
from titanic.app.ports.input.passenger_molly_scaler_use_case import PassengerMollyScalerUseCase
from titanic.app.ports.output.passenger_molly_scaler_repository import PassengerMollyScalerRepository
from titanic.app.use_cases.passenger_molly_scaler_interactor import PassengerMollyScalerInteractor


def get_passenger_molly_scaler_use_case(
    db: AsyncSession = Depends(get_db),
) -> PassengerMollyScalerUseCase:
    repository: PassengerMollyScalerRepository = PassengerMollyScalerPgRepository(session=db)
    return PassengerMollyScalerInteractor(repository=repository)
