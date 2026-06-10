from __future__ import annotations

from titanic.adapter.outbound.orm.crew_hartley_violin_orm import CrewHartleyViolinOrm


class CrewHartleyViolinMapper:
    """CrewHartleyViolin entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: CrewHartleyViolinOrm):
        raise NotImplementedError("CrewHartleyViolinOrm is abstract")

    @staticmethod
    def to_orm(entity) -> CrewHartleyViolinOrm:
        raise NotImplementedError("CrewHartleyViolinOrm is abstract")
