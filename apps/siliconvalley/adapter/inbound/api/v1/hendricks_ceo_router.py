from fastapi import APIRouter, Depends

from siliconvalley.adapter.inbound.api.schemas.hendricks_ceo_schema import HendricksCeoSchema
from siliconvalley.app.dtos.hendricks_ceo_dto import HendricksCeoResponse
from siliconvalley.app.ports.input.hendricks_ceo_use_case import HendricksCeoUseCase
from siliconvalley.dependencies.hendricks_ceo_provider import get_hendricks_ceo_use_case

hendricks_ceo_router = APIRouter(prefix="/siliconvalley/hendricks", tags=["hendricks"])


@hendricks_ceo_router.get("/myself")
async def introduce_myself(
    character: HendricksCeoUseCase = Depends(get_hendricks_ceo_use_case),
) -> HendricksCeoResponse:
    return await character.introduce_myself(
        HendricksCeoSchema(
            id=1,
            name='Richard Hendricks (CEO)',
        )
    )
