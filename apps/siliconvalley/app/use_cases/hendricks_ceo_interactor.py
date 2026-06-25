from __future__ import annotations

import logging

from siliconvalley.adapter.inbound.api.schemas.hendricks_ceo_schema import HendricksCeoSchema
from siliconvalley.app.dtos.hendricks_ceo_dto import HendricksCeoQuery, HendricksCeoResponse
from siliconvalley.app.ports.input.hendricks_ceo_use_case import HendricksCeoUseCase
from siliconvalley.app.ports.output.hendricks_ceo_port import HendricksCeoPort

logger = logging.getLogger(__name__)


class HendricksCeoInteractor(HendricksCeoUseCase):
    def __init__(self, repository: HendricksCeoPort):
        self.repository = repository

    async def introduce_myself(self, schema: HendricksCeoSchema) -> HendricksCeoResponse:
        logger.info("[HendricksCeoInteractor] introduce_myself id=%s", schema.id)
        return await self.repository.introduce_myself(
            HendricksCeoQuery(
                id=schema.id,
                name=schema.name,
            )
        )
