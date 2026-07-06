from __future__ import annotations

from sherlock_holmes.adapter.inbound.api.schemas.detective_sherlock_holmes_schema import SherlockHolmesSchema
from sherlock_holmes.app.dtos.detective_sherlock_holmes_dto import SherlockHolmesQuery, SherlockHolmesResponse
from sherlock_holmes.app.ports.input.detective_sherlock_holmes_use_case import SherlockHolmesUseCase
from sherlock_holmes.app.ports.output.detective_sherlock_holmes_port import SherlockHolmesPort


class SherlockHolmesInteractor(SherlockHolmesUseCase):
    def __init__(self, repository: SherlockHolmesPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: SherlockHolmesSchema) -> SherlockHolmesResponse:
        return await self._repository.introduce_myself(
            SherlockHolmesQuery(id=schema.id, name=schema.name)
        )


DetectiveSherlockHolmesInteractor = SherlockHolmesInteractor
