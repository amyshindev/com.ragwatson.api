from __future__ import annotations

from abc import ABC, abstractmethod

from automata.adapter.inbound.api.schemas.address_book_schema import (
    ContactListResponseSchema,
    ContactUploadRowSchema,
)


class AddressBookUseCase(ABC):
    @abstractmethod
    async def upload_contacts(self, rows: list[ContactUploadRowSchema]) -> dict[str, int]:
        pass

    @abstractmethod
    async def list_contacts(self, *, page: int, page_size: int) -> ContactListResponseSchema:
        pass
