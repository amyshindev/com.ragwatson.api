from __future__ import annotations

import logging

from siliconvalley.adapter.inbound.api.schemas.bighetti_hr_schema import BighettiHrSchema
from siliconvalley.app.dtos.bighetti_hr_dto import BighettiHrQuery, BighettiHrResponse
from siliconvalley.app.ports.input.bighetti_hr_use_case import BighettiHrUseCase
from siliconvalley.app.ports.output.bighetti_hr_port import BighettiHrPort

logger = logging.getLogger(__name__)


class BighettiHrInteractor(BighettiHrUseCase):

    def __init__(self, repository: BighettiHrPort):
        self.repository = repository

    async def introduce_myself(self, schema: BighettiHrSchema) -> BighettiHrResponse:
        logger.info("[BighettiHrInteractor] introduce_myself id=%s", schema.id)
        return await self.repository.introduce_myself(BighettiHrQuery(
            id=schema.id,
            name=schema.name,
        ))
