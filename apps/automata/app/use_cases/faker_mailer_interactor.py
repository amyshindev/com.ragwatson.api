from __future__ import annotations

import asyncio
import logging
import re

from automata.adapter.inbound.api.schemas.faker_mailer_schema import (
    FakerEmailRequestSchema,
    FakerEmailResponseSchema,
)
from automata.app.email_body_format import email_body_to_html, format_email_body
from automata.app.ports.input.faker_mailer_use_case import FakerMailerUseCase
from automata.app.ports.output.faker_mailer_port import FakerMailerPort, GmailSendCommand
from automata.app.ports.output.spam_guard_port import SpamGuardPort
from core.lol.t1_mid_faker_orchestrator import T1MidFakerOrchestrator

logger = logging.getLogger(__name__)

EMAIL_WRITER_SYSTEM = """당신은 한국어 비즈니스 이메일 전문 작가입니다.

규칙:
- 반드시 한국어 존댓말(~입니다, ~합니다)로 작성합니다.
- 아래 출력 형식만 사용하고, 설명·코드블록·따옴표는 붙이지 않습니다.
- Body는 인사, 본문 단락, 맺음말 사이에 빈 줄을 넣어 단락을 나눕니다.
- 본문은 2~3개 단락, 각 단락은 1~3문장으로 짧게 씁니다.
- 한 줄에 문장을 너무 많이 이어 붙이지 않습니다.

출력 형식:
Subject: (제목 한 줄)

Body:
(인사말 한 문장)

(본문 첫 단락)

(본문 둘째 단락 — 필요 시)

(맺음말 한 문장)
"""

_BODY_PREVIEW_LEN = 200


class SpamEmailBlockedError(Exception):
    def __init__(self, label: str, score: float, detail: str) -> None:
        self.label = label
        self.score = score
        self.detail = detail
        super().__init__(detail)


def parse_email_draft(raw: str, *, fallback_subject: str | None = None) -> tuple[str, str]:
    text = raw.strip()
    subject_match = re.search(r"^Subject:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    body_match = re.search(r"^Body:\s*\n?(.*)$", text, re.MULTILINE | re.IGNORECASE | re.DOTALL)

    if subject_match and body_match:
        subject = subject_match.group(1).strip()
        body = body_match.group(1).strip()
        return subject, body

    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) >= 2:
        return lines[0].strip(), "\n".join(lines[1:]).strip()

    subject = fallback_subject or "[Automata] 알림"
    return subject, text


class FakerMailerInteractor(FakerMailerUseCase):
    def __init__(
        self,
        repository: FakerMailerPort,
        faker: T1MidFakerOrchestrator,
        spam_guard: SpamGuardPort,
    ) -> None:
        self._repository = repository
        self._faker = faker
        self._spam_guard = spam_guard

    async def send_email(self, schema: FakerEmailRequestSchema) -> FakerEmailResponseSchema:
        logger.info("[FakerMailerInteractor] send_email to=%s", schema.to)

        try:
            raw = await asyncio.to_thread(
                self._faker.chat,
                schema.prompt,
                system=EMAIL_WRITER_SYSTEM,
            )
        except RuntimeError as exc:
            logger.warning("[FakerMailerInteractor] ExaONE not ready: %s", exc)
            raise

        subject, body = parse_email_draft(raw, fallback_subject=schema.subject)
        if schema.subject:
            subject = schema.subject
        body = format_email_body(body)
        body_html = email_body_to_html(body)

        spam = await self._spam_guard.classify(
            sender=None,
            subject=subject,
            body=body,
        )
        if spam.is_blocked:
            reason_text = "; ".join(spam.reasons) if spam.reasons else spam.label
            raise SpamEmailBlockedError(spam.label, spam.score, reason_text)

        send_result = await self._repository.send_gmail(
            GmailSendCommand(
                to=str(schema.to),
                subject=subject,
                body=body,
                body_html=body_html,
            ),
        )

        preview = body[:_BODY_PREVIEW_LEN]
        if len(body) > _BODY_PREVIEW_LEN:
            preview += "…"

        return FakerEmailResponseSchema(
            ok=send_result.ok,
            to=str(schema.to),
            subject=subject,
            body_preview=preview,
            n8n_status=send_result.status,
        )
