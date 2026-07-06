"""YOLO 사전학습 가중치 기본값."""

from __future__ import annotations

# 초경량 nano (권장 기본값)
DEFAULT_YOLO_NANO_WEIGHTS = "yolo11n.pt"

# 호환성 높은 대안
YOLOV8_NANO_WEIGHTS = "yolov8n.pt"

# 선택: 얼굴 전용 사전학습 가중치 로컬 경로 (없으면 nano 일반 모델 사용)
# 예: backend/.env → VISION_FACE_BASE_WEIGHTS=C:\models\yolov8n-face.pt
ENV_FACE_BASE_WEIGHTS = "VISION_FACE_BASE_WEIGHTS"


def resolve_train_base_weights(explicit: str | None = None) -> str:
    """@deprecated — LocalYoloBaseWeightsAdapter 사용."""
    from vision.adapter.outbound.detection.local_yolo_base_weights_adapter import (
        LocalYoloBaseWeightsAdapter,
    )

    return LocalYoloBaseWeightsAdapter().resolve(explicit or DEFAULT_YOLO_NANO_WEIGHTS)
