from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import CrewHartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import CrewHartleyViolinResponse


class CrewHartleyViolinUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: CrewHartleyViolinSchema) -> CrewHartleyViolinResponse:
        ...
