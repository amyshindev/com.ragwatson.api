from __future__ import annotations

import hashlib
import logging

from automata.adapter.inbound.api.schemas.inbound_mailer_schema import (
    InboundMailListResponseSchema,
    InboundMailReceiveResponseSchema,
    InboundMailReceiveSchema,
)
from automata.app.dtos.inbound_mail_dto import InboundMailCommand
from automata.app.ports.input.inbound_mail_use_case import InboundMailUseCase
from automata.app.ports.output.inbound_mail_port import InboundMailPort

logger = logging.getLogger(__name__)


def _fallback_message_id(schema: InboundMailReceiveSchema) -> str:
    digest = hashlib.sha256(
        f"{schema.from_email}|{schema.subject}|{schema.body[:200]}".encode(),
    ).hexdigest()[:16]
    return f"synthetic-{digest}"


class InboundMailerInteractor(InboundMailUseCase):
    def __init__(self, repository: InboundMailPort) -> None:
        self._repository = repository

    async def receive_mail(
        self,
        schema: InboundMailReceiveSchema,
    ) -> InboundMailReceiveResponseSchema:
        message_id = (schema.message_id or "").strip() or _fallback_message_id(schema)
        if await self._repository.exists_by_message_id(message_id):
            logger.info("[InboundMailerInteractor] duplicate message_id=%s", message_id)
            return InboundMailReceiveResponseSchema(ok=True, id=0, duplicate=True)

        row_id = await self._repository.save_mail(
            InboundMailCommand(
                message_id=message_id,
                from_email=schema.from_email,
                from_name=schema.from_name,
                subject=schema.subject.strip(),
                body=schema.body.strip(),
            ),
        )
        return InboundMailReceiveResponseSchema(ok=True, id=row_id, duplicate=False)

    async def list_mails(
        self,
        *,
        page: int,
        page_size: int,
    ) -> InboundMailListResponseSchema:
        result = await self._repository.list_mails(page=page, page_size=page_size)
        return InboundMailListResponseSchema(
            items=[
                {
                    "id": item.id,
                    "message_id": item.message_id,
                    "from_email": item.from_email,
                    "from_name": item.from_name,
                    "subject": item.subject,
                    "body": item.body,
                    "received_at": item.received_at,
                }
                for item in result.items
            ],
            total=result.total,
            page=result.page,
            page_size=result.page_size,
        )
