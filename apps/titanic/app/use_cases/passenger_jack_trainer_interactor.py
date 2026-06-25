from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.adapter.outbound.orm.passenger_rose_model_strategies import (
    RoseModelStrategy,
    build_all_strategies,
)
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort

logger = logging.getLogger(__name__)

_ML_COLUMN_MAP = {
    "PassengerId": "passenger_id",
    "Survived": "survived",
    "Pclass": "pclass",
    "Name": "name",
    "Sex": "gender",
    "Age": "age",
    "SibSp": "sibsp",
    "Parch": "parch",
    "Ticket": "ticket",
    "Fare": "fare",
    "Cabin": "cabin",
    "Embarked": "embarked",
}


def _normalize_train_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.rename(
        columns={
            source: target for source, target in _ML_COLUMN_MAP.items() if source in df.columns
        }
    )
    if "gender" not in normalized.columns and "Sex" in df.columns:
        normalized["gender"] = df["Sex"]
    if "survived" not in normalized.columns and "Survived" in df.columns:
        normalized["survived"] = df["Survived"]
    if "name" not in normalized.columns and "Name" in df.columns:
        normalized["name"] = df["Name"]
    return normalized


def _preprocess_train(df: pd.DataFrame) -> tuple[list[list[float]], list[int]]:
    """잭 학습용 피처 전처리. survived 라벨을 분리해 X, y를 반환한다."""
    frame = df.copy()

    y_label = frame["survived"].astype(int).tolist()
    frame = frame.drop("survived", axis=1)

    frame["Title"] = frame["name"].str.extract(r"([A-Za-z]+)\.", expand=False)
    frame["Title"] = frame["Title"].replace(
        ["Capt", "Col", "Don", "Dr", "Major", "Rev", "Jonkheer", "Dona", "Mme"], "Rare"
    )
    frame["Title"] = frame["Title"].replace(["Countess", "Lady", "Sir"], "Royal")
    frame["Title"] = frame["Title"].replace({"Mlle": "Mr", "Ms": "Miss"})
    title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6}
    frame["Title"] = frame["Title"].map(title_mapping).fillna(0).astype(int)

    frame["gender"] = frame["gender"].astype(str).str.lower().map({"male": 0, "female": 1})

    bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
    age_labels = [
        "Unknown",
        "Baby",
        "Child",
        "Teenager",
        "Student",
        "Young Adult",
        "Adult",
        "Senior",
    ]
    age_title_mapping = {
        0: "Unknown",
        1: "Baby",
        2: "Child",
        3: "Teenager",
        4: "Student",
        5: "Young Adult",
        6: "Adult",
        7: "Senior",
    }
    age_mapping = {label: code for code, label in age_title_mapping.items()}

    frame["age"] = pd.to_numeric(frame["age"], errors="coerce").fillna(-0.5)
    frame["AgeGroup"] = pd.cut(frame["age"], bins, labels=age_labels).astype(str)
    unknown_mask = frame["AgeGroup"] == "Unknown"
    frame.loc[unknown_mask, "AgeGroup"] = frame.loc[unknown_mask, "Title"].map(age_title_mapping)
    frame["AgeGroup"] = frame["AgeGroup"].map(age_mapping).fillna(0).astype(int)

    frame["embarked"] = frame["embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3})

    frame["fare"] = pd.to_numeric(frame["fare"], errors="coerce").fillna(0)
    frame["FareBand"] = (
        pd.qcut(frame["fare"], 4, labels=[1, 2, 3, 4], duplicates="drop").fillna(1).astype(int)
    )

    drop_cols = ["name", "age", "fare", "ticket", "cabin", "passenger_id"]
    frame = frame.drop(columns=[column for column in drop_cols if column in frame.columns])

    return frame.values.tolist(), y_label


class JackTrainerInteractor(JackTrainerUseCase):
    def __init__(self, repository: JackTrainerPort):
        self.repository = repository

    async def get_model_train(self, train_set: pd.DataFrame) -> dict[str, Any]:
        """로즈가 제안한 모델들을 훈련시키는 메소드"""
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")

        normalized = _normalize_train_columns(train_set.copy())
        if normalized.empty or "survived" not in normalized.columns:
            raise RuntimeError("훈련 데이터가 비어 있거나 Survived 컬럼이 없습니다.")

        x_train, y_label = _preprocess_train(normalized)
        if not x_train:
            raise RuntimeError("피처 전처리 결과가 비어 있습니다.")

        trained_strategies: dict[str, RoseModelStrategy] = {}
        trained_names: list[str] = []
        train_results: list[dict[str, Any]] = []
        for key, strategy_class in build_all_strategies().items():
            strategy = strategy_class()
            try:
                strategy.fit(x_train, y_label)
                trained_strategies[key] = strategy
                trained_names.append(strategy.name)
                predictions = strategy.predict(x_train)
                train_accuracy = sum(
                    pred == label for pred, label in zip(predictions, y_label, strict=True)
                ) / len(y_label)
                train_results.append(
                    {
                        "algorithm": key,
                        "model_name": strategy.name,
                        "train_accuracy": train_accuracy,
                    }
                )
                logger.info(
                    "[JackTrainerInteractor] %s 학습 완료 | train_accuracy=%.4f",
                    strategy.name,
                    train_accuracy,
                )
            except Exception as error:
                logger.warning("[JackTrainerInteractor] %s 학습 실패 | error=%s", key, error)

        return {
            "role": "jack_trainer",
            "action": "train",
            "train_samples": len(x_train),
            "sample_count_train": len(x_train),
            "trained_models": trained_names,
            "trained_strategies": trained_strategies,
            "train_results": train_results,
        }

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        """잭 트레이너의 자기소개 인터렉트"""
        return await self.repository.introduce_myself(
            JackTrainerQuery(
                id=schema.id,
                name=schema.name,
            )
        )


PassengerJackTrainerInteractor = JackTrainerInteractor
