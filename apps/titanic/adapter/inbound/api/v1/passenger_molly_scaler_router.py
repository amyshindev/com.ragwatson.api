import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import PassengerMollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import PassengerMollyScalerResponse
from titanic.app.ports.input.passenger_molly_scaler_use_case import PassengerMollyScalerUseCase
from titanic.dependencies.passenger_molly_scaler_provider import get_passenger_molly_scaler_use_case

log = logging.getLogger(__name__)

passenger_molly_scaler_router = APIRouter(prefix="/api/molly/v1", tags=["molly"])


@passenger_molly_scaler_router.get("/myself")
async def introduce_myself(
    use_case: PassengerMollyScalerUseCase = Depends(get_passenger_molly_scaler_use_case),
) -> PassengerMollyScalerResponse:
    schema = PassengerMollyScalerSchema(
        id=9,
        name="Molly Brown",
    )

    log_myself_intro(log, "PassengerMollyScalerRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return PassengerMollyScalerResponse(
        id=schema.id,
        name=schema.name,
    )
