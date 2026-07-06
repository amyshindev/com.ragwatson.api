from fastapi import APIRouter, Depends

from sherlock_holmes.adapter.inbound.api.schemas.inspector_lestrade_official_schema import LestradeOfficialSchema
from sherlock_holmes.app.dtos.inspector_lestrade_official_dto import LestradeOfficialResponse
from sherlock_holmes.app.ports.input.inspector_lestrade_official_use_case import LestradeOfficialUseCase
from sherlock_holmes.dependencies.inspector_lestrade_official_provider import get_inspector_lestrade_official_use_case

lestrade_official_router = APIRouter(prefix="/sherlock/lestrade", tags=["lestrade"])


@lestrade_official_router.get("/myself")
async def introduce_myself(
    character: LestradeOfficialUseCase = Depends(get_inspector_lestrade_official_use_case),
) -> LestradeOfficialResponse:
    return await character.introduce_myself(
        LestradeOfficialSchema(id=3, name="인스펙터 레스트레이드 (Inspector Lestrade)")
    )
