from __future__ import annotations

import re

from automata.adapter.inbound.api.schemas.address_book_schema import (
    ContactListResponseSchema,
    ContactUploadRowSchema,
)
from automata.app.dtos.address_book_dto import ContactCommand
from automata.app.ports.input.address_book_use_case import AddressBookUseCase
from automata.app.ports.output.address_book_port import AddressBookPort

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalize_email(raw: str | None) -> str | None:
    text = (raw or "").strip()
    if not text or not _EMAIL_RE.match(text):
        return None
    return text.lower()


def _normalize_nickname(raw: str | None, *, fallback_email: str) -> str:
    text = (raw or "").strip()
    return text or fallback_email.split("@", 1)[0]


class AddressBookInteractor(AddressBookUseCase):
    def __init__(self, repository: AddressBookPort) -> None:
        self._repository = repository

    async def upload_contacts(self, rows: list[ContactUploadRowSchema]) -> dict[str, int]:
        commands: list[ContactCommand] = []
        for row in rows:
            email = _normalize_email(row.email)
            if email is None:
                continue
            commands.append(
                ContactCommand(
                    nickname=_normalize_nickname(row.nickname, fallback_email=email),
                    email=email,
                )
            )

        if not commands:
            return {"saved": 0}

        saved = await self._repository.upsert_contacts(commands)
        return {"saved": saved}

    async def list_contacts(self, *, page: int, page_size: int) -> ContactListResponseSchema:
        result = await self._repository.list_contacts(page=page, page_size=page_size)
        return ContactListResponseSchema(
            items=[
                {"id": item.id, "nickname": item.nickname, "email": item.email}
                for item in result.items
            ],
            total=result.total,
            page=result.page,
            page_size=result.page_size,
        )
