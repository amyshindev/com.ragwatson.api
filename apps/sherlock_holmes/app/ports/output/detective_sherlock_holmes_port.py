from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.app.dtos.detective_sherlock_holmes_dto import SherlockHolmesQuery, SherlockHolmesResponse


class SherlockHolmesPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: SherlockHolmesQuery) -> SherlockHolmesResponse:
        """셜록 홈즈 자기소개 저장소"""
        pass


DetectiveSherlockHolmesPort = SherlockHolmesPort
