from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Ticket:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Ticket은 필수 값입니다.")

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> Ticket:
        if raw is None or raw.strip() == "":
            raise ValueError("Ticket은 필수 값입니다.")
        return cls(value=raw.strip())

    def __str__(self) -> str:
        return self.value
