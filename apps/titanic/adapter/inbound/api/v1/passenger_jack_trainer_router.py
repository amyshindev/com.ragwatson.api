import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import PassengerJackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import PassengerJackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import PassengerJackTrainerUseCase
from titanic.dependencies.passenger_jack_trainer_provider import get_passenger_jack_trainer_use_case

log = logging.getLogger(__name__)

passenger_jack_trainer_router = APIRouter(prefix="/api/jack/v1", tags=["jack"])


@passenger_jack_trainer_router.get("/myself")
async def introduce_myself(
    use_case: PassengerJackTrainerUseCase = Depends(get_passenger_jack_trainer_use_case),
) -> PassengerJackTrainerResponse:
    schema = PassengerJackTrainerSchema(
        id=8,
        name="Jack Dawson",
    )

    log_myself_intro(log, "PassengerJackTrainerRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return PassengerJackTrainerResponse(
        id=schema.id,
        name=schema.name,
    )
