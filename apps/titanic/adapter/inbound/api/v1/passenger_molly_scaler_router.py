from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse
from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.dependencies.passenger_molly_scaler_provider import get_molly_scaler_use_case
'''
몰리 브라운 (Molly Brown)
생존자로 피처 스케일링을 담당하는 승객입니다. 전처리·정규화·스케일링 역할에 적합합니다.

추천 파일명: molly_scaler_router.py (Scaler: 피처 스케일링)
'''
molly_scaler_router = APIRouter(prefix="/titanic/molly", tags=["molly"])

@molly_scaler_router.get("/myself")
async def introduce_myself(
    molly: MollyScalerUseCase = Depends(get_molly_scaler_use_case)
) -> MollyScalerResponse:
    return await molly.introduce_myself(
        MollyScalerSchema(
            id=9,
            name="몰리 브라운 (Molly Brown)"
        )
    )
