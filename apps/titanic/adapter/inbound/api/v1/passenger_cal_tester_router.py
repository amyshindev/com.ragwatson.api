import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import PassengerCalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import PassengerCalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import PassengerCalTesterUseCase
from titanic.dependencies.passenger_cal_tester_provider import get_passenger_cal_tester_use_case

log = logging.getLogger(__name__)

passenger_cal_tester_router = APIRouter(prefix="/api/cal/v1", tags=["cal"])


@passenger_cal_tester_router.get("/myself")
async def introduce_myself(
    use_case: PassengerCalTesterUseCase = Depends(get_passenger_cal_tester_use_case),
) -> PassengerCalTesterResponse:
    schema = PassengerCalTesterSchema(
        id=6,
        name="Caledon Hockley",
    )

    log_myself_intro(log, "PassengerCalTesterRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return PassengerCalTesterResponse(
        id=schema.id,
        name=schema.name,
    )
