from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import PassengerJackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import PassengerJackTrainerResponse


class PassengerJackTrainerUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: PassengerJackTrainerSchema) -> PassengerJackTrainerResponse:
        ...
