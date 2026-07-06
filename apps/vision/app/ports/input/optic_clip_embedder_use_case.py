from __future__ import annotations

from abc import ABC, abstractmethod

from vision.adapter.inbound.api.schemas.optic_clip_embedder_schema import ClipEmbedderSchema
from vision.app.dtos.optic_clip_embedder_dto import ClipEmbedderResponse


class ClipEmbedderUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: ClipEmbedderSchema) -> ClipEmbedderResponse:
        """클립 (CLIP) 자기소개"""
        pass
