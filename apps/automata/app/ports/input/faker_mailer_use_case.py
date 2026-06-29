from __future__ import annotations

from abc import ABC, abstractmethod

from automata.adapter.inbound.api.schemas.faker_mailer_schema import (
    FakerEmailRequestSchema,
    FakerEmailResponseSchema,
)


class FakerMailerUseCase(ABC):
    @abstractmethod
    async def send_email(self, schema: FakerEmailRequestSchema) -> FakerEmailResponseSchema:
        pass
