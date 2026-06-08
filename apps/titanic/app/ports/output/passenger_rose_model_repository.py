from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_rose_model_dto import PassengerRoseModelQuery, PassengerRoseModelResponse


class PassengerRoseModelRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: PassengerRoseModelQuery) -> PassengerRoseModelResponse:
        ...
