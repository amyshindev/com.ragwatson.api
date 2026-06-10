from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case

from fastapi import APIRouter, Depends, HTTPException

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    SmithCaptainChatRequest,
    SmithCaptainChatResponse,
    SmithCaptainSchema,
)

'''
에드워드 스미스 (Edward Smith)
타이타닉호의 선장으로 최종 항해를 지휘했습니다. 전체 오케스트레이션과 최종 의사결정을 맡는 역할에 적합합니다.

추천 파일명: smith_captain_router.py (Captain: 타이타닉호 선장)
'''
smith_captain_router = APIRouter(prefix="/titanic/smith", tags=["smith"])


@smith_captain_router.post("/chat", response_model=SmithCaptainChatResponse)
async def chat_with_smith_captain(
    body: SmithCaptainChatRequest,
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> SmithCaptainChatResponse:
    try:
        reply = await smith.chat_with_smith_captain(body.message)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return SmithCaptainChatResponse(reply=reply)


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
