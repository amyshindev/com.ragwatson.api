from __future__ import annotations

import os
from pathlib import Path

from vision.app.constants.yolo_models import (
    DEFAULT_YOLO_NANO_WEIGHTS,
    ENV_FACE_BASE_WEIGHTS,
)
from vision.app.constants.vision_paths import VISION_APP_ROOT
from vision.app.ports.output.yolo_base_weights_port import YoloBaseWeightsPort

# 레포에 포함된 Hugging Face 얼굴 탐지 체크포인트 (선택)
_LOCAL_HF_FACE_MODEL = VISION_APP_ROOT / "tests" / "resources" / "models" / "model.pt"


class LocalYoloBaseWeightsAdapter(YoloBaseWeightsPort):
    """
    시작 가중치 해석 — 환경 변수·로컬 HF 모델·요청값·yolo11n.pt 순.
    App Use Case는 os.environ을 읽지 않습니다.
    """

    def resolve(self, requested: str) -> str:
        from_env = (os.getenv(ENV_FACE_BASE_WEIGHTS) or "").strip()
        if from_env:
            return str(Path(from_env).resolve()) if Path(from_env).exists() else from_env

        explicit = (requested or "").strip()
        if explicit and explicit != DEFAULT_YOLO_NANO_WEIGHTS:
            return explicit

        if _LOCAL_HF_FACE_MODEL.is_file():
            return str(_LOCAL_HF_FACE_MODEL.resolve())

        return DEFAULT_YOLO_NANO_WEIGHTS
