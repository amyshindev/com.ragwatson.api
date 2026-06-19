from __future__ import annotations

from siliconvalley.adapter.outbound.orm.dunn_coo_orm import DunnCooOrm


class DunnCooMapper:

    @staticmethod
    def to_entity(orm: DunnCooOrm):
        raise NotImplementedError("DunnCooOrm is abstract")

    @staticmethod
    def to_orm(entity) -> DunnCooOrm:
        raise NotImplementedError("DunnCooOrm is abstract")
