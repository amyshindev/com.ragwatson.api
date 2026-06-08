import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_cal_tester_dto import PassengerCalTesterQuery, PassengerCalTesterResponse
from titanic.app.ports.output.passenger_cal_tester_repository import PassengerCalTesterRepository

log = logging.getLogger(__name__)


class PassengerCalTesterPgRepository(PassengerCalTesterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: PassengerCalTesterQuery) -> PassengerCalTesterResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "PassengerCalTester", query.id)
        return PassengerCalTesterResponse(id=query.id, name=query.name)
