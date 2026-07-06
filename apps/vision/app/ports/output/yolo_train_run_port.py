from __future__ import annotations

from abc import ABC, abstractmethod


class YoloTrainRunPort(ABC):
    """Ultralytics 학습 산출물 저장 위치(로컬/S3 동기화 등)를 제공합니다."""

    @abstractmethod
    def get_project_directory(self) -> str:
        """model.train(project=...)에 전달할 디렉터리 경로."""

    @abstractmethod
    def ensure_project_directory(self) -> None:
        """학습 시작 전 저장소 준비."""
