from fastapi import APIRouter, Depends

from sherlock_holmes.adapter.inbound.api.schemas.professor_moriarty_rival_schema import MoriartyRivalSchema
from sherlock_holmes.app.dtos.professor_moriarty_rival_dto import MoriartyRivalResponse
from sherlock_holmes.app.ports.input.professor_moriarty_rival_use_case import MoriartyRivalUseCase
from sherlock_holmes.dependencies.professor_moriarty_rival_provider import get_professor_moriarty_rival_use_case

moriarty_rival_router = APIRouter(prefix="/sherlock/moriarty", tags=["moriarty"])


@moriarty_rival_router.get("/myself")
async def introduce_myself(
    character: MoriartyRivalUseCase = Depends(get_professor_moriarty_rival_use_case),
) -> MoriartyRivalResponse:
    return await character.introduce_myself(
        MoriartyRivalSchema(id=6, name="프로페서 모리어티 (Professor Moriarty)")
    )
