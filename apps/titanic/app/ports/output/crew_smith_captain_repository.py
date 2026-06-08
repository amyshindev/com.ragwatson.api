from abc import ABC, abstractmethod

from titanic.app.dtos.crew_smith_captain_dto import CrewSmithCaptainQuery, CrewSmithCaptainResponse


class CrewSmithCaptainRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: CrewSmithCaptainQuery) -> CrewSmithCaptainResponse:
        ...
