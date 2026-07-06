from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.optic_clip_embedder_dto import ClipEmbedderQuery, ClipEmbedderResponse


class ClipEmbedderPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: ClipEmbedderQuery) -> ClipEmbedderResponse:
        """클립 (CLIP) 저장소"""
        pass
