import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import PassengerIsidorCoupleSchema
from titanic.app.dtos.passenger_isidor_couple_dto import PassengerIsidorCoupleResponse
from titanic.app.ports.input.passenger_isidor_couple_use_case import PassengerIsidorCoupleUseCase
from titanic.dependencies.passenger_isidor_couple_provider import get_passenger_isidor_couple_use_case

log = logging.getLogger(__name__)

passenger_isidor_couple_router = APIRouter(prefix="/api/isidor/v1", tags=["isidor"])


@passenger_isidor_couple_router.get("/myself")
async def introduce_myself(
    use_case: PassengerIsidorCoupleUseCase = Depends(get_passenger_isidor_couple_use_case),
) -> PassengerIsidorCoupleResponse:
    schema = PassengerIsidorCoupleSchema(
        id=7,
        name="Isidor Straus",
    )

    log_myself_intro(log, "PassengerIsidorCoupleRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return PassengerIsidorCoupleResponse(
        id=schema.id,
        name=schema.name,
    )
