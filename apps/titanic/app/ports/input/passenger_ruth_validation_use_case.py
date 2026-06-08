from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import PassengerRuthValidationSchema
from titanic.app.dtos.passenger_ruth_validation_dto import PassengerRuthValidationResponse


class PassengerRuthValidationUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: PassengerRuthValidationSchema) -> PassengerRuthValidationResponse:
        ...
