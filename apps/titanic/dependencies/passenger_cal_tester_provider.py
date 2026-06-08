from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.passenger_cal_tester_pg_repository import PassengerCalTesterPgRepository
from titanic.app.ports.input.passenger_cal_tester_use_case import PassengerCalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import PassengerCalTesterRepository
from titanic.app.use_cases.passenger_cal_tester_interactor import PassengerCalTesterInteractor


def get_passenger_cal_tester_use_case(
    db: AsyncSession = Depends(get_db),
) -> PassengerCalTesterUseCase:
    repository: PassengerCalTesterRepository = PassengerCalTesterPgRepository(session=db)
    return PassengerCalTesterInteractor(repository=repository)
