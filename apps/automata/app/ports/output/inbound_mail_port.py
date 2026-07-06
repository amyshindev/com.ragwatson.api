from __future__ import annotations

from abc import ABC, abstractmethod

from automata.app.dtos.inbound_mail_dto import InboundMailCommand, InboundMailListResult


class InboundMailPort(ABC):
    @abstractmethod
    async def save_mail(self, command: InboundMailCommand) -> int:
        pass

    @abstractmethod
    async def list_mails(self, *, page: int, page_size: int) -> InboundMailListResult:
        pass

    @abstractmethod
    async def exists_by_message_id(self, message_id: str) -> bool:
        pass
