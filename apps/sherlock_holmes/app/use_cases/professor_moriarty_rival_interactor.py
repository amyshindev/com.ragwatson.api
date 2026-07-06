from __future__ import annotations

from sherlock_holmes.adapter.inbound.api.schemas.professor_moriarty_rival_schema import MoriartyRivalSchema
from sherlock_holmes.app.dtos.professor_moriarty_rival_dto import MoriartyRivalQuery, MoriartyRivalResponse
from sherlock_holmes.app.ports.input.professor_moriarty_rival_use_case import MoriartyRivalUseCase
from sherlock_holmes.app.ports.output.professor_moriarty_rival_port import MoriartyRivalPort


class MoriartyRivalInteractor(MoriartyRivalUseCase):
    def __init__(self, repository: MoriartyRivalPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: MoriartyRivalSchema) -> MoriartyRivalResponse:
        return await self._repository.introduce_myself(
            MoriartyRivalQuery(id=schema.id, name=schema.name)
        )


ProfessorMoriartyRivalInteractor = MoriartyRivalInteractor
