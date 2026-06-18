from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Age:
    value: float | None

    def __post_init__(self) -> None:
        if self.value is None:
            return
        if self.value < 0:
            raise ValueError("Age는 음수일 수 없습니다.")
        if self.value > 120:
            raise ValueError("Age는 120을 초과할 수 없습니다.")

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> Age:
        if raw is None or raw.strip() == "":
            return cls(value=None)
        try:
            return cls(value=float(raw.strip()))
        except ValueError:
            raise ValueError(f"Age 유효하지 않은 값: '{raw}'") from None

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        if self.value is None:
            return False
        return self.value < 18.0

    @property
    def is_infant(self) -> bool:
        if self.value is None:
            return False
        return self.value < 1.0

    def __str__(self) -> str:
        if self.value is None:
            return ""
        return str(self.value)
