from __future__ import annotations

import asyncio
import logging

from core.graph.neo4j_driver import get_neo4j_driver
from automata.adapter.outbound.memory.address_book_memory_repository import (
    AddressBookMemoryRepository,
)
from automata.app.dtos.address_book_dto import ContactCommand, ContactListResult, ContactRow
from automata.app.ports.output.address_book_port import AddressBookPort

log = logging.getLogger(__name__)

_LABEL = "AutomataContact"


class AddressBookNeo4jRepository(AddressBookPort):
    """메모리를 읽기·쓰기 기준으로 두고, Neo4j에는 best-effort로 동기화한다."""

    def __init__(self, fallback: AddressBookPort | None = None) -> None:
        self._fallback = fallback or AddressBookMemoryRepository()

    async def upsert_contacts(self, commands: list[ContactCommand]) -> int:
        saved = await self._fallback.upsert_contacts(commands)
        driver = get_neo4j_driver()
        if driver is None or not commands:
            return saved
        try:
            await asyncio.to_thread(self._upsert_sync, driver, commands)
        except Exception:
            log.exception("[AddressBookNeo4jRepository] upsert failed (memory kept)")
        return saved

    async def list_contacts(self, *, page: int, page_size: int) -> ContactListResult:
        return await self._fallback.list_contacts(page=page, page_size=page_size)

    def _upsert_sync(self, driver, commands: list[ContactCommand]) -> None:
        with driver.session() as session:
            for cmd in commands:
                session.run(
                    f"""
                    MERGE (c:{_LABEL} {{email: $email}})
                    SET c.nickname = $nickname
                    """,
                    email=cmd.email,
                    nickname=cmd.nickname,
                )
        log.info("[AddressBookNeo4jRepository] synced to neo4j rows=%s", len(commands))
