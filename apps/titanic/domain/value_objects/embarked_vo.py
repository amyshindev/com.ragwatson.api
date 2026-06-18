from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EmbarkedType(str, Enum):
    CHERBOURG = "C"
    QUEENSTOWN = "Q"
    SOUTHAMPTON = "S"


@dataclass(frozen=True)
class Embarked:
    value: EmbarkedType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> Embarked:
        if raw is None or raw.strip() == "":
            raise ValueError("Embarked는 필수 값입니다.")
        code = raw.strip().upper()
        try:
            return cls(value=EmbarkedType(code))
        except ValueError:
            raise ValueError(f"Embarked 유효하지 않은 값: '{raw}'") from None

    @property
    def is_cherbourg(self) -> bool:
        return self.value == EmbarkedType.CHERBOURG

    def __str__(self) -> str:
        return self.value.value
