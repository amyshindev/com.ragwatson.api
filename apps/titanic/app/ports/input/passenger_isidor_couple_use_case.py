from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import PassengerIsidorCoupleSchema
from titanic.app.dtos.passenger_isidor_couple_dto import PassengerIsidorCoupleResponse


class PassengerIsidorCoupleUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: PassengerIsidorCoupleSchema) -> PassengerIsidorCoupleResponse:
        ...
