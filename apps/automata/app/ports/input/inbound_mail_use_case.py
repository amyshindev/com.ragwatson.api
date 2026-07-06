from __future__ import annotations

from abc import ABC, abstractmethod

from automata.adapter.inbound.api.schemas.inbound_mailer_schema import (
    InboundMailListResponseSchema,
    InboundMailReceiveSchema,
    InboundMailReceiveResponseSchema,
)


class InboundMailUseCase(ABC):
    @abstractmethod
    async def receive_mail(
        self,
        schema: InboundMailReceiveSchema,
    ) -> InboundMailReceiveResponseSchema:
        pass

    @abstractmethod
    async def list_mails(
        self,
        *,
        page: int,
        page_size: int,
    ) -> InboundMailListResponseSchema:
        pass
