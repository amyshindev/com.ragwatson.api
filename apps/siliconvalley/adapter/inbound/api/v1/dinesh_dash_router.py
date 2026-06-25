from fastapi import APIRouter, Depends

from siliconvalley.adapter.inbound.api.schemas.dinesh_dash_schema import DineshDashSchema
from siliconvalley.app.dtos.dinesh_dash_dto import DineshDashResponse
from siliconvalley.app.ports.input.dinesh_dash_use_case import DineshDashUseCase
from siliconvalley.dependencies.dinesh_dash_provider import get_dinesh_dash_use_case

dinesh_dash_router = APIRouter(prefix="/siliconvalley/dinesh", tags=["dinesh"])


@dinesh_dash_router.get("/myself")
async def introduce_myself(
    character: DineshDashUseCase = Depends(get_dinesh_dash_use_case),
) -> DineshDashResponse:
    return await character.introduce_myself(
        DineshDashSchema(
            id=3,
            name="Dinesh Chugtai (Dash)",
        )
    )
