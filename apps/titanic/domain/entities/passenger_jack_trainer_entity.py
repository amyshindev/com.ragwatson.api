from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.gender_vo import Gender
from titanic.domain.value_objects.name_vo import Name
from titanic.domain.value_objects.parch_vo import Parch
from titanic.domain.value_objects.sib_sp_vo import SibSp
from titanic.domain.value_objects.survived_vo import Survived


@dataclass
class PassengerEntity:
    id: int
    passenger_id: str | None
    name: Name | None
    gender: Gender
    age: Age
    sib_sp: SibSp
    parch: Parch
    survival_status: Survived

    def is_high_risk(self) -> bool:
        if self.gender.is_female():
            return False
        if self.age.is_minor:
            return False
        return not self.has_family()

    def has_family(self) -> bool:
        return self.sib_sp.has_sibling_or_spouse or self.parch.has_parent_or_child

    @property
    def family_size(self) -> int:
        return self.sib_sp.value + self.parch.value + 1

    def record_survival(self, survived: bool) -> None:
        from titanic.domain.value_objects.survived_vo import SurvivedType

        self.survival_status = Survived(
            value=SurvivedType.YES if survived else SurvivedType.NO,
        )

    @classmethod
    def from_orm(cls, orm: Any) -> PassengerEntity:
        name = Name(str(orm.name)) if getattr(orm, "name", None) is not None else None
        return cls(
            id=int(getattr(orm, "id", 0) or 0),
            passenger_id=(
                str(orm.passenger_id) if getattr(orm, "passenger_id", None) is not None else None
            ),
            name=name,
            gender=Gender.from_raw(getattr(orm, "gender", None)),
            age=Age.from_raw(getattr(orm, "age", None)),
            sib_sp=SibSp.from_raw(getattr(orm, "sib_sp", None)),
            parch=Parch.from_raw(getattr(orm, "parch", None)),
            survival_status=Survived.from_raw(getattr(orm, "survived", None)),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PassengerEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


Passenger = PassengerEntity
