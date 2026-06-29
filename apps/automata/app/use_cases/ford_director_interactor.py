from __future__ import annotations

import logging

from automata.adapter.inbound.api.schemas.ford_director_schema import (
    FordDirectorSchema,
    FordDirectorTriggerSchema,
)
from automata.app.dtos.ford_director_dto import FordDirectorQuery, FordDirectorResponse
from automata.app.ports.input.ford_director_use_case import FordDirectorUseCase
from automata.app.ports.output.ford_director_port import FordDirectorPort

logger = logging.getLogger(__name__)


class FordDirectorInteractor(FordDirectorUseCase):
    def __init__(self, repository: FordDirectorPort) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: FordDirectorSchema) -> FordDirectorResponse:
        logger.info("[FordDirectorInteractor] introduce_myself id=%s", schema.id)
        return await self.repository.introduce_myself(
            FordDirectorQuery(id=schema.id, name=schema.name),
        )

    async def trigger_workflow(self, schema: FordDirectorTriggerSchema) -> FordDirectorResponse:
        logger.info("[FordDirectorInteractor] trigger workflow=%s", schema.workflow)
        return await self.repository.trigger_workflow(
            FordDirectorQuery(
                id=1,
                name="Robert Ford (Director)",
                workflow=schema.workflow,
                payload=schema.payload,
            ),
        )
