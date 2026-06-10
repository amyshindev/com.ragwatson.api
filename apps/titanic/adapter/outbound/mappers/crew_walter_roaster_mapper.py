from __future__ import annotations

from titanic.adapter.outbound.orm.crew_walter_roaster_orm import CrewWalterRoasterOrm


class CrewWalterRoasterMapper:
    """CrewWalterRoaster entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: CrewWalterRoasterOrm):
        raise NotImplementedError("CrewWalterRoasterOrm is abstract")

    @staticmethod
    def to_orm(entity) -> CrewWalterRoasterOrm:
        raise NotImplementedError("CrewWalterRoasterOrm is abstract")
