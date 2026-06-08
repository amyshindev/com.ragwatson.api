from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import PassengerMollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import PassengerMollyScalerResponse


class PassengerMollyScalerUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: PassengerMollyScalerSchema) -> PassengerMollyScalerResponse:
        ...
