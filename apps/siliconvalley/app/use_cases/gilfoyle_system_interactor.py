from __future__ import annotations

import logging

from siliconvalley.adapter.inbound.api.schemas.gilfoyle_system_schema import GilfoyleSystemSchema
from siliconvalley.app.dtos.gilfoyle_system_dto import GilfoyleSystemQuery, GilfoyleSystemResponse
from siliconvalley.app.ports.input.gilfoyle_system_use_case import GilfoyleSystemUseCase
from siliconvalley.app.ports.output.gilfoyle_system_port import GilfoyleSystemPort

logger = logging.getLogger(__name__)


class GilfoyleSystemInteractor(GilfoyleSystemUseCase):
    def __init__(self, repository: GilfoyleSystemPort):
        self.repository = repository

    async def introduce_myself(self, schema: GilfoyleSystemSchema) -> GilfoyleSystemResponse:
        logger.info("[GilfoyleSystemInteractor] introduce_myself id=%s", schema.id)
        return await self.repository.introduce_myself(
            GilfoyleSystemQuery(
                id=schema.id,
                name=schema.name,
            )
        )
