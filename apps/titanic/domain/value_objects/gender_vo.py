from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Gender:
    value: GenderType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> Gender:
        if raw is None or raw.strip() == "":
            return cls(value=GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        if normalized in {"male", "m"}:
            return cls(value=GenderType.MALE)
        if normalized in {"female", "f"}:
            return cls(value=GenderType.FEMALE)
        if normalized == GenderType.UNKNOWN.value:
            return cls(value=GenderType.UNKNOWN)
        return cls(value=GenderType.UNKNOWN)

    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    def is_male(self) -> bool:
        return self.value == GenderType.MALE

    def __str__(self) -> str:
        return self.value.value
