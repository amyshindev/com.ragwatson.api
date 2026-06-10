from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case
'''
로즈 드윗 부케이터 (Rose DeWitt Bukater)
1등석 승객으로 의사결정나무 생존 모델을 소유합니다. 모델 추론·예측 결과 제공 역할에 적합합니다.

추천 파일명: rose_model_router.py (Model: 의사결정나무 생존 모델)
'''
rose_model_router = APIRouter(prefix="/titanic/rose", tags=["rose"])

@rose_model_router.get("/myself")
async def introduce_myself(
    rose: RoseModelUseCase = Depends(get_rose_model_use_case)
) -> RoseModelResponse:
    return await rose.introduce_myself(
        RoseModelSchema(
            id=10,
            name="로즈 드윗 부케이터 (Rose DeWitt Bukater)"
        )
    )
