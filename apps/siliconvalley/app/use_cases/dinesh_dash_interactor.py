from __future__ import annotations

import logging

from siliconvalley.adapter.inbound.api.schemas.dinesh_dash_schema import DineshDashSchema
from siliconvalley.app.dtos.dinesh_dash_dto import DineshDashQuery, DineshDashResponse
from siliconvalley.app.ports.input.dinesh_dash_use_case import DineshDashUseCase
from siliconvalley.app.ports.output.dinesh_dash_port import DineshDashPort

logger = logging.getLogger(__name__)


class DineshDashInteractor(DineshDashUseCase):
    def __init__(self, repository: DineshDashPort):
        self.repository = repository

    async def introduce_myself(self, schema: DineshDashSchema) -> DineshDashResponse:
        logger.info("[DineshDashInteractor] introduce_myself id=%s", schema.id)
        return await self.repository.introduce_myself(
            DineshDashQuery(
                id=schema.id,
                name=schema.name,
            )
        )
