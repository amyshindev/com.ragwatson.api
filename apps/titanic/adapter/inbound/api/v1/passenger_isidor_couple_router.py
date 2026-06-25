from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IsidorCoupleSchema
from titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleResponse
from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.dependencies.passenger_isidor_couple_provider import get_isidor_couple_use_case

"""
이시도르 스트라우스 (Isidor Straus)
1등석 승객으로 부인과 함께 탑승한 부부입니다. 페어 데이터·관계형 레코드 처리 역할에 적합합니다.

추천 파일명: isidor_couple_router.py (Couple: 부부 동반 승객)
"""
isidor_couple_router = APIRouter(prefix="/titanic/isidor", tags=["isidor"])


@isidor_couple_router.get("/myself")
async def introduce_myself(
    isidor: IsidorCoupleUseCase = Depends(get_isidor_couple_use_case),
) -> IsidorCoupleResponse:
    return await isidor.introduce_myself(
        IsidorCoupleSchema(id=7, name="이시도르 스트라우스 (Isidor Straus)")
    )
