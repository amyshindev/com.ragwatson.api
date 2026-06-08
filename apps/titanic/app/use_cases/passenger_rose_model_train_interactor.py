import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


class RoseModelTrainInteractor:
    def __init__(self) -> None:
        self.model = DecisionTreeClassifier(random_state=42, max_depth=5)

    def get_model_name(self) -> str:
        return type(self.model).__name__

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return np.asarray(self.model.predict(X))

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        return np.asarray(self.model.predict_proba(X))

    def get_accuracy(self, X: pd.DataFrame, y: pd.Series) -> float:
        return float(self.model.score(X, y))
