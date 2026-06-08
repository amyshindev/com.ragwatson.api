import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import CrewLoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import CrewLoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import CrewLoweBoatUseCase
from titanic.dependencies.crew_lowe_boat_provider import get_crew_lowe_boat_use_case

log = logging.getLogger(__name__)

crew_lowe_boat_router = APIRouter(prefix="/api/lowe/v1", tags=["lowe"])


@crew_lowe_boat_router.get("/myself")
async def introduce_myself(
    use_case: CrewLoweBoatUseCase = Depends(get_crew_lowe_boat_use_case),
) -> CrewLoweBoatResponse:
    schema = CrewLoweBoatSchema(
        id=4,
        name="Harold Lowe",
    )

    log_myself_intro(log, "CrewLoweBoatRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return CrewLoweBoatResponse(
        id=schema.id,
        name=schema.name,
    )
