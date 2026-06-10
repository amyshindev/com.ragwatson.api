from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.dependencies.passenger_cal_tester_provider import get_cal_tester_use_case
'''
캘러든 호클리 (Caledon Hockley)
1등석 승객으로 탑승 데이터 유효성 검증 테스터 역할을 맡습니다. 입력 검증·스키마 확인 역할에 적합합니다.

추천 파일명: cal_tester_router.py (Tester: 탑승 데이터 검증)
'''
cal_tester_router = APIRouter(prefix="/titanic/cal", tags=["cal"])

@cal_tester_router.get("/myself")
async def introduce_myself(
    cal: CalTesterUseCase = Depends(get_cal_tester_use_case)
) -> CalTesterResponse:
    return await cal.introduce_myself(
        CalTesterSchema(
            id=6,
            name="캘러든 호클리 (Caledon Hockley)"
        )
    )
