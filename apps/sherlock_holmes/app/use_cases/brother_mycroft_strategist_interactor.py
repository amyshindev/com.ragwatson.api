from __future__ import annotations

from sherlock_holmes.adapter.inbound.api.schemas.brother_mycroft_strategist_schema import MycroftStrategistSchema
from sherlock_holmes.app.dtos.brother_mycroft_strategist_dto import MycroftStrategistQuery, MycroftStrategistResponse
from sherlock_holmes.app.ports.input.brother_mycroft_strategist_use_case import MycroftStrategistUseCase
from sherlock_holmes.app.ports.output.brother_mycroft_strategist_port import MycroftStrategistPort


class MycroftStrategistInteractor(MycroftStrategistUseCase):
    def __init__(self, repository: MycroftStrategistPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: MycroftStrategistSchema) -> MycroftStrategistResponse:
        return await self._repository.introduce_myself(
            MycroftStrategistQuery(id=schema.id, name=schema.name)
        )


BrotherMycroftStrategistInteractor = MycroftStrategistInteractor
