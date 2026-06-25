from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_walter_roaster_use_case

walter_roaster_router = APIRouter(prefix="/titanic/walter", tags=["walter"])


@walter_roaster_router.get("/myself")
async def introduce_myself(
    walter: WalterRoasterUseCase = Depends(get_walter_roaster_use_case),
) -> WalterRoasterResponse:
    return await walter.introduce_myself(
        WalterRoasterSchema(id=2, name="Hugh Walter McElroy"),
    )
