from __future__ import annotations

from abc import ABC, abstractmethod


class YoloBaseWeightsPort(ABC):
    """YOLO 시작 가중치(yolo11n.pt, HF model.pt 등) 경로를 해석합니다."""

    @abstractmethod
    def resolve(self, requested: str) -> str:
        """요청된 가중치 식별자를 실제 로드 가능한 경로/이름으로 반환합니다."""
