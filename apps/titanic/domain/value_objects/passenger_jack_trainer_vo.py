from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GenderType(Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PassengerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class PassengerName:
    full_name: str

    def __post_init__(self) -> None:
        if not self.full_name or len(self.full_name.strip()) == 0:
            raise ValueError("이름은 공백일 수 없습니다.")
        if len(self.full_name) > 200:
            raise ValueError("이름은 200자를 초과할 수 없습니다.")

    @property
    def normalized(self) -> str:
        return self.full_name.strip()


@dataclass(frozen=True)
class Gender:
    value: GenderType

    @classmethod
    def from_raw(cls, raw: str | None) -> Gender:
        if raw is None:
            return cls(GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        if normalized in {"male", "m"}:
            return cls(GenderType.MALE)
        if normalized in {"female", "f"}:
            return cls(GenderType.FEMALE)
        return cls(GenderType.UNKNOWN)

    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE


@dataclass(frozen=True)
class Age:
    value: float | None

    def __post_init__(self) -> None:
        if self.value is None:
            return
        if self.value < 0:
            raise ValueError("나이는 음수일 수 없습니다.")
        if self.value > 120:
            raise ValueError("나이는 120을 초과할 수 없습니다.")

    @classmethod
    def from_raw(cls, raw: str | None) -> Age:
        if raw is None:
            return cls(value=None)
        text = raw.strip()
        if not text:
            return cls(value=None)
        try:
            return cls(value=float(text))
        except ValueError as exc:
            raise ValueError("나이 파싱 실패") from exc

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        if self.value is None:
            return False
        return self.value < 18.0


@dataclass(frozen=True)
class FamilyRelation:
    sib_sp: int
    parch: int

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise ValueError("sib_sp는 음수일 수 없습니다.")
        if self.parch < 0:
            raise ValueError("parch는 음수일 수 없습니다.")

    @classmethod
    def from_raw(cls, sib_sp: str | None, parch: str | None) -> FamilyRelation:
        return cls(
            sib_sp=cls._parse_count(sib_sp),
            parch=cls._parse_count(parch),
        )

    @staticmethod
    def _parse_count(raw: str | None) -> int:
        if raw is None:
            return 0
        text = raw.strip()
        if not text:
            return 0
        return int(float(text))

    @property
    def total_family_size(self) -> int:
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.sib_sp == 0 and self.parch == 0


@dataclass(frozen=True)
class SurvivalStatus:
    survived: bool | None

    @classmethod
    def from_raw(cls, raw: str | None) -> SurvivalStatus:
        if raw is None:
            return cls(survived=None)
        text = raw.strip()
        if not text:
            return cls(survived=None)
        if text == "1":
            return cls(survived=True)
        if text == "0":
            return cls(survived=False)
        raise ValueError("생존 여부 파싱 실패")

    @property
    def is_unknown(self) -> bool:
        return self.survived is None


FamilySize = FamilyRelation
