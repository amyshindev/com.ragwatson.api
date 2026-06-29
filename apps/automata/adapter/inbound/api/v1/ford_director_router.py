from fastapi import APIRouter, Depends

from automata.adapter.inbound.api.schemas.ford_director_schema import (
    FordDirectorSchema,
    FordDirectorTriggerSchema,
)
from automata.app.dtos.ford_director_dto import FordDirectorResponse
from automata.app.ports.input.ford_director_use_case import FordDirectorUseCase
from automata.dependencies.ford_director_provider import get_ford_director_use_case

ford_director_router = APIRouter(prefix="/automata/ford", tags=["automata", "ford"])


@ford_director_router.get("/myself")
async def introduce_myself(
    ford: FordDirectorUseCase = Depends(get_ford_director_use_case),
) -> FordDirectorResponse:
    return await ford.introduce_myself(
        FordDirectorSchema(id=1, name="Robert Ford (Director)"),
    )


@ford_director_router.post("/trigger")
async def trigger_workflow(
    body: FordDirectorTriggerSchema,
    ford: FordDirectorUseCase = Depends(get_ford_director_use_case),
) -> FordDirectorResponse:
    return await ford.trigger_workflow(body)
