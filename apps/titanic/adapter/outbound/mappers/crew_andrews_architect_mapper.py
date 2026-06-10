from __future__ import annotations

from titanic.adapter.outbound.orm.crew_andrews_architect_orm import CrewAndrewsArchitectOrm


class CrewAndrewsArchitectMapper:
    """CrewAndrewsArchitect entity ↔ ORM mapper (abstract ORM — 구현 대기)."""

    @staticmethod
    def to_entity(orm: CrewAndrewsArchitectOrm):
        raise NotImplementedError("CrewAndrewsArchitectOrm is abstract")

    @staticmethod
    def to_orm(entity) -> CrewAndrewsArchitectOrm:
        raise NotImplementedError("CrewAndrewsArchitectOrm is abstract")
