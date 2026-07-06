from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.app.dtos.brother_mycroft_strategist_dto import MycroftStrategistQuery, MycroftStrategistResponse


class MycroftStrategistPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: MycroftStrategistQuery) -> MycroftStrategistResponse:
        """마이크로프트 자기소개 저장소"""
        pass


BrotherMycroftStrategistPort = MycroftStrategistPort
