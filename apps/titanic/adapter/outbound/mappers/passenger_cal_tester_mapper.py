from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_cal_tester_orm import PassengerCalTesterOrm


class PassengerCalTesterMapper:
    """PassengerCalTester entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: PassengerCalTesterOrm):
        raise NotImplementedError("PassengerCalTesterOrm is abstract")

    @staticmethod
    def to_orm(entity) -> PassengerCalTesterOrm:
        raise NotImplementedError("PassengerCalTesterOrm is abstract")
