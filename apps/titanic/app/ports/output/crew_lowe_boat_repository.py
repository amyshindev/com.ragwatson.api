from abc import ABC, abstractmethod

from titanic.app.dtos.crew_lowe_boat_dto import CrewLoweBoatQuery, CrewLoweBoatResponse


class CrewLoweBoatRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: CrewLoweBoatQuery) -> CrewLoweBoatResponse:
        ...
