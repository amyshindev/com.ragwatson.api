from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_roaster_dto import CrewWalterRoasterQuery, CrewWalterRoasterResponse


class CrewWalterRoasterRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: CrewWalterRoasterQuery) -> CrewWalterRoasterResponse:
        ...
