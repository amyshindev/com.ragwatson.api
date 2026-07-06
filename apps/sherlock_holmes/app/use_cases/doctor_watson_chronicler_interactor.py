from __future__ import annotations

from sherlock_holmes.adapter.inbound.api.schemas.doctor_watson_chronicler_schema import WatsonChroniclerSchema
from sherlock_holmes.app.dtos.doctor_watson_chronicler_dto import WatsonChroniclerQuery, WatsonChroniclerResponse
from sherlock_holmes.app.ports.input.doctor_watson_chronicler_use_case import WatsonChroniclerUseCase
from sherlock_holmes.app.ports.output.doctor_watson_chronicler_port import WatsonChroniclerPort


class WatsonChroniclerInteractor(WatsonChroniclerUseCase):
    def __init__(self, repository: WatsonChroniclerPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: WatsonChroniclerSchema) -> WatsonChroniclerResponse:
        return await self._repository.introduce_myself(
            WatsonChroniclerQuery(id=schema.id, name=schema.name)
        )


DoctorWatsonChroniclerInteractor = WatsonChroniclerInteractor
