from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GmailSendCommand:
    to: str
    subject: str
    body: str
    body_html: str | None = None


@dataclass(frozen=True)
class GmailSendResult:
    ok: bool
    status: str
    detail: dict[str, Any] | None = None


class FakerMailerPort(ABC):
    @abstractmethod
    async def send_gmail(self, command: GmailSendCommand) -> GmailSendResult:
        pass
