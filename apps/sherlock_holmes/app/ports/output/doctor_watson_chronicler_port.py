from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.app.dtos.doctor_watson_chronicler_dto import WatsonChroniclerQuery, WatsonChroniclerResponse


class WatsonChroniclerPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: WatsonChroniclerQuery) -> WatsonChroniclerResponse:
        """왓슨 자기소개 저장소"""
        pass


DoctorWatsonChroniclerPort = WatsonChroniclerPort
