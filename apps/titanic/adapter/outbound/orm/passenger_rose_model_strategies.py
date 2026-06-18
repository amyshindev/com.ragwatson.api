from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


class RoseModelStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def fit(self, X: Any, y: Any) -> None:
        pass

    @abstractmethod
    def predict(self, X: Any) -> list[int]:
        pass

    @abstractmethod
    def predict_proba(self, X: Any) -> list[float]:
        pass


class XGBoostStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "XGBoost"

    @property
    def description(self) -> str:
        return "그래디언트 부스팅 기반 고성능 모델."

    def __init__(self) -> None:
        self._model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class RandomForestStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "RandomForest"

    @property
    def description(self) -> str:
        return "다수의 결정 트리를 결합하는 배깅 방식."

    def __init__(self) -> None:
        self._model = RandomForestClassifier(n_estimators=100, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class LightGBMStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "LightGBM"

    @property
    def description(self) -> str:
        return "리프 중심 트리 분할 방식의 부스팅."

    def __init__(self) -> None:
        self._model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class CatBoostStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "CatBoost"

    @property
    def description(self) -> str:
        return "범주형 데이터 처리에 최적화된 부스팅."

    def __init__(self) -> None:
        self._model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class LogisticRegressionStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "LogisticRegression"

    @property
    def description(self) -> str:
        return "선형 기반 이진 분류 Baseline."

    def __init__(self) -> None:
        self._scaler = StandardScaler()
        self._model = LogisticRegression(max_iter=1000, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(self._scaler.fit_transform(X), y)

    def predict(self, X) -> list[int]:
        return self._model.predict(self._scaler.transform(X)).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class DecisionTreeStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "DecisionTree"

    @property
    def description(self) -> str:
        return "직관적인 규칙 기반 결정 트리."

    def __init__(self) -> None:
        self._model = DecisionTreeClassifier(max_depth=5, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class SVMStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "SVM"

    @property
    def description(self) -> str:
        return "마진 최대화 결정 경계 탐색."

    def __init__(self) -> None:
        self._scaler = StandardScaler()
        self._model = SVC(kernel="rbf", probability=True, random_state=42)

    def fit(self, X, y) -> None:
        self._model.fit(self._scaler.fit_transform(X), y)

    def predict(self, X) -> list[int]:
        return self._model.predict(self._scaler.transform(X)).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class KNNStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "KNN"

    @property
    def description(self) -> str:
        return "K-최근접 이웃 분류."

    def __init__(self, k: int = 5) -> None:
        self._scaler = MinMaxScaler()
        self._model = KNeighborsClassifier(n_neighbors=k)

    def fit(self, X, y) -> None:
        self._model.fit(self._scaler.fit_transform(X), y)

    def predict(self, X) -> list[int]:
        return self._model.predict(self._scaler.transform(X)).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(self._scaler.transform(X))[:, 1].tolist()


class NaiveBayesStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "NaiveBayes"

    @property
    def description(self) -> str:
        return "베이즈 정리 조건부 확률 기반 분류."

    def __init__(self) -> None:
        self._model = GaussianNB()

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class PCAKMeansStrategy(RoseModelStrategy):
    @property
    def name(self) -> str:
        return "PCA+KMeans"

    @property
    def description(self) -> str:
        return "PCA 차원 축소 후 K-Means 군집화."

    def __init__(self, n_components: int = 2, n_clusters: int = 2) -> None:
        self._scaler = StandardScaler()
        self._pca = PCA(n_components=n_components)
        self._kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self._cluster_to_label: dict[int, int] = {}

    def fit(self, X, y) -> None:
        import numpy as np

        X_reduced = self._pca.fit_transform(self._scaler.fit_transform(X))
        self._kmeans.fit(X_reduced)
        y_arr = np.array(y)
        for cluster in range(self._kmeans.n_clusters):
            mask = self._kmeans.labels_ == cluster
            rate = float(y_arr[mask].mean()) if mask.sum() > 0 else 0.0
            self._cluster_to_label[cluster] = 1 if rate >= 0.5 else 0

    def predict(self, X) -> list[int]:
        X_reduced = self._pca.transform(self._scaler.transform(X))
        return [self._cluster_to_label.get(int(cluster), 0) for cluster in self._kmeans.predict(X_reduced)]

    def predict_proba(self, X) -> list[float]:
        return [float(value) for value in self.predict(X)]


def build_all_strategies() -> dict[str, type[RoseModelStrategy]]:
    return {
        "xgboost": XGBoostStrategy,
        "random_forest": RandomForestStrategy,
        "lightgbm": LightGBMStrategy,
        "catboost": CatBoostStrategy,
        "logistic_regression": LogisticRegressionStrategy,
        "decision_tree": DecisionTreeStrategy,
        "svm": SVMStrategy,
        "knn": KNNStrategy,
        "naive_bayes": NaiveBayesStrategy,
        "pca_kmeans": PCAKMeansStrategy,
    }
