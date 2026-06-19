from __future__ import annotations

import logging

from siliconvalley.adapter.inbound.api.schemas.dunn_coo_schema import DunnCooSchema
from siliconvalley.app.dtos.dunn_coo_dto import DunnCooQuery, DunnCooResponse
from siliconvalley.app.ports.input.dunn_coo_use_case import DunnCooUseCase
from siliconvalley.app.ports.output.dunn_coo_port import DunnCooPort

logger = logging.getLogger(__name__)


class DunnCooInteractor(DunnCooUseCase):

    def __init__(self, repository: DunnCooPort):
        self.repository = repository

    async def introduce_myself(self, schema: DunnCooSchema) -> DunnCooResponse:
        logger.info("[DunnCooInteractor] introduce_myself id=%s", schema.id)
        return await self.repository.introduce_myself(DunnCooQuery(
            id=schema.id,
            name=schema.name,
        ))
