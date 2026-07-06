from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmailSignal:
    sender: str | None
    subject: str
    body: str

    @property
    def combined_text(self) -> str:
        return f"{self.subject}\n{self.body}".lower()
