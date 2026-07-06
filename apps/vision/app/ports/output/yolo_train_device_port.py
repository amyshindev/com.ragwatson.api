from __future__ import annotations

from abc import ABC, abstractmethod


class YoloTrainDevicePort(ABC):
    """YOLO model.train(device=...) 값을 해석합니다."""

    @abstractmethod
    def resolve(self, requested: str | int) -> str | int:
        """
        requested:
          - "auto" → CUDA GPU 있으면 0, 없으면 cpu
          - "0", "cuda", "cpu", "mps" 등은 그대로 또는 정규화
        """
