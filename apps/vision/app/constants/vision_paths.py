"""Vision 앱 공통 경로 상수."""

from __future__ import annotations

from pathlib import Path

VISION_APP_ROOT = Path(__file__).resolve().parents[2]

# 원본 학습 데이터
YOLO_TRAIN_RAW_DIR = VISION_APP_ROOT / "tests" / "resources" / "yolo_train"

# YOLO 변환 데이터셋
PREPARED_FACE_YOLO_DIR = (
    VISION_APP_ROOT / "adapter" / "outbound" / "datasets" / "prepared_face_yolo"
)

# 학습 산출물
RUNS_FACE_DETECT_DIR = VISION_APP_ROOT / "adapter" / "outbound" / "runs" / "face_detect"

# S3 업로드 prefix (core.config VISION_S3_PREFIX 기본값과 동일)
S3_UPLOAD_PREFIX = "vision/uploads"
