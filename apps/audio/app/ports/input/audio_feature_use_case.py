from abc import ABC, abstractmethod
from uuid import UUID

from audio.adapter.inbound.api.schemas.audio_features import (
    AudioFeatureCreate,
    AudioFeatureRead,
    AudioFeatureStatusRead,
)


class AudioFeatureUseCase(ABC):
    @abstractmethod
    async def ingest(self, body: AudioFeatureCreate) -> AudioFeatureRead:
        ...

    @abstractmethod
    async def get(self, feature_id: UUID) -> AudioFeatureRead:
        ...

    @abstractmethod
    async def get_status(self, feature_id: UUID) -> AudioFeatureStatusRead:
        ...

    @abstractmethod
    async def list_by_user(
        self, user_id: int, limit: int, offset: int
    ) -> list[AudioFeatureRead]:
        ...

    @abstractmethod
    async def update_inference_result(
        self, feature_id: UUID, result: dict
    ) -> AudioFeatureRead:
        ...

    @abstractmethod
    async def update_visual_mapping(
        self, feature_id: UUID, mapping: dict
    ) -> AudioFeatureRead:
        ...

    @abstractmethod
    async def update_beat_analysis(
        self, feature_id: UUID, analysis: dict
    ) -> AudioFeatureRead:
        ...
