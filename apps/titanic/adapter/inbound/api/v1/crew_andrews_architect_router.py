import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import CrewAndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import CrewAndrewsArchitectResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import CrewAndrewsArchitectUseCase
from titanic.dependencies.crew_andrews_architect_provider import get_crew_andrews_architect_use_case

log = logging.getLogger(__name__)

crew_andrews_architect_router = APIRouter(prefix="/api/andrews/v1", tags=["andrews"])


@crew_andrews_architect_router.get("/myself")
async def introduce_myself(
    use_case: CrewAndrewsArchitectUseCase = Depends(get_crew_andrews_architect_use_case),
) -> CrewAndrewsArchitectResponse:
    schema = CrewAndrewsArchitectSchema(
        id=2,
        name="Thomas Andrews",
    )

    log_myself_intro(log, "CrewAndrewsArchitectRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return CrewAndrewsArchitectResponse(
        id=schema.id,
        name=schema.name,
    )
