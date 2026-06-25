from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.dependencies.crew_lowe_boat_provider import get_lowe_boat_use_case

"""
해롤드 로우 (Harold Lowe)
5등 항해사로 구명보트 배정과 구조 작전을 담당했습니다. 배치·할당·리소스 분배 로직을 담당하는 역할로 좋습니다.

추천 파일명: lowe_boat_router.py (Boat: 구명보트 배정 담당)
"""
lowe_boat_router = APIRouter(prefix="/titanic/lowe", tags=["lowe"])


@lowe_boat_router.get("/myself")
async def introduce_myself(
    lowe: LoweBoatUseCase = Depends(get_lowe_boat_use_case),
) -> LoweBoatResponse:
    return await lowe.introduce_myself(LoweBoatSchema(id=4, name="해롤드 로우 (Harold Lowe)"))
