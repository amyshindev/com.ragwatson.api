from __future__ import annotations

from siliconvalley.adapter.outbound.orm.dinesh_dash_orm import DineshDashOrm


class DineshDashMapper:

    @staticmethod
    def to_entity(orm: DineshDashOrm):
        raise NotImplementedError("DineshDashOrm is abstract")

    @staticmethod
    def to_orm(entity) -> DineshDashOrm:
        raise NotImplementedError("DineshDashOrm is abstract")
