from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import (
    RuthValidationSchema,
)
from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationResponse
from titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from titanic.dependencies.passenger_ruth_validation_provider import get_ruth_validation_use_case

"""
루스 드윗 부케이터 (Ruth DeWitt Bukater)
검증 담당 승객으로 데이터·결과 검증 역할을 맡습니다. 최종 검증·품질 확인 역할에 적합합니다.

추천 파일명: ruth_validation_router.py (Validation: 검증 담당)
"""
ruth_validation_router = APIRouter(prefix="/titanic/ruth", tags=["ruth"])


@ruth_validation_router.get("/myself")
async def introduce_myself(
    ruth: RuthValidationUseCase = Depends(get_ruth_validation_use_case),
) -> RuthValidationResponse:
    return await ruth.introduce_myself(
        RuthValidationSchema(id=11, name="루스 드윗 부케이터 (Ruth DeWitt Bukater)")
    )
