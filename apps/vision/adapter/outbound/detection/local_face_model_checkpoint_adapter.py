from __future__ import annotations

import logging
import os
from pathlib import Path

from vision.app.constants.vision_paths import RUNS_FACE_DETECT_DIR
from vision.app.ports.output.face_model_checkpoint_port import FaceModelCheckpointPort

log = logging.getLogger(__name__)


class LocalFaceModelCheckpointAdapter(FaceModelCheckpointPort):
    """학습 산출물(runs/face_detect/**/weights/best.pt) 경로를 탐색합니다."""

    def __init__(
        self,
        *,
        runs_root: Path | str | None = None,
        env_var: str = "VISION_FACE_MODEL_PATH",
    ) -> None:
        self._runs_root = Path(runs_root or RUNS_FACE_DETECT_DIR)
        self._env_var = env_var

    def get_default_weights_path(self) -> str | None:
        env_path = (os.getenv(self._env_var) or "").strip()
        if env_path and Path(env_path).is_file():
            return str(Path(env_path).resolve())

        candidates = sorted(
            self._runs_root.glob("**/weights/best.pt"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            return None
        return str(candidates[0].resolve())

    def resolve_weights_path(self, explicit: str | None = None) -> str:
        if explicit and Path(explicit).is_file():
            return str(Path(explicit).resolve())

        default = self.get_default_weights_path()
        if default:
            return default

        raise FileNotFoundError(
            "학습된 얼굴 인식 가중치를 찾을 수 없습니다. "
            "먼저 TrainFaceDetectorInteractor로 학습하거나 "
            f"{self._env_var} 환경 변수를 설정하세요.",
        )
