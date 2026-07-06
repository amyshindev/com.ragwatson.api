from __future__ import annotations

from dataclasses import dataclass

from vision.app.dtos.yolo_train_dto import YoloTrainHyperparams, YoloTrainResult

# 하위 호환 alias
FaceTrainHyperparams = YoloTrainHyperparams
FaceTrainResult = YoloTrainResult


@dataclass(frozen=True)
class FaceDetectionBox:
    class_id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass(frozen=True)
class FaceDetectResult:
    source: str
    detections: tuple[FaceDetectionBox, ...]
    weights_path: str
