from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Parch:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Parch는 음수일 수 없습니다.")

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> Parch:
        if raw is None or raw.strip() == "":
            return cls(value=0)
        try:
            return cls(value=int(float(raw.strip())))
        except ValueError:
            raise ValueError(f"Parch 유효하지 않은 값: '{raw}'") from None

    @property
    def has_parent_or_child(self) -> bool:
        return self.value > 0

    def __str__(self) -> str:
        return str(self.value)
