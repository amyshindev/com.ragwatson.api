from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.optic_resnet_classifier_dto import ResnetClassifierQuery, ResnetClassifierResponse


class ResnetClassifierPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: ResnetClassifierQuery) -> ResnetClassifierResponse:
        """레즈넷 (ResNet) 저장소"""
        pass
