import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_isidor_couple_dto import PassengerIsidorCoupleQuery, PassengerIsidorCoupleResponse
from titanic.app.ports.output.passenger_isidor_couple_repository import PassengerIsidorCoupleRepository

log = logging.getLogger(__name__)


class PassengerIsidorCouplePgRepository(PassengerIsidorCoupleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: PassengerIsidorCoupleQuery) -> PassengerIsidorCoupleResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "PassengerIsidorCouple", query.id)
        return PassengerIsidorCoupleResponse(id=query.id, name=query.name)
