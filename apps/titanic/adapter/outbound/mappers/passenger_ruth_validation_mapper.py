from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_ruth_validation_orm import PassengerRuthValidationOrm


class PassengerRuthValidationMapper:
    """PassengerRuthValidation entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: PassengerRuthValidationOrm):
        raise NotImplementedError("PassengerRuthValidationOrm is abstract")

    @staticmethod
    def to_orm(entity) -> PassengerRuthValidationOrm:
        raise NotImplementedError("PassengerRuthValidationOrm is abstract")
