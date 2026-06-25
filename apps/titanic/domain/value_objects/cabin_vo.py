from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cabin:
    value: str | None

    @classmethod
    def from_raw(cls, raw: str | None) -> Cabin:
        if raw is None or raw.strip() == "":
            return cls(value=None)
        return cls(value=raw.strip())

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def deck(self) -> str | None:
        if self.value is None:
            return None
        return self.value[0].upper()

    def __str__(self) -> str:
        return self.value or ""
