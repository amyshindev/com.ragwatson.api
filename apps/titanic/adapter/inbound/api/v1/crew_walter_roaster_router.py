import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import CrewWalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import CrewWalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import CrewWalterRoasterUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_crew_walter_roaster_use_case

log = logging.getLogger(__name__)

crew_walter_roaster_router = APIRouter(prefix="/api/walter/v1", tags=["walter-reader"])


@crew_walter_roaster_router.get("/myself")
async def introduce_myself(
    use_case: CrewWalterRoasterUseCase = Depends(get_crew_walter_roaster_use_case),
) -> CrewWalterRoasterResponse:
    schema = CrewWalterRoasterSchema(
        id=1,
        name="Hugh Walter McElroy",
    )

    log_myself_intro(log, "CrewWalterRoasterRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return CrewWalterRoasterResponse(
        id=schema.id,
        name=schema.name,
    )
