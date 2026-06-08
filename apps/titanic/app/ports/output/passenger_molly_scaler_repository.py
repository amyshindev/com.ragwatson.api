from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_molly_scaler_dto import PassengerMollyScalerQuery, PassengerMollyScalerResponse


class PassengerMollyScalerRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: PassengerMollyScalerQuery) -> PassengerMollyScalerResponse:
        ...
