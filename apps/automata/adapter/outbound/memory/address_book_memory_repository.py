from __future__ import annotations

import logging
from threading import Lock

from automata.app.dtos.address_book_dto import ContactCommand, ContactListResult, ContactRow
from automata.app.ports.output.address_book_port import AddressBookPort

log = logging.getLogger(__name__)


def _contact_id(email: str) -> int:
    return abs(hash(email)) % 1_000_000_000


class AddressBookMemoryRepository(AddressBookPort):
    """In-memory 주소록 — Neo4j/PostgreSQL 없이 동작."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._by_email: dict[str, ContactRow] = {}

    async def upsert_contacts(self, commands: list[ContactCommand]) -> int:
        with self._lock:
            for cmd in commands:
                self._by_email[cmd.email] = ContactRow(
                    id=_contact_id(cmd.email),
                    nickname=cmd.nickname,
                    email=cmd.email,
                )
        count = len(commands)
        log.info("[AddressBookMemoryRepository] upsert_contacts rows=%s", count)
        return count

    async def list_contacts(self, *, page: int, page_size: int) -> ContactListResult:
        with self._lock:
            items = sorted(
                self._by_email.values(),
                key=lambda row: (row.nickname.lower(), row.email),
            )
        total = len(items)
        offset = (page - 1) * page_size
        page_items = items[offset : offset + page_size]
        return ContactListResult(
            items=page_items,
            total=total,
            page=page,
            page_size=page_size,
        )
