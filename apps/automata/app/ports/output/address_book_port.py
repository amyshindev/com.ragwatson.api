from __future__ import annotations

from abc import ABC, abstractmethod

from automata.app.dtos.address_book_dto import ContactCommand, ContactListResult


class AddressBookPort(ABC):
    @abstractmethod
    async def upsert_contacts(self, commands: list[ContactCommand]) -> int:
        pass

    @abstractmethod
    async def list_contacts(self, *, page: int, page_size: int) -> ContactListResult:
        pass
