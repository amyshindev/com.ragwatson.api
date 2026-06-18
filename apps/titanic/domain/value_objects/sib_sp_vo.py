from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SibSp:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("SibSp는 음수일 수 없습니다.")

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> SibSp:
        if raw is None or raw.strip() == "":
            return cls(value=0)
        try:
            return cls(value=int(float(raw.strip())))
        except ValueError:
            raise ValueError(f"SibSp 유효하지 않은 값: '{raw}'") from None

    @property
    def has_sibling_or_spouse(self) -> bool:
        return self.value > 0

    def __str__(self) -> str:
        return str(self.value)
