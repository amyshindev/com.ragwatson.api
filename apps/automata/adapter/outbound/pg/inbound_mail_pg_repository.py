from __future__ import annotations

import asyncio
import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from automata.adapter.outbound.ollama.inbound_mail_embedding_adapter import (
    build_mail_embedding_text,
)
from automata.adapter.outbound.orm.automata_inbound_mail_orm import AutomataInboundMailOrm
from automata.app.dtos.inbound_mail_dto import InboundMailCommand, InboundMailListResult, InboundMailRow
from automata.app.ports.output.inbound_mail_port import InboundMailPort
from automata.app.ports.output.mail_embedding_port import MailEmbeddingPort

log = logging.getLogger(__name__)


class InboundMailPgRepository(InboundMailPort):
    def __init__(self, session: AsyncSession, embedder: MailEmbeddingPort) -> None:
        self._session = session
        self._embedder = embedder

    async def save_mail(self, command: InboundMailCommand) -> int:
        embedding_text = build_mail_embedding_text(
            from_email=command.from_email,
            from_name=command.from_name,
            subject=command.subject,
            body=command.body,
        )
        embedding = await asyncio.to_thread(self._embedder.embed_mail_text, embedding_text)

        row = AutomataInboundMailOrm(
            message_id=command.message_id,
            from_email=command.from_email,
            from_name=command.from_name,
            subject=command.subject,
            body=command.body,
            embedding=embedding,
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)

        log.info(
            "[InboundMailPgRepository] saved id=%s message_id=%s embedding_dim=%s",
            row.id,
            row.message_id,
            len(embedding),
        )
        return int(row.id)

    async def list_mails(self, *, page: int, page_size: int) -> InboundMailListResult:
        total_result = await self._session.execute(
            select(func.count()).select_from(AutomataInboundMailOrm)
        )
        total = int(total_result.scalar_one() or 0)
        offset = (page - 1) * page_size
        rows = await self._session.execute(
            select(AutomataInboundMailOrm)
            .order_by(AutomataInboundMailOrm.received_at.desc(), AutomataInboundMailOrm.id.desc())
            .offset(offset)
            .limit(page_size)
        )
        items = [
            InboundMailRow(
                id=row.id,
                message_id=row.message_id,
                from_email=row.from_email,
                from_name=row.from_name,
                subject=row.subject,
                body=row.body,
                received_at=row.received_at.isoformat(),
            )
            for row in rows.scalars().all()
        ]
        return InboundMailListResult(items=items, total=total, page=page, page_size=page_size)

    async def exists_by_message_id(self, message_id: str) -> bool:
        result = await self._session.execute(
            select(AutomataInboundMailOrm.id)
            .where(AutomataInboundMailOrm.message_id == message_id)
            .limit(1)
        )
        return result.scalar_one_or_none() is not None
