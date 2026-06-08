from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import PassengerCalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import PassengerCalTesterResponse


class PassengerCalTesterUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: PassengerCalTesterSchema) -> PassengerCalTesterResponse:
        ...
