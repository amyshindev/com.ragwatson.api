from __future__ import annotations

from pathlib import Path

from vision.app.constants.vision_paths import RUNS_FACE_DETECT_DIR
from vision.app.ports.output.yolo_train_run_port import YoloTrainRunPort


class LocalYoloTrainRunAdapter(YoloTrainRunPort):
    """로컬 파일시스템 runs/face_detect 에 학습 산출물을 저장합니다."""

    def __init__(self, project_dir: Path | str | None = None) -> None:
        self._project_dir = Path(project_dir or RUNS_FACE_DETECT_DIR)

    def get_project_directory(self) -> str:
        return str(self._project_dir.resolve())

    def ensure_project_directory(self) -> None:
        self._project_dir.mkdir(parents=True, exist_ok=True)
