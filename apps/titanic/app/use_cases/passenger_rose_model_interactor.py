from __future__ import annotations

from typing import Any, Callable

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import (
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.adapter.outbound.orm.passenger_rose_model_strategies import RoseModelStrategy
from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import (
    RoseModelAlgorithmStrategy,
    RoseModelUseCase,
    ScalingMode,
    TitanicAlgorithm,
)
from titanic.app.ports.output.passenger_rose_model_port import RoseModelPort
from titanic.app.use_cases.crew_walter_roaster_reader import WalterReader


# titanic-algorithms.md §4 로드맵 — Baseline → Scaling Up → TOP 10 전체
ROSE_BASELINE_ALGORITHMS: tuple[TitanicAlgorithm, ...] = (
    TitanicAlgorithm.LOGISTIC_REGRESSION,
    TitanicAlgorithm.RANDOM_FOREST,
)
ROSE_SCALING_UP_ALGORITHMS: tuple[TitanicAlgorithm, ...] = (
    TitanicAlgorithm.XGBOOST,
    TitanicAlgorithm.LIGHTGBM,
    TitanicAlgorithm.CATBOOST,
)
ROSE_SUGGESTED_ALGORITHMS: tuple[TitanicAlgorithm, ...] = tuple(TitanicAlgorithm)


class _SklearnEstimatorStrategy(RoseModelAlgorithmStrategy):
    def __init__(
        self,
        algorithm: TitanicAlgorithm,
        display_name: str,
        estimator_factory: Callable[[], object],
        scaling: ScalingMode,
    ) -> None:
        self._algorithm = algorithm
        self._display_name = display_name
        self._estimator_factory = estimator_factory
        self._scaling: ScalingMode = scaling

    @property
    def algorithm(self) -> TitanicAlgorithm:
        return self._algorithm

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def scaling(self) -> ScalingMode:
        return self._scaling

    def create_estimator(self) -> Any:
        return self._estimator_factory()


def _kmeans_pca_estimator() -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=3, random_state=42)),
            ("kmeans", KMeans(n_clusters=3, random_state=42, n_init="auto")),
            ("clf", KNeighborsClassifier(n_neighbors=3)),
        ]
    )


ALGORITHM_STRATEGIES: dict[TitanicAlgorithm, RoseModelAlgorithmStrategy] = {
    TitanicAlgorithm.XGBOOST: _SklearnEstimatorStrategy(
        TitanicAlgorithm.XGBOOST,
        "XGBoost (GradientBoosting)",
        lambda: GradientBoostingClassifier(random_state=42),
        scaling="standard",
    ),
    TitanicAlgorithm.RANDOM_FOREST: _SklearnEstimatorStrategy(
        TitanicAlgorithm.RANDOM_FOREST,
        "Random Forest",
        lambda: RandomForestClassifier(random_state=42, n_estimators=100),
        scaling="minmax",
    ),
    TitanicAlgorithm.LIGHTGBM: _SklearnEstimatorStrategy(
        TitanicAlgorithm.LIGHTGBM,
        "LightGBM (HistGradientBoosting)",
        lambda: HistGradientBoostingClassifier(random_state=42),
        scaling="standard",
    ),
    TitanicAlgorithm.CATBOOST: _SklearnEstimatorStrategy(
        TitanicAlgorithm.CATBOOST,
        "CatBoost (ExtraTrees)",
        lambda: ExtraTreesClassifier(random_state=42, n_estimators=100),
        scaling="minmax",
    ),
    TitanicAlgorithm.LOGISTIC_REGRESSION: _SklearnEstimatorStrategy(
        TitanicAlgorithm.LOGISTIC_REGRESSION,
        "Logistic Regression",
        lambda: LogisticRegression(max_iter=1000, random_state=42),
        scaling="standard",
    ),
    TitanicAlgorithm.DECISION_TREE: _SklearnEstimatorStrategy(
        TitanicAlgorithm.DECISION_TREE,
        "Decision Tree",
        lambda: DecisionTreeClassifier(random_state=42, max_depth=5),
        scaling="minmax",
    ),
    TitanicAlgorithm.SVM: _SklearnEstimatorStrategy(
        TitanicAlgorithm.SVM,
        "SVM",
        lambda: SVC(probability=True, random_state=42),
        scaling="standard",
    ),
    TitanicAlgorithm.KNN: _SklearnEstimatorStrategy(
        TitanicAlgorithm.KNN,
        "KNN",
        lambda: KNeighborsClassifier(n_neighbors=3),
        scaling="standard",
    ),
    TitanicAlgorithm.NAIVE_BAYES: _SklearnEstimatorStrategy(
        TitanicAlgorithm.NAIVE_BAYES,
        "Naive Bayes",
        lambda: GaussianNB(),
        scaling="standard",
    ),
    TitanicAlgorithm.KMEANS_PCA: _SklearnEstimatorStrategy(
        TitanicAlgorithm.KMEANS_PCA,
        "K-Means & PCA",
        _kmeans_pca_estimator,
        scaling="none",
    ),
}


class RoseModelInteractor(RoseModelUseCase):

    def __init__(
        self,
        repository: RoseModelPort | None = None,
        algorithm: TitanicAlgorithm | str = TitanicAlgorithm.DECISION_TREE,
    ) -> None:
        self.repository = repository
        self._strategy = self._resolve_strategy(algorithm)
        self._scaler: StandardScaler | MinMaxScaler | None = None
        self.model: Any = self._strategy.create_estimator()
        self._active_strategy: RoseModelStrategy | None = None

    def set_strategy(self, strategy: RoseModelStrategy) -> None:
        self._active_strategy = strategy

    def predict_strategy_rows(self, rows: list[list[float]]) -> list[int]:
        if self._active_strategy is None:
            raise RuntimeError("장착된 RoseModelStrategy가 없습니다.")
        return self._active_strategy.predict(rows)

    def _resolve_strategy(self, algorithm: TitanicAlgorithm | str) -> RoseModelAlgorithmStrategy:
        key = TitanicAlgorithm(algorithm) if isinstance(algorithm, str) else algorithm
        strategy = ALGORITHM_STRATEGIES.get(key)
        if strategy is None:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        return strategy

    def set_algorithm(self, algorithm: TitanicAlgorithm | str) -> None:
        self._strategy = self._resolve_strategy(algorithm)
        self._scaler = None
        self.model = self._strategy.create_estimator()

    def get_algorithm(self) -> TitanicAlgorithm:
        return self._strategy.algorithm

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        if self.repository is None:
            return RoseModelResponse(id=schema.id, name=schema.name)

        return await self.repository.introduce_myself(RoseModelQuery(
            id=schema.id,
            name=schema.name,
        ))

    def get_model_name(self) -> str:
        return self._strategy.display_name

    def _build_scaler(self) -> StandardScaler | MinMaxScaler | None:
        if self._strategy.scaling == "standard":
            return StandardScaler()
        if self._strategy.scaling == "minmax":
            return MinMaxScaler()
        return None

    def _transform_features(self, X: pd.DataFrame, *, fit: bool) -> np.ndarray:
        values = X.to_numpy()
        if self._strategy.scaling == "none":
            return values

        if self._scaler is None:
            scaler = self._build_scaler()
            if scaler is None:
                return values
            self._scaler = scaler

        if fit:
            return np.asarray(self._scaler.fit_transform(values))

        return np.asarray(self._scaler.transform(values))

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        self._scaler = None
        X_scaled = self._transform_features(X, fit=True)
        self.model = self._strategy.create_estimator()
        self.model.fit(X_scaled, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        X_scaled = self._transform_features(X, fit=False)
        return np.asarray(self.model.predict(X_scaled))

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        X_scaled = self._transform_features(X, fit=False)
        if not hasattr(self.model, "predict_proba"):
            raise AttributeError(f"{self.get_model_name()} does not support predict_proba")
        return np.asarray(self.model.predict_proba(X_scaled))

    def get_accuracy(self, X: pd.DataFrame, y: pd.Series) -> float:
        X_scaled = self._transform_features(X, fit=False)
        return float(self.model.score(X_scaled, y))

    def _fallback_training_data(self) -> tuple[pd.DataFrame, pd.Series]:
        return (
            pd.DataFrame(
                {
                    "Pclass": [1, 3, 3, 1],
                    "Sex": [1, 0, 0, 1],
                    "Age": [28, 20, 22, 35],
                    "SibSp": [0, 0, 1, 1],
                    "Parch": [0, 0, 0, 1],
                    "Fare": [80.0, 7.0, 9.0, 55.0],
                }
            ),
            pd.Series([1, 0, 0, 1]),
        )

    def _resolve_training_data(
        self,
        X: pd.DataFrame | None,
        y: pd.Series | None,
    ) -> tuple[pd.DataFrame, pd.Series]:
        if X is not None and y is not None and not X.empty and not y.empty:
            return X, y

        reader = WalterReader()
        features, labels = reader.get_features_and_labels()
        if not features.empty and not labels.empty:
            return features, labels

        return self._fallback_training_data()

    def _train_algorithm(self, algorithm: TitanicAlgorithm, X: pd.DataFrame, y: pd.Series) -> dict[str, Any]:
        self.set_algorithm(algorithm)
        self.train(X, y)
        accuracy = self.get_accuracy(X, y)
        return {
            "algorithm": algorithm.value,
            "model_name": self.get_model_name(),
            "scaling": self._strategy.scaling,
            "accuracy": accuracy,
        }

    def get_model_train(
        self,
        X: pd.DataFrame | None = None,
        y: pd.Series | None = None,
    ) -> dict[str, Any]:
        '''로즈가 제안한 모델들(titanic-algorithms.md TOP 10)을 훈련하고 최고 성능 전략을 채택한다'''

        features, labels = self._resolve_training_data(X, y)
        results: list[dict[str, Any]] = []

        for algorithm in ROSE_SUGGESTED_ALGORITHMS:
            results.append(self._train_algorithm(algorithm, features, labels))

        best = max(results, key=lambda row: row["accuracy"])

        self.set_algorithm(TitanicAlgorithm(best["algorithm"]))
        self.train(features, labels)

        def _phase_summary(phase: str, algorithms: tuple[TitanicAlgorithm, ...]) -> dict[str, Any]:
            keys = {algo.value for algo in algorithms}
            phase_rows = [row for row in results if row["algorithm"] in keys]
            phase_best = max(phase_rows, key=lambda row: row["accuracy"])
            return {
                "phase": phase,
                "models": phase_rows,
                "best_algorithm": phase_best["algorithm"],
                "best_accuracy": phase_best["accuracy"],
            }

        return {
            "feature_columns": list(features.columns),
            "target_name": "Survived",
            "sample_count": len(features),
            "results": results,
            "roadmap": {
                "baseline": _phase_summary("baseline", ROSE_BASELINE_ALGORITHMS),
                "scaling_up": _phase_summary("scaling_up", ROSE_SCALING_UP_ALGORITHMS),
                "full_top10": _phase_summary("full_top10", ROSE_SUGGESTED_ALGORITHMS),
            },
            "best_algorithm": best["algorithm"],
            "best_model_name": best["model_name"],
            "best_accuracy": best["accuracy"],
        }


PassengerRoseModelInteractor = RoseModelInteractor
RoseModelTrainInteractor = RoseModelInteractor
