from __future__ import annotations

from siliconvalley.adapter.outbound.orm.gilfoyle_system_orm import GilfoyleSystemOrm


class GilfoyleSystemMapper:

    @staticmethod
    def to_entity(orm: GilfoyleSystemOrm):
        raise NotImplementedError("GilfoyleSystemOrm is abstract")

    @staticmethod
    def to_orm(entity) -> GilfoyleSystemOrm:
        raise NotImplementedError("GilfoyleSystemOrm is abstract")
