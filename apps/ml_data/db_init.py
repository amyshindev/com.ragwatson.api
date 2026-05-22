"""ML 4-Layer 테이블 — create_all 시 orm_registry 로 메타데이터에 등록됩니다."""

import logging

log = logging.getLogger(__name__)


def register_ml_models() -> None:
    """ORM 메타데이터 등록용 side-effect import."""
    from ml_data.models.audio_features import AudioFeature  # noqa: F401
    from ml_data.models.generation_logs import GenerationLog  # noqa: F401
    from ml_data.models.user_events import UserEvent  # noqa: F401
    from ml_data.models.visual_ratings import VisualRating  # noqa: F401

    log.debug("ml_data models registered")
