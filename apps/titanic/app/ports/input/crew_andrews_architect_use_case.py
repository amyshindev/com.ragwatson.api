from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import CrewAndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import CrewAndrewsArchitectResponse


class CrewAndrewsArchitectUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: CrewAndrewsArchitectSchema) -> CrewAndrewsArchitectResponse:
        ...
