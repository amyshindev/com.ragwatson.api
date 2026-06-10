from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_walter_roaster_use_case
'''
휴 월터 맥엘로이 (Hugh Walter McElroy)
타이타닉 일등 항해사로 승객 명단 관리를 담당했습니다. 데이터 적재·조회·리더 역할에 적합합니다.

추천 파일명: walter_roaster_router.py (Roaster: 승객 명단 관리)
'''
walter_roaster_router = APIRouter(prefix="/titanic/walter", tags=["walter"])

@walter_roaster_router.get("/myself")
async def introduce_myself(
    walter: WalterRoasterUseCase = Depends(get_walter_roaster_use_case)
) -> WalterRoasterResponse:
    return await walter.introduce_myself(
        WalterRoasterSchema(
            id=1,
            name="휴 월터 맥엘로이 (Hugh Walter McElroy)"
        )
    )
