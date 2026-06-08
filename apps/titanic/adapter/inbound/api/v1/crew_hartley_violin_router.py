import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.myself_log import log_myself_intro
from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import CrewHartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import CrewHartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import CrewHartleyViolinUseCase
from titanic.dependencies.crew_hartley_violin_provider import get_crew_hartley_violin_use_case

log = logging.getLogger(__name__)

crew_hartley_violin_router = APIRouter(prefix="/api/hartley/v1", tags=["hartley"])


@crew_hartley_violin_router.get("/myself")
async def introduce_myself(
    use_case: CrewHartleyViolinUseCase = Depends(get_crew_hartley_violin_use_case),
) -> CrewHartleyViolinResponse:
    schema = CrewHartleyViolinSchema(
        id=3,
        name="Wallace Hartley",
    )

    log_myself_intro(log, "CrewHartleyViolinRouter", schema.id, schema.name)
    await use_case.introduce_myself(schema)

    return CrewHartleyViolinResponse(
        id=schema.id,
        name=schema.name,
    )
