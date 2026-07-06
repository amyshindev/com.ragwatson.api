from __future__ import annotations

from sherlock_holmes.adapter.inbound.api.schemas.inspector_lestrade_official_schema import LestradeOfficialSchema
from sherlock_holmes.app.dtos.inspector_lestrade_official_dto import LestradeOfficialQuery, LestradeOfficialResponse
from sherlock_holmes.app.ports.input.inspector_lestrade_official_use_case import LestradeOfficialUseCase
from sherlock_holmes.app.ports.output.inspector_lestrade_official_port import LestradeOfficialPort


class LestradeOfficialInteractor(LestradeOfficialUseCase):
    def __init__(self, repository: LestradeOfficialPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: LestradeOfficialSchema) -> LestradeOfficialResponse:
        return await self._repository.introduce_myself(
            LestradeOfficialQuery(id=schema.id, name=schema.name)
        )


InspectorLestradeOfficialInteractor = LestradeOfficialInteractor
