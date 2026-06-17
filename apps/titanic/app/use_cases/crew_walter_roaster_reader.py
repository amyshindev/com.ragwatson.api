from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

_DATA_PATHS = [
    Path(__file__).resolve().parent / "Titanic-Dataset.csv",
    Path(__file__).resolve().parent.parent / "Titanic-Dataset.csv",
]


class WalterReader:
    def __init__(self) -> None:
        self._df = self._load_dataset()

    def _load_dataset(self) -> pd.DataFrame:
        for path in _DATA_PATHS:
            if path.is_file():
                return self._normalize_columns(pd.read_csv(path))
        return pd.DataFrame()

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        rename_map = {
            "passenger_id": "PassengerId",
            "survived": "Survived",
            "pclass": "Pclass",
            "gender": "Sex",
            "age": "Age",
            "sibsp": "SibSp",
            "parch": "Parch",
            "fare": "Fare",
        }
        normalized = df.rename(columns={key: value for key, value in rename_map.items() if key in df.columns})
        if "Sex" not in normalized.columns and "gender" in df.columns:
            normalized["Sex"] = df["gender"]
        return normalized

    def get_data(self) -> pd.DataFrame:
        if self._df.empty:
            return self._df
        return self._df.head(1)

    def get_count(self) -> int:
        return len(self._df)

    def get_dataset(self) -> pd.DataFrame:
        return self._df.copy()

    def get_features_and_labels(self) -> tuple[pd.DataFrame, pd.Series]:
        if self._df.empty or "Survived" not in self._df.columns:
            return pd.DataFrame(), pd.Series(dtype=int)

        features = self._build_features(self._df)
        labels = pd.to_numeric(self._df["Survived"], errors="coerce").fillna(0).astype(int)
        return features, labels

    def preprocess_single_passenger(self, passenger: dict[str, Any]) -> pd.DataFrame:
        row = pd.DataFrame(
            [
                {
                    "Pclass": passenger.get("Pclass", 3),
                    "Sex": passenger.get("Sex", "male"),
                    "Age": passenger.get("Age", 30.0),
                    "SibSp": passenger.get("SibSp", 0),
                    "Parch": passenger.get("Parch", 0),
                    "Fare": passenger.get("Fare", 0.0),
                }
            ]
        )
        return self._build_features(row)

    def _build_features(self, df: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame()
        features["Pclass"] = pd.to_numeric(df.get("Pclass", 3), errors="coerce").fillna(3)
        sex = df.get("Sex", "male")
        if isinstance(sex, pd.Series):
            features["Sex"] = sex.astype(str).str.lower().map({"male": 0, "female": 1}).fillna(0)
        else:
            features["Sex"] = 0 if str(sex).lower() == "male" else 1
        features["Age"] = pd.to_numeric(df.get("Age", 30), errors="coerce").fillna(30)
        features["SibSp"] = pd.to_numeric(df.get("SibSp", 0), errors="coerce").fillna(0)
        features["Parch"] = pd.to_numeric(df.get("Parch", 0), errors="coerce").fillna(0)
        features["Fare"] = pd.to_numeric(df.get("Fare", 0), errors="coerce").fillna(0)
        return features
