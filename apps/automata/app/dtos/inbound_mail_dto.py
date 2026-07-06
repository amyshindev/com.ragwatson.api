from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InboundMailCommand:
    message_id: str
    from_email: str
    from_name: str | None
    subject: str
    body: str


@dataclass(frozen=True)
class InboundMailRow:
    id: int
    message_id: str
    from_email: str
    from_name: str | None
    subject: str
    body: str
    received_at: str


@dataclass(frozen=True)
class InboundMailListResult:
    items: list[InboundMailRow]
    total: int
    page: int
    page_size: int
