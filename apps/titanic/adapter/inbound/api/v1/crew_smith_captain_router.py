import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import CrewSmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import CrewSmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import CrewSmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_crew_smith_captain_use_case

log = logging.getLogger(__name__)

crew_smith_captain_router = APIRouter(prefix="/api/smith/v1", tags=["smith"])


@crew_smith_captain_router.get("/myself")
async def introduce_myself(
    use_case: CrewSmithCaptainUseCase = Depends(get_crew_smith_captain_use_case),
) -> CrewSmithCaptainResponse:
    schema = CrewSmithCaptainSchema(
        id=5,
        name="Edward Smith",
    )

    log_myself_intro(log, "CrewSmithCaptainRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return CrewSmithCaptainResponse(
        id=schema.id,
        name=schema.name,
    )
