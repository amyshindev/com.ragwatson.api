from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_ruth_validation_dto import PassengerRuthValidationQuery, PassengerRuthValidationResponse


class PassengerRuthValidationRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: PassengerRuthValidationQuery) -> PassengerRuthValidationResponse:
        ...
