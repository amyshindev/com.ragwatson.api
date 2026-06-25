from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_rose_model_orm import PassengerRoseModelOrm
from titanic.domain.entities.passenger_rose_model_entity import Booking


class PassengerRoseModelMapper:
    @staticmethod
    def to_entity(orm: PassengerRoseModelOrm) -> Booking:
        return Booking(
            passenger_id=orm.passenger_id,
            pclass=orm.pclass,
            ticket=orm.ticket,
            fare=orm.fare,
            cabin=orm.cabin,
            embarked=orm.embarked,
        )

    @staticmethod
    def to_orm(entity: Booking) -> PassengerRoseModelOrm:
        return PassengerRoseModelOrm(
            passenger_id=entity.passenger_id,
            pclass=entity.pclass,
            ticket=entity.ticket,
            fare=entity.fare,
            cabin=entity.cabin,
            embarked=entity.embarked,
        )
