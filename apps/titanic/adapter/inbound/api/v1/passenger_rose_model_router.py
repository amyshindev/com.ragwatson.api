import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import PassengerRoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import PassengerRoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import PassengerRoseModelUseCase
from titanic.dependencies.passenger_rose_model_provider import get_passenger_rose_model_use_case

log = logging.getLogger(__name__)

passenger_rose_model_router = APIRouter(prefix="/api/rose/v1", tags=["rose"])


@passenger_rose_model_router.get("/myself")
async def introduce_myself(
    use_case: PassengerRoseModelUseCase = Depends(get_passenger_rose_model_use_case),
) -> PassengerRoseModelResponse:
    schema = PassengerRoseModelSchema(
        id=10,
        name="Rose DeWitt Bukater",
    )

    log_myself_intro(log, "PassengerRoseModelRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return PassengerRoseModelResponse(
        id=schema.id,
        name=schema.name,
    )
