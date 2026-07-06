from __future__ import annotations

import logging

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from automata.adapter.outbound.orm.automata_contact_orm import AutomataContactOrm
from automata.app.dtos.address_book_dto import ContactCommand, ContactListResult, ContactRow
from automata.app.ports.output.address_book_port import AddressBookPort

log = logging.getLogger(__name__)

_BATCH_SIZE = 500


class AddressBookPgRepository(AddressBookPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_contacts(self, commands: list[ContactCommand]) -> int:
        if not commands:
            return 0

        for start in range(0, len(commands), _BATCH_SIZE):
            chunk = commands[start : start + _BATCH_SIZE]
            values = [{"nickname": cmd.nickname, "email": cmd.email} for cmd in chunk]
            insert_stmt = pg_insert(AutomataContactOrm).values(values)
            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[AutomataContactOrm.email],
                set_={"nickname": insert_stmt.excluded.nickname},
            )
            await self._session.execute(upsert_stmt)

        count = len(commands)
        log.info("[AddressBookPgRepository] upsert_contacts rows=%s", count)
        return count

    async def list_contacts(self, *, page: int, page_size: int) -> ContactListResult:
        total_result = await self._session.execute(
            select(func.count()).select_from(AutomataContactOrm)
        )
        total = int(total_result.scalar_one() or 0)
        offset = (page - 1) * page_size
        rows = await self._session.execute(
            select(AutomataContactOrm)
            .order_by(AutomataContactOrm.nickname.asc(), AutomataContactOrm.id.asc())
            .offset(offset)
            .limit(page_size)
        )
        items = [
            ContactRow(id=row.id, nickname=row.nickname, email=row.email)
            for row in rows.scalars().all()
        ]
        return ContactListResult(items=items, total=total, page=page, page_size=page_size)
