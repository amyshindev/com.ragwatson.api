from abc import ABC, abstractmethod

from titanic.app.dtos.crew_hartley_violin_dto import CrewHartleyViolinQuery, CrewHartleyViolinResponse


class CrewHartleyViolinRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: CrewHartleyViolinQuery) -> CrewHartleyViolinResponse:
        ...
