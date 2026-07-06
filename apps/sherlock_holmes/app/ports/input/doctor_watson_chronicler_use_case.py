from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.adapter.inbound.api.schemas.doctor_watson_chronicler_schema import WatsonChroniclerSchema
from sherlock_holmes.app.dtos.doctor_watson_chronicler_dto import WatsonChroniclerResponse


class WatsonChroniclerUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: WatsonChroniclerSchema) -> WatsonChroniclerResponse:
        """왓슨 자기소개"""
        pass


DoctorWatsonChroniclerUseCase = WatsonChroniclerUseCase
