"""ML 데이터 ORM 등록 (orm_registry 가 단일 소스이면 이 모듈은 선택)."""

import logging

log = logging.getLogger(__name__)


def register_ml_models() -> None:
    from ml_data.adapter.outbound.orm.audio_feature_orm import AudioFeature  # noqa: F401
    from ml_data.adapter.outbound.orm.generation_log_orm import GenerationLog  # noqa: F401
    from ml_data.adapter.outbound.orm.user_event_orm import UserEvent  # noqa: F401
    from ml_data.adapter.outbound.orm.visual_rating_orm import VisualRating  # noqa: F401

    log.debug("ml_data models registered")
