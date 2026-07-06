from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.app.dtos.inspector_lestrade_official_dto import LestradeOfficialQuery, LestradeOfficialResponse


class LestradeOfficialPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: LestradeOfficialQuery) -> LestradeOfficialResponse:
        """레스트레이드 자기소개 저장소"""
        pass


InspectorLestradeOfficialPort = LestradeOfficialPort
