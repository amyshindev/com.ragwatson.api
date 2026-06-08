from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_isidor_couple_dto import PassengerIsidorCoupleQuery, PassengerIsidorCoupleResponse


class PassengerIsidorCoupleRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: PassengerIsidorCoupleQuery) -> PassengerIsidorCoupleResponse:
        ...
