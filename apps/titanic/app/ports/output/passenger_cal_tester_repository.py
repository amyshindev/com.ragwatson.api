from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_cal_tester_dto import PassengerCalTesterQuery, PassengerCalTesterResponse


class PassengerCalTesterRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: PassengerCalTesterQuery) -> PassengerCalTesterResponse:
        ...
