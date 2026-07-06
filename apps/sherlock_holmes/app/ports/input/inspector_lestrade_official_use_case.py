from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.adapter.inbound.api.schemas.inspector_lestrade_official_schema import LestradeOfficialSchema
from sherlock_holmes.app.dtos.inspector_lestrade_official_dto import LestradeOfficialResponse


class LestradeOfficialUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: LestradeOfficialSchema) -> LestradeOfficialResponse:
        """레스트레이드 자기소개"""
        pass


InspectorLestradeOfficialUseCase = LestradeOfficialUseCase
