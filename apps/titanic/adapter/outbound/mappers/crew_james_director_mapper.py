from __future__ import annotations

from titanic.adapter.outbound.orm.crew_james_director_orm import CrewJamesDirectorOrm


class CrewJamesDirectorMapper:
    """CrewJamesDirector entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: CrewJamesDirectorOrm):
        raise NotImplementedError("CrewJamesDirectorOrm is abstract")

    @staticmethod
    def to_orm(entity) -> CrewJamesDirectorOrm:
        raise NotImplementedError("CrewJamesDirectorOrm is abstract")
