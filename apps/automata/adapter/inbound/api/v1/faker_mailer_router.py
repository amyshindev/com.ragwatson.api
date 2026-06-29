import logging

from fastapi import APIRouter, Depends, HTTPException

from automata.adapter.inbound.api.schemas.faker_mailer_schema import (
    FakerEmailRequestSchema,
    FakerEmailResponseSchema,
)
from automata.app.ports.input.faker_mailer_use_case import FakerMailerUseCase
from automata.dependencies.faker_mailer_provider import get_faker_mailer_use_case

logger = logging.getLogger(__name__)

faker_mailer_router = APIRouter(prefix="/automata/faker", tags=["automata", "faker"])


@faker_mailer_router.post("/email", response_model=FakerEmailResponseSchema)
async def send_faker_email(
    body: FakerEmailRequestSchema,
    faker_mailer: FakerMailerUseCase = Depends(get_faker_mailer_use_case),
) -> FakerEmailResponseSchema:
    try:
        result = await faker_mailer.send_email(body)
    except RuntimeError as exc:
        logger.warning("[faker_mailer_router] ExaONE unavailable: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="ExaONE(Ollama)이 준비되지 않았습니다. Ollama를 실행하고 exaone3.5:2.4b 모델을 pull 해주세요.",
        ) from exc

    if not result.ok:
        raise HTTPException(
            status_code=502,
            detail=f"n8n Gmail 발송에 실패했습니다. 상태: {result.n8n_status}",
        )

    return result
