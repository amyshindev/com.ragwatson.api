from __future__ import annotations

from sherlock_holmes.adapter.inbound.api.schemas.mrs_hudson_housekeeper_schema import HudsonHousekeeperSchema
from sherlock_holmes.app.dtos.mrs_hudson_housekeeper_dto import HudsonHousekeeperQuery, HudsonHousekeeperResponse
from sherlock_holmes.app.ports.input.mrs_hudson_housekeeper_use_case import HudsonHousekeeperUseCase
from sherlock_holmes.app.ports.output.mrs_hudson_housekeeper_port import HudsonHousekeeperPort


class HudsonHousekeeperInteractor(HudsonHousekeeperUseCase):
    def __init__(self, repository: HudsonHousekeeperPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: HudsonHousekeeperSchema) -> HudsonHousekeeperResponse:
        return await self._repository.introduce_myself(
            HudsonHousekeeperQuery(id=schema.id, name=schema.name)
        )


MrsHudsonHousekeeperInteractor = HudsonHousekeeperInteractor
