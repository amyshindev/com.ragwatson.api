from __future__ import annotations

import logging
from datetime import UTC, datetime
from threading import Lock

from automata.app.dtos.inbound_mail_dto import InboundMailCommand, InboundMailListResult, InboundMailRow
from automata.app.ports.output.inbound_mail_port import InboundMailPort

log = logging.getLogger(__name__)

_MAX_STORED = 500


class InboundMailMemoryRepository(InboundMailPort):
    def __init__(self) -> None:
        self._lock = Lock()
        self._rows: list[InboundMailRow] = []
        self._message_ids: set[str] = set()
        self._next_id = 1

    async def save_mail(self, command: InboundMailCommand) -> int:
        with self._lock:
            row = InboundMailRow(
                id=self._next_id,
                message_id=command.message_id,
                from_email=command.from_email,
                from_name=command.from_name,
                subject=command.subject,
                body=command.body,
                received_at=datetime.now(UTC).isoformat(),
            )
            self._next_id += 1
            self._rows.insert(0, row)
            self._message_ids.add(command.message_id)
            if len(self._rows) > _MAX_STORED:
                removed = self._rows.pop()
                self._message_ids.discard(removed.message_id)
        log.info(
            "[InboundMailMemoryRepository] saved id=%s from=%s subject=%s",
            row.id,
            row.from_email,
            row.subject,
        )
        return row.id

    async def list_mails(self, *, page: int, page_size: int) -> InboundMailListResult:
        with self._lock:
            total = len(self._rows)
            offset = (page - 1) * page_size
            items = list(self._rows[offset : offset + page_size])
        return InboundMailListResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )

    async def exists_by_message_id(self, message_id: str) -> bool:
        with self._lock:
            return message_id in self._message_ids
