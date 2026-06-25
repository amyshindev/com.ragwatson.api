from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case

"""
잭 도슨 (Jack Dawson)
3등석 승객으로 생존 예측 모델 학습을 담당합니다. ML 학습·파이프라인 오케스트레이션 역할에 적합합니다.

추천 파일명: jack_trainer_router.py (Trainer: 생존 예측 모델 학습)
"""
jack_trainer_router = APIRouter(prefix="/titanic/jack", tags=["jack"])


@jack_trainer_router.get("/myself")
async def introduce_myself(
    jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
) -> JackTrainerResponse:
    return await jack.introduce_myself(JackTrainerSchema(id=8, name="잭 도슨 (Jack Dawson)"))
