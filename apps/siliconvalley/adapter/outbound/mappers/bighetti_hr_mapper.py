from __future__ import annotations

from siliconvalley.adapter.outbound.orm.bighetti_hr_orm import BighettiHrOrm


class BighettiHrMapper:

    @staticmethod
    def to_entity(orm: BighettiHrOrm):
        raise NotImplementedError("BighettiHrOrm is abstract")

    @staticmethod
    def to_orm(entity) -> BighettiHrOrm:
        raise NotImplementedError("BighettiHrOrm is abstract")
