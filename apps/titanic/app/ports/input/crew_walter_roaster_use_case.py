from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import CrewWalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import CrewWalterRoasterResponse


class CrewWalterRoasterUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: CrewWalterRoasterSchema) -> CrewWalterRoasterResponse:
        ...
