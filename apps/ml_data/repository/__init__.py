from ml_data.repository.audio_features import AudioFeatureRepository
from ml_data.repository.generation_logs import GenerationLogRepository
from ml_data.repository.user_events import UserEventRepository
from ml_data.repository.visual_ratings import VisualRatingRepository


class MlDataRepositories:
    def __init__(self) -> None:
        self.audio_features = AudioFeatureRepository()
        self.user_events = UserEventRepository()
        self.generation_logs = GenerationLogRepository()
        self.visual_ratings = VisualRatingRepository()


__all__ = ["MlDataRepositories"]
