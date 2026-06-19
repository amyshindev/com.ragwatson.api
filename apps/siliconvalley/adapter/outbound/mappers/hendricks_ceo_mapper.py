from __future__ import annotations

from siliconvalley.adapter.outbound.orm.hendricks_ceo_orm import HendricksCeoOrm


class HendricksCeoMapper:

    @staticmethod
    def to_entity(orm: HendricksCeoOrm):
        raise NotImplementedError("HendricksCeoOrm is abstract")

    @staticmethod
    def to_orm(entity) -> HendricksCeoOrm:
        raise NotImplementedError("HendricksCeoOrm is abstract")
