from __future__ import annotations

from titanic.adapter.outbound.orm.titanic_booking_orm import TitanicBookingOrm
from titanic.domain.entities.passenger_rose_model_entity import Booking


class TitanicBookingMapper:

    @staticmethod
    def to_entity(orm: TitanicBookingOrm) -> Booking:
        return Booking(
            passenger_id=orm.passenger_id,
            pclass=orm.pclass,
            ticket=orm.ticket,
            fare=orm.fare,
            cabin=orm.cabin,
            embarked=orm.embarked,
        )

    @staticmethod
    def to_orm(entity: Booking) -> TitanicBookingOrm:
        return TitanicBookingOrm(
            passenger_id=entity.passenger_id,
            pclass=entity.pclass,
            ticket=entity.ticket,
            fare=entity.fare,
            cabin=entity.cabin,
            embarked=entity.embarked,
        )
