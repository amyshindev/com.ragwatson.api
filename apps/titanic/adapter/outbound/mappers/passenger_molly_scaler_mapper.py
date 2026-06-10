from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_molly_scaler_orm import PassengerMollyScalerOrm


class PassengerMollyScalerMapper:
    """PassengerMollyScaler entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: PassengerMollyScalerOrm):
        raise NotImplementedError("PassengerMollyScalerOrm is abstract")

    @staticmethod
    def to_orm(entity) -> PassengerMollyScalerOrm:
        raise NotImplementedError("PassengerMollyScalerOrm is abstract")
