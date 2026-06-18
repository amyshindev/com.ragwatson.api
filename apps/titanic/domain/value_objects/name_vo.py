from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Name은 필수 값입니다.")
        if len(self.value) > 200:
            raise ValueError("Name은 200자를 초과할 수 없습니다.")

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> Name:
        if raw is None or raw.strip() == "":
            raise ValueError("Name은 필수 값입니다.")
        return cls(value=raw.strip())

    @property
    def normalized(self) -> str:
        return self.value.strip()

    def __str__(self) -> str:
        return self.value
