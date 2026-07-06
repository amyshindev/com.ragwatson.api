from fastapi import APIRouter, Depends

from sherlock_holmes.adapter.inbound.api.schemas.detective_sherlock_holmes_schema import SherlockHolmesSchema
from sherlock_holmes.app.dtos.detective_sherlock_holmes_dto import SherlockHolmesResponse
from sherlock_holmes.app.ports.input.detective_sherlock_holmes_use_case import SherlockHolmesUseCase
from sherlock_holmes.dependencies.detective_sherlock_holmes_provider import get_detective_sherlock_holmes_use_case

detective_sherlock_holmes_router = APIRouter(prefix="/sherlock/holmes", tags=["holmes"])


@detective_sherlock_holmes_router.get("/myself")
async def introduce_myself(
    character: SherlockHolmesUseCase = Depends(get_detective_sherlock_holmes_use_case),
) -> SherlockHolmesResponse:
    return await character.introduce_myself(
        SherlockHolmesSchema(id=1, name="셜록 홈즈 (Sherlock Holmes)")
    )
