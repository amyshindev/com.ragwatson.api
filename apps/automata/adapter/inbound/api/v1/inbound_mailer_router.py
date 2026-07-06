import logging

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from automata.adapter.inbound.api.schemas.inbound_mailer_schema import (
    InboundMailListResponseSchema,
    InboundMailReceiveResponseSchema,
    InboundMailReceiveSchema,
)
from automata.app.ports.input.inbound_mail_use_case import InboundMailUseCase
from automata.dependencies.inbound_mailer_provider import (
    get_inbound_mail_use_case,
    get_inbound_secret,
)

log = logging.getLogger(__name__)

inbound_mailer_router = APIRouter(prefix="/automata/inbound", tags=["automata", "inbound"])


def _verify_inbound_secret(
    x_automata_inbound_secret: str | None = Header(default=None, alias="X-Automata-Inbound-Secret"),
) -> None:
    expected = get_inbound_secret()
    if expected is None:
        return
    if x_automata_inbound_secret != expected:
        raise HTTPException(status_code=401, detail="수신 웹훅 인증에 실패했습니다.")


@inbound_mailer_router.post("/mail", response_model=InboundMailReceiveResponseSchema)
async def receive_inbound_mail(
    body: InboundMailReceiveSchema,
    _: None = Depends(_verify_inbound_secret),
    inbound_mail: InboundMailUseCase = Depends(get_inbound_mail_use_case),
) -> InboundMailReceiveResponseSchema:
    log.info(
        "[InboundMailerRouter] receive from=%s subject=%s message_id=%s",
        body.from_email,
        body.subject,
        body.message_id,
    )
    try:
        return await inbound_mail.receive_mail(body)
    except RuntimeError as exc:
        log.warning("[InboundMailerRouter] embedding/store failed: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="메일 저장 또는 임베딩 생성에 실패했습니다. Ollama와 DATABASE_URL을 확인하세요.",
        ) from exc


@inbound_mailer_router.get("/mail", response_model=InboundMailListResponseSchema)
async def list_inbound_mail(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    inbound_mail: InboundMailUseCase = Depends(get_inbound_mail_use_case),
) -> InboundMailListResponseSchema:
    return await inbound_mail.list_mails(page=page, page_size=page_size)
