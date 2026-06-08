import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import PassengerRuthValidationSchema
from titanic.app.dtos.passenger_ruth_validation_dto import PassengerRuthValidationResponse
from titanic.app.ports.input.passenger_ruth_validation_use_case import PassengerRuthValidationUseCase
from titanic.dependencies.passenger_ruth_validation_provider import get_passenger_ruth_validation_use_case

log = logging.getLogger(__name__)

passenger_ruth_validation_router = APIRouter(prefix="/api/ruth/v1", tags=["ruth"])


@passenger_ruth_validation_router.get("/myself")
async def introduce_myself(
    use_case: PassengerRuthValidationUseCase = Depends(get_passenger_ruth_validation_use_case),
) -> PassengerRuthValidationResponse:
    schema = PassengerRuthValidationSchema(
        id=11,
        name="Ruth DeWitt Bukater",
    )

    log_myself_intro(log, "PassengerRuthValidationRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return PassengerRuthValidationResponse(
        id=schema.id,
        name=schema.name,
    )
