from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.adapter.inbound.api.schemas.brother_mycroft_strategist_schema import MycroftStrategistSchema
from sherlock_holmes.app.dtos.brother_mycroft_strategist_dto import MycroftStrategistResponse


class MycroftStrategistUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: MycroftStrategistSchema) -> MycroftStrategistResponse:
        """마이크로프트 자기소개"""
        pass


BrotherMycroftStrategistUseCase = MycroftStrategistUseCase
