from __future__ import annotations

from abc import ABC, abstractmethod


class FaceModelCheckpointPort(ABC):
    """학습된 YOLO 가중치 경로를 제공하는 포트."""

    @abstractmethod
    def get_default_weights_path(self) -> str | None:
        """가장 최근 학습된 best.pt 경로. 없으면 None."""

    @abstractmethod
    def resolve_weights_path(self, explicit: str | None = None) -> str:
        """명시 경로 또는 기본 경로를 반환합니다."""
