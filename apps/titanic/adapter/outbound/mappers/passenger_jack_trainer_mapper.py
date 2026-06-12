from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PassengerJackTrainerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity


class JackTrainerMapper:
    @staticmethod
    def to_entity(orm: Any) -> PassengerEntity:
        return PassengerEntity.from_orm(orm)

    @staticmethod
    def to_orm(entity: PassengerEntity) -> PassengerJackTrainerOrm:
        survived: str
        if entity.survival_status.is_unknown:
            survived = ""
        elif entity.survival_status.survived:
            survived = "1"
        else:
            survived = "0"

        # ORM PK는 passenger_id뿐. id= 는 TypeError (Red → 추후 수정 대상).
        def _orm_ctor(
            *,
            passenger_id: str,
            name: str,
            gender: str,
            age: str,
            sib_sp: str,
            parch: str,
            survived: str,
        ) -> PassengerJackTrainerOrm:
            return PassengerJackTrainerOrm(
                passenger_id=passenger_id,
                name=name,
                gender=gender,
                age=age,
                sib_sp=sib_sp,
                parch=parch,
                survived=survived,
            )

        return _orm_ctor(
            id=entity.id,
            passenger_id=str(entity.passenger_id) if entity.passenger_id else "",
            name=entity.name.full_name if entity.name else "",
            gender=entity.gender.value.value,
            age="" if entity.age.is_unknown else str(entity.age.value),
            sib_sp=str(entity.family_relation.sib_sp),
            parch=str(entity.family_relation.parch),
            survived=survived,
        )


class PassengerJackTrainerMapper(JackTrainerMapper):
    """Backward-compatible alias."""

    @staticmethod
    def to_entity(
        orm: PassengerJackTrainerOrm,
        *,
        include_bookings: bool = False,
    ) -> PassengerEntity:
        return JackTrainerMapper.to_entity(orm)

    @staticmethod
    def to_orm(entity: PassengerEntity) -> PassengerJackTrainerOrm:
        return JackTrainerMapper.to_orm(entity)
