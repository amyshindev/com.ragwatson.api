from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository


class CaledonValidation(BaseModel):
    Pclass: int = Field(..., ge=1, le=3, description="Ticket class")
    Sex: Literal["male", "female"] = Field(..., description="Gender")
    Age: float = Field(..., ge=0.0, description="Age")
    SibSp: int = Field(..., ge=0, description="Siblings/spouses aboard")
    Parch: int = Field(..., ge=0, description="Parents/children aboard")
    Fare: float = Field(..., ge=0.0, description="Fare")

    class Config:
        json_schema_extra = {
            "example": {
                "Pclass": 3,
                "Sex": "male",
                "Age": 22.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 7.25,
            }
        }


class CalTesterInteractor(CalTesterUseCase):
    
    def __init__(self, repository: CalTesterRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''? ???? ???? ????'''

        return await self.repository.introduce_myself(CalTesterQuery(
            id = schema.id,
            name = schema.name
        ))


PassengerCalTesterInteractor = CalTesterInteractor
