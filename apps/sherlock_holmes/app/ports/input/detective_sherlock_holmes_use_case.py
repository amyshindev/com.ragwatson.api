from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.adapter.inbound.api.schemas.detective_sherlock_holmes_schema import SherlockHolmesSchema
from sherlock_holmes.app.dtos.detective_sherlock_holmes_dto import SherlockHolmesResponse


class SherlockHolmesUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: SherlockHolmesSchema) -> SherlockHolmesResponse:
        """셜록 홈즈 자기소개"""
        pass


DetectiveSherlockHolmesUseCase = SherlockHolmesUseCase
