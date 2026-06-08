from abc import ABC, abstractmethod

from titanic.app.dtos.crew_andrews_architect_dto import CrewAndrewsArchitectQuery, CrewAndrewsArchitectResponse


class CrewAndrewsArchitectRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: CrewAndrewsArchitectQuery) -> CrewAndrewsArchitectResponse:
        ...
