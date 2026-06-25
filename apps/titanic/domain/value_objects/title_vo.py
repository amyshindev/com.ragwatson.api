from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import ClassVar

_TITLE_PATTERN = re.compile(r"([A-Za-z]+)\.")


class TitleCategory(str, Enum):
    """Name에서 추출한 호칭 — nominal 인코딩 전 범주"""

    UNKNOWN = "Unknown"
    MR = "Mr"
    MISS = "Miss"
    MRS = "Mrs"
    MASTER = "Master"
    ROYAL = "Royal"
    RARE = "Rare"


@dataclass(frozen=True)
class Title:
    """승객 이름(Name)에서 호칭을 추출하고 nominal 정수로 변환한다."""

    category: TitleCategory

    _RARE_RAW: ClassVar[frozenset[str]] = frozenset(
        {
            "Capt",
            "Col",
            "Don",
            "Dr",
            "Major",
            "Rev",
            "Jonkheer",
            "Dona",
            "Mme",
        }
    )
    _ROYAL_RAW: ClassVar[frozenset[str]] = frozenset({"Countess", "Lady", "Sir"})
    _ALIASES: ClassVar[dict[str, str]] = {"Mlle": "Mr", "Ms": "Miss"}
    _NOMINAL_CODES: ClassVar[dict[TitleCategory, int]] = {
        TitleCategory.UNKNOWN: 0,
        TitleCategory.MR: 1,
        TitleCategory.MISS: 2,
        TitleCategory.MRS: 3,
        TitleCategory.MASTER: 4,
        TitleCategory.ROYAL: 5,
        TitleCategory.RARE: 6,
    }

    @classmethod
    def from_name(cls, name: str | None) -> Title:
        if name is None or not name.strip():
            return cls(category=TitleCategory.UNKNOWN)

        match = _TITLE_PATTERN.search(name.strip())
        if match is None:
            return cls(category=TitleCategory.UNKNOWN)

        return cls.from_raw(match.group(1))

    @classmethod
    def from_raw(cls, raw: str | None) -> Title:
        if raw is None or not str(raw).strip():
            return cls(category=TitleCategory.UNKNOWN)

        token = str(raw).strip()
        if token in cls._RARE_RAW:
            return cls(category=TitleCategory.RARE)
        if token in cls._ROYAL_RAW:
            return cls(category=TitleCategory.ROYAL)

        token = cls._ALIASES.get(token, token)
        try:
            return cls(category=TitleCategory(token))
        except ValueError:
            return cls(category=TitleCategory.UNKNOWN)

    @property
    def nominal_code(self) -> int:
        return self._NOMINAL_CODES[self.category]

    def __str__(self) -> str:
        return self.category.value
