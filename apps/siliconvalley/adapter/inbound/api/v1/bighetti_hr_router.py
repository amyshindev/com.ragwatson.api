from fastapi import APIRouter, Depends

from siliconvalley.adapter.inbound.api.schemas.bighetti_hr_schema import BighettiHrSchema
from siliconvalley.app.dtos.bighetti_hr_dto import BighettiHrResponse
from siliconvalley.app.ports.input.bighetti_hr_use_case import BighettiHrUseCase
from siliconvalley.dependencies.bighetti_hr_provider import get_bighetti_hr_use_case

bighetti_hr_router = APIRouter(prefix="/siliconvalley/bighetti", tags=["bighetti"])


@bighetti_hr_router.get("/myself")
async def introduce_myself(
    character: BighettiHrUseCase = Depends(get_bighetti_hr_use_case),
) -> BighettiHrResponse:
    return await character.introduce_myself(
        BighettiHrSchema(
            id=5,
            name="Bighetti (HR)",
        )
    )
