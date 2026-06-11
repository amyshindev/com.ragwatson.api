from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatSchema,
    SmithCaptainSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
        self,
        repository,
        jack: JackTrainerInteractor | None = None,
        rose: RoseModelInteractor | None = None,
    ) -> None:
        self.repository = repository
        if jack is not None and rose is not None:
            jack.train_rose_model(rose)

    async def chat(self, schema: ChatSchema) -> str:
        return await self.repository.chat(schema)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))


CrewSmithCaptainInteractor = SmithCaptainInteractor
