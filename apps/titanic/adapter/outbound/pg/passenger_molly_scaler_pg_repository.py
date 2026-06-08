import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_molly_scaler_dto import PassengerMollyScalerQuery, PassengerMollyScalerResponse
from titanic.app.ports.output.passenger_molly_scaler_repository import PassengerMollyScalerRepository

log = logging.getLogger(__name__)


class PassengerMollyScalerPgRepository(PassengerMollyScalerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: PassengerMollyScalerQuery) -> PassengerMollyScalerResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "PassengerMollyScaler", query.id)
        return PassengerMollyScalerResponse(id=query.id, name=query.name)
