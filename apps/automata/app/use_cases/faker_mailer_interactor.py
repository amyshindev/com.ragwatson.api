from __future__ import annotations

import asyncio
import logging
import re

from automata.adapter.inbound.api.schemas.faker_mailer_schema import (
    FakerEmailRequestSchema,
    FakerEmailResponseSchema,
)
from automata.app.ports.input.faker_mailer_use_case import FakerMailerUseCase
from automata.app.ports.output.faker_mailer_port import FakerMailerPort, GmailSendCommand
from core.lol.t1_mid_faker_orchestrator import T1MidFakerOrchestrator

logger = logging.getLogger(__name__)

EMAIL_WRITER_SYSTEM = """You are a professional email writer.
Use Korean unless the user prompt requests another language.
Output format (strict):
Subject: <single line title>
Body:
<email body, multiple paragraphs allowed>
"""

_BODY_PREVIEW_LEN = 200


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
    ) -> None:
        self._repository = repository
        self._faker = faker

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

        send_result = await self._repository.send_gmail(
            GmailSendCommand(to=str(schema.to), subject=subject, body=body),
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
