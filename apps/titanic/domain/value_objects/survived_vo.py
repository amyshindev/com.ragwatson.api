from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SurvivedType(int, Enum):
    NO = 0
    YES = 1


@dataclass(frozen=True)
class Survived:
    value: SurvivedType | None

    @classmethod
    def from_raw(cls, raw: str | None) -> Survived:
        if raw is None or raw.strip() == "":
            return cls(value=None)
        text = raw.strip()
        try:
            survived_type = SurvivedType(int(text))
        except (ValueError, KeyError):
            raise ValueError(f"Survived 유효하지 않은 값: '{raw}'") from None
        return cls(value=survived_type)

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def survived(self) -> bool | None:
        if self.value is None:
            return None
        return self.value == SurvivedType.YES

    @property
    def did_survive(self) -> bool:
        if self.value is None:
            raise ValueError("생존 여부가 알려지지 않았습니다.")
        return self.value == SurvivedType.YES

    def __str__(self) -> str:
        if self.value is None:
            return ""
        return str(self.value.value)
