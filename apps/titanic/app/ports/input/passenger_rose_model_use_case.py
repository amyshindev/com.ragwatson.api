from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Literal

import numpy as np
import pandas as pd

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse


class TitanicAlgorithm(str, Enum):
    """titanic-algorithms.md TOP 10 — 런타임 전략 키"""

    XGBOOST = "xgboost"
    RANDOM_FOREST = "random_forest"
    LIGHTGBM = "lightgbm"
    CATBOOST = "catboost"
    LOGISTIC_REGRESSION = "logistic_regression"
    DECISION_TREE = "decision_tree"
    SVM = "svm"
    KNN = "knn"
    NAIVE_BAYES = "naive_bayes"
    KMEANS_PCA = "kmeans_pca"


ScalingMode = Literal["standard", "minmax", "none"]


class RoseModelAlgorithmStrategy(ABC):
    """타이타닉 생존 분류 알고리즘 전략 (Strategy)"""

    @property
    @abstractmethod
    def algorithm(self) -> TitanicAlgorithm:
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        pass

    @property
    @abstractmethod
    def scaling(self) -> ScalingMode:
        """standard: 아웃라이어 유무 · interval/ratio | minmax: 균일 분포 | none: 파이프라인 내장"""
        pass

    @abstractmethod
    def create_estimator(self) -> Any:
        pass


class RoseModelUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        """로즈 모델의 자기소개 메소드"""
        pass

    @abstractmethod
    def set_algorithm(self, algorithm: TitanicAlgorithm | str) -> None:
        """학습·추론에 사용할 알고리즘 전략을 선택한다"""
        pass

    @abstractmethod
    def get_algorithm(self) -> TitanicAlgorithm:
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        pass

    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        pass

    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        pass

    @abstractmethod
    def get_accuracy(self, X: pd.DataFrame, y: pd.Series) -> float:
        pass

    @abstractmethod
    def get_model_train(
        self,
        X: pd.DataFrame | None = None,
        y: pd.Series | None = None,
    ) -> dict[str, Any]:
        """titanic-algorithms.md 로드맵 — 로즈가 제안한 TOP 10 모델을 순차 훈련하고 최적 모델을 선택한다"""
        pass


PassengerRoseModelUseCase = RoseModelUseCase
