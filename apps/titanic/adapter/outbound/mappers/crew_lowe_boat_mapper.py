from __future__ import annotations

from titanic.adapter.outbound.orm.crew_lowe_boat_orm import CrewLoweBoatOrm


class CrewLoweBoatMapper:
    """CrewLoweBoat entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: CrewLoweBoatOrm):
        raise NotImplementedError("CrewLoweBoatOrm is abstract")

    @staticmethod
    def to_orm(entity) -> CrewLoweBoatOrm:
        raise NotImplementedError("CrewLoweBoatOrm is abstract")
