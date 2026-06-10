from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_isidor_couple_orm import PassengerIsidorCoupleOrm


class PassengerIsidorCoupleMapper:
    """PassengerIsidorCouple entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: PassengerIsidorCoupleOrm):
        raise NotImplementedError("PassengerIsidorCoupleOrm is abstract")

    @staticmethod
    def to_orm(entity) -> PassengerIsidorCoupleOrm:
        raise NotImplementedError("PassengerIsidorCoupleOrm is abstract")
