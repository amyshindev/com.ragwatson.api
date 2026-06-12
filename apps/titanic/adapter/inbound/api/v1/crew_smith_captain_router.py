import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatResponseSchema,
    ChatSchema,
    SmithCaptainSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case

'''
에드워드 스미스 (Edward Smith)
타이타닉호의 선장으로 최종 항해를 지휘했습니다. 전체 오케스트레이션과 최종 의사결정을 맡는 역할에 적합합니다.

추천 파일명: smith_captain_router.py (Captain: 타이타닉호 선장)
'''
logger = logging.getLogger(__name__)

smith_captain_router = APIRouter(prefix="/titanic/smith", tags=["smith"])



@smith_captain_router.post("/chat")
async def chat(
    schema: Annotated[ChatSchema, Body()],
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> ChatResponseSchema:
    logger.info(
        "POST /titanic/smith/chat request body: message=%r",
        schema.message,
    )
    return ChatResponseSchema(reply=await smith.chat(schema))



@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case)
) -> SmithCaptainResponse:
    return await smith.introduce_myself(
        SmithCaptainSchema(
            id=5,
            name="에드워드 스미스 (Edward Smith)"
        )
    )
