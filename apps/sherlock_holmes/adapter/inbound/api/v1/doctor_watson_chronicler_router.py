from fastapi import APIRouter, Depends

from sherlock_holmes.adapter.inbound.api.schemas.doctor_watson_chronicler_schema import WatsonChroniclerSchema
from sherlock_holmes.app.dtos.doctor_watson_chronicler_dto import WatsonChroniclerResponse
from sherlock_holmes.app.ports.input.doctor_watson_chronicler_use_case import WatsonChroniclerUseCase
from sherlock_holmes.dependencies.doctor_watson_chronicler_provider import get_doctor_watson_chronicler_use_case

watson_chronicler_router = APIRouter(prefix="/sherlock/watson", tags=["watson"])


@watson_chronicler_router.get("/myself")
async def introduce_myself(
    character: WatsonChroniclerUseCase = Depends(get_doctor_watson_chronicler_use_case),
) -> WatsonChroniclerResponse:
    return await character.introduce_myself(
        WatsonChroniclerSchema(id=2, name="존 H. 왓슨 (Dr. John Watson)")
    )
