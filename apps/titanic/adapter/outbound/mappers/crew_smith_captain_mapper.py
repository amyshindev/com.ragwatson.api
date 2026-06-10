from __future__ import annotations

from titanic.adapter.outbound.orm.crew_smith_captain_orm import CrewSmithCaptainOrm


class CrewSmithCaptainMapper:
    """CrewSmithCaptain entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: CrewSmithCaptainOrm):
        raise NotImplementedError("CrewSmithCaptainOrm is abstract")

    @staticmethod
    def to_orm(entity) -> CrewSmithCaptainOrm:
        raise NotImplementedError("CrewSmithCaptainOrm is abstract")
