from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_jack_trainer_dto import PassengerJackTrainerQuery, PassengerJackTrainerResponse


class PassengerJackTrainerRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: PassengerJackTrainerQuery) -> PassengerJackTrainerResponse:
        ...
