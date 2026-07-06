from fastapi import APIRouter, Depends

from sherlock_holmes.adapter.inbound.api.schemas.mrs_hudson_housekeeper_schema import HudsonHousekeeperSchema
from sherlock_holmes.app.dtos.mrs_hudson_housekeeper_dto import HudsonHousekeeperResponse
from sherlock_holmes.app.ports.input.mrs_hudson_housekeeper_use_case import HudsonHousekeeperUseCase
from sherlock_holmes.dependencies.mrs_hudson_housekeeper_provider import get_mrs_hudson_housekeeper_use_case

hudson_housekeeper_router = APIRouter(prefix="/sherlock/hudson", tags=["hudson"])


@hudson_housekeeper_router.get("/myself")
async def introduce_myself(
    character: HudsonHousekeeperUseCase = Depends(get_mrs_hudson_housekeeper_use_case),
) -> HudsonHousekeeperResponse:
    return await character.introduce_myself(
        HudsonHousekeeperSchema(id=4, name="미스 허드슨 (Mrs. Hudson)")
    )
