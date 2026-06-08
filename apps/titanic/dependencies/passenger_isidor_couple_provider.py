from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.passenger_isidor_couple_pg_repository import PassengerIsidorCouplePgRepository
from titanic.app.ports.input.passenger_isidor_couple_use_case import PassengerIsidorCoupleUseCase
from titanic.app.ports.output.passenger_isidor_couple_repository import PassengerIsidorCoupleRepository
from titanic.app.use_cases.passenger_isidor_couple_interactor import PassengerIsidorCoupleInteractor


def get_passenger_isidor_couple_use_case(
    db: AsyncSession = Depends(get_db),
) -> PassengerIsidorCoupleUseCase:
    repository: PassengerIsidorCoupleRepository = PassengerIsidorCouplePgRepository(session=db)
    return PassengerIsidorCoupleInteractor(repository=repository)
