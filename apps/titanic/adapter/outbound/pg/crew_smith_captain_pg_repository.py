from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
import asyncio
from core.matrix.keymaker_api import keymaker

log = logging.getLogger(__name__)


class SmithCaptainPgRepository(SmithCaptainRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        '''스미스 선장의 자기 소개 레포지토리 구현 메소드'''
        log.info("[SmithCaptainPgRepository] introduce_myself id=%s", query.id)
        return SmithCaptainResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )


    async def chat(self, schema: ChatSchema) -> str:
        if not keymaker.has_gemini():
            raise RuntimeError("GEMINI_API_KEY is not set")

        model = keymaker.get_gemini_model()
        if model is None:
            raise RuntimeError("Gemini model is not configured")

        persona = (
            "당신은 RMS 타이타닉호의 선장 에드워드 스미스(Edward Smith)입니다. "
            "1912년 항해와 선박 운영에 대한 질문에 답하되, 항상 선장 캐릭터를 유지하세요. "
            "답변은 한국어로 간결하고 정중하게 작성하세요."
        )
        prompt = f"{persona}\n\n사용자: {schema.message}"

        def _generate():
            return model.generate_content(prompt)

        response = await asyncio.to_thread(_generate)

        try:
            return response.text
        except ValueError as exc:
            raise RuntimeError("Model returned no text (empty or blocked).") from exc


CrewSmithCaptainPgRepository = SmithCaptainPgRepository
