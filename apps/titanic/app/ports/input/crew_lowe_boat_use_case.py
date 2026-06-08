from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import CrewLoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import CrewLoweBoatResponse


class CrewLoweBoatUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: CrewLoweBoatSchema) -> CrewLoweBoatResponse:
        ...
