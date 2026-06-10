from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PassengerJackTrainerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import (
    Gender,
    Passenger,
    SurvivalStatus,
)
from titanic.domain.value_objects.passenger_jack_trainer_vo import Age, FamilySize, PassengerName


class PassengerJackTrainerMapper:

    @staticmethod
    def to_entity(
        orm: PassengerJackTrainerOrm,
        *,
        include_bookings: bool = False,
    ) -> Passenger:
        from titanic.adapter.outbound.mappers.passenger_rose_model_mapper import (
            PassengerRoseModelMapper,
        )

        bookings = (
            [PassengerRoseModelMapper.to_entity(booking) for booking in orm.bookings]
            if include_bookings
            else None
        )

        return Passenger(
            passenger_id=orm.passenger_id,
            name=PassengerName(orm.name),
            gender=PassengerJackTrainerMapper._parse_gender(orm.gender),
            age=PassengerJackTrainerMapper._parse_age(orm.age),
            family=FamilySize(
                sib_sp=PassengerJackTrainerMapper._parse_int(orm.sib_sp),
                parch=PassengerJackTrainerMapper._parse_int(orm.parch),
            ),
            survival_status=PassengerJackTrainerMapper._parse_survival(orm.survived),
            bookings=bookings,
        )

    @staticmethod
    def to_orm(entity: Passenger) -> PassengerJackTrainerOrm:
        return PassengerJackTrainerOrm(
            passenger_id=entity.passenger_id,
            name=entity.name.value,
            gender=entity.gender.value,
            age="" if entity.age is None else str(entity.age.value),
            sib_sp=str(entity.family.sib_sp),
            parch=str(entity.family.parch),
            survived=str(entity.survival_status.value),
        )

    @staticmethod
    def _parse_gender(value: str) -> Gender:
        normalized = value.strip().lower()
        if normalized in {"male", "m"}:
            return Gender.MALE
        if normalized in {"female", "f"}:
            return Gender.FEMALE
        return Gender.UNKNOWN

    @staticmethod
    def _parse_survival(value: str) -> SurvivalStatus:
        normalized = value.strip().lower()
        if normalized in {"1", "true", "survived", "yes"}:
            return SurvivalStatus.SURVIVED
        return SurvivalStatus.PERISHED

    @staticmethod
    def _parse_age(value: str) -> Age | None:
        text = value.strip()
        if not text:
            return None
        return Age(float(text))

    @staticmethod
    def _parse_int(value: str) -> int:
        text = value.strip()
        if not text:
            return 0
        return int(float(text))
