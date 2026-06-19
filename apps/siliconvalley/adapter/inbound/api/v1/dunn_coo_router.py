from fastapi import APIRouter, Depends

from siliconvalley.adapter.inbound.api.schemas.dunn_coo_schema import DunnCooSchema
from siliconvalley.app.dtos.dunn_coo_dto import DunnCooResponse
from siliconvalley.app.ports.input.dunn_coo_use_case import DunnCooUseCase
from siliconvalley.dependencies.dunn_coo_provider import get_dunn_coo_use_case

dunn_coo_router = APIRouter(prefix="/siliconvalley/dunn", tags=["dunn"])


@dunn_coo_router.get("/myself")
async def introduce_myself(
    character: DunnCooUseCase = Depends(get_dunn_coo_use_case),
) -> DunnCooResponse:
    return await character.introduce_myself(
        DunnCooSchema(
            id=4,
            name='Dunn (COO)',
        )
    )
