from fastapi import APIRouter, Depends

from siliconvalley.adapter.inbound.api.schemas.gilfoyle_system_schema import GilfoyleSystemSchema
from siliconvalley.app.dtos.gilfoyle_system_dto import GilfoyleSystemResponse
from siliconvalley.app.ports.input.gilfoyle_system_use_case import GilfoyleSystemUseCase
from siliconvalley.dependencies.gilfoyle_system_provider import get_gilfoyle_system_use_case

gilfoyle_system_router = APIRouter(prefix="/siliconvalley/gilfoyle", tags=["gilfoyle"])


@gilfoyle_system_router.get("/myself")
async def introduce_myself(
    character: GilfoyleSystemUseCase = Depends(get_gilfoyle_system_use_case),
) -> GilfoyleSystemResponse:
    return await character.introduce_myself(
        GilfoyleSystemSchema(
            id=2,
            name='Bertram Gilfoyle (System)',
        )
    )
