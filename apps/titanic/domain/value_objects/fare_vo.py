from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Fare:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Fare는 음수일 수 없습니다.")

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> Fare:
        if raw is None or raw.strip() == "":
            raise ValueError("Fare는 필수 값입니다.")
        try:
            return cls(value=float(raw.strip()))
        except ValueError:
            raise ValueError(f"Fare 유효하지 않은 값: '{raw}'") from None

    def __str__(self) -> str:
        return str(self.value)
