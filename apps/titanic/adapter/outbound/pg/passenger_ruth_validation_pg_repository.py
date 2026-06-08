import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_ruth_validation_dto import PassengerRuthValidationQuery, PassengerRuthValidationResponse
from titanic.app.ports.output.passenger_ruth_validation_repository import PassengerRuthValidationRepository

log = logging.getLogger(__name__)


class PassengerRuthValidationPgRepository(PassengerRuthValidationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: PassengerRuthValidationQuery) -> PassengerRuthValidationResponse:
        log.info("[%sPgRepository] introduce_myself id=%s", "PassengerRuthValidation", query.id)
        return PassengerRuthValidationResponse(id=query.id, name=query.name)
