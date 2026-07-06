from __future__ import annotations

from dataclasses import dataclass

from vision.app.constants.yolo_models import DEFAULT_YOLO_NANO_WEIGHTS


@dataclass(frozen=True)
class YoloTrainHyperparams:
    """훈련 하이퍼파라미터 — 인프라 경로 없음."""

    base_weights: str = DEFAULT_YOLO_NANO_WEIGHTS
    epochs: int = 10
    batch_size: int = 8
    imgsz: int = 640
    device: str | int = "auto"
    run_name: str = "train"


@dataclass(frozen=True)
class YoloTrainResult:
    ok: bool
    dataset_yaml: str
    base_weights: str
    weights_path: str | None
    save_dir: str | None
    message: str
