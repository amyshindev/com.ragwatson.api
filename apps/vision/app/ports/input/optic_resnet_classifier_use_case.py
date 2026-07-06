from __future__ import annotations

from abc import ABC, abstractmethod

from vision.adapter.inbound.api.schemas.optic_resnet_classifier_schema import ResnetClassifierSchema
from vision.app.dtos.optic_resnet_classifier_dto import ResnetClassifierResponse


class ResnetClassifierUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: ResnetClassifierSchema) -> ResnetClassifierResponse:
        """레즈넷 (ResNet) 자기소개"""
        pass
