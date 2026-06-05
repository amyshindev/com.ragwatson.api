from abc import ABC, abstractmethod
from uuid import UUID

from ml_data.adapter.inbound.api.schemas.audio_features import AudioFeatureCreate
from ml_data.adapter.outbound.orm.audio_feature_orm import AudioFeature


class AudioFeatureRepository(ABC):
    @abstractmethod
    async def create(self, body: AudioFeatureCreate) -> AudioFeature:
        ...

    @abstractmethod
    async def get(self, feature_id: UUID) -> AudioFeature | None:
        ...

    @abstractmethod
    async def list_by_user(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[AudioFeature]:
        ...

    @abstractmethod
    async def update_inference_result(
        self, feature_id: UUID, result: dict
    ) -> AudioFeature:
        ...

    @abstractmethod
    async def update_visual_mapping(
        self, feature_id: UUID, mapping: dict
    ) -> AudioFeature:
        ...

    @abstractmethod
    async def update_beat_analysis(
        self, feature_id: UUID, analysis: dict
    ) -> AudioFeature:
        ...
