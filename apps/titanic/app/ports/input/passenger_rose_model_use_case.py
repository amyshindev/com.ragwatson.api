from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import PassengerRoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import PassengerRoseModelResponse


class PassengerRoseModelUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: PassengerRoseModelSchema) -> PassengerRoseModelResponse:
        ...
