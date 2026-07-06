from fastapi import APIRouter, Depends

from sherlock_holmes.adapter.inbound.api.schemas.brother_mycroft_strategist_schema import MycroftStrategistSchema
from sherlock_holmes.app.dtos.brother_mycroft_strategist_dto import MycroftStrategistResponse
from sherlock_holmes.app.ports.input.brother_mycroft_strategist_use_case import MycroftStrategistUseCase
from sherlock_holmes.dependencies.brother_mycroft_strategist_provider import get_brother_mycroft_strategist_use_case

mycroft_strategist_router = APIRouter(prefix="/sherlock/mycroft", tags=["mycroft"])


@mycroft_strategist_router.get("/myself")
async def introduce_myself(
    character: MycroftStrategistUseCase = Depends(get_brother_mycroft_strategist_use_case),
) -> MycroftStrategistResponse:
    return await character.introduce_myself(
        MycroftStrategistSchema(id=5, name="마이크로프트 홈즈 (Mycroft Holmes)")
    )
