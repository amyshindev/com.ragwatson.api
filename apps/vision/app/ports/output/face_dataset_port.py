from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class FaceDatasetManifest:
    yaml_path: str
    prepared_root: str
    raw_root: str
    class_names: tuple[str, ...]
    train_images: int
    val_images: int


class FaceDatasetPort(ABC):
    """YOLO 얼굴 학습용 데이터셋 공급 포트."""

    @abstractmethod
    def prepare_dataset(self, *, force: bool = False) -> FaceDatasetManifest:
        """원본 이미지를 YOLO 포맷으로 정제하고 manifest를 반환합니다."""

    @abstractmethod
    def get_dataset_config_path(self, *, force_prepare: bool = False) -> str:
        """data.yaml 절대 경로를 반환합니다."""
