from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SpamGuardVerdict:
    label: str
    score: float
    is_blocked: bool
    reasons: tuple[str, ...]


class SpamGuardPort(ABC):
    @abstractmethod
    async def classify(self, *, sender: str | None, subject: str, body: str) -> SpamGuardVerdict:
        pass
