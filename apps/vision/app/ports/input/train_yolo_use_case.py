from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from vision.app.dtos.yolo_train_dto import YoloTrainHyperparams, YoloTrainResult


class TrainYoloUseCase(ABC):
    """YOLOv11 Nano 비전 훈련 인바운드 포트."""

    @abstractmethod
    def execute(
        self,
        hyperparams: YoloTrainHyperparams | None = None,
        *,
        force_prepare: bool = False,
    ) -> YoloTrainResult:
        """데이터셋 Port로 data.yaml을 받아 YOLO 파인튜닝을 실행합니다."""
