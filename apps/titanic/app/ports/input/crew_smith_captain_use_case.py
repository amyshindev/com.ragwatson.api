from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import CrewSmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import CrewSmithCaptainResponse


class CrewSmithCaptainUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: CrewSmithCaptainSchema) -> CrewSmithCaptainResponse:
        ...
