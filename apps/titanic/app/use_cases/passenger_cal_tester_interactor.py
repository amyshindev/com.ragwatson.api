from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.adapter.outbound.orm.passenger_rose_model_strategies import RoseModelStrategy
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_port import CalTesterPort

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


class CalTesterInteractor(CalTesterUseCase):
    def __init__(self, repository: CalTesterPort):
        self.repository = repository

    async def get_model_test(self, test_set: dict[str, Any]) -> CalTesterResponse:
        """로즈가 제안한 10개 모델의 트레이닝 정도를 점수화해서 최고 성능 모델을 뽑는 메소드

        Args:
            test_set: {
                "df": pd.DataFrame,  # Survived/survived 라벨 포함
                "trained_strategies": dict[str, RoseModelStrategy],  # Jack이 학습시킨 모델들
            }
        """
        logger.info("[CalTesterInteractor] 모델 채점 시작")

        trained_strategies: dict[str, RoseModelStrategy] = test_set["trained_strategies"]
        if not trained_strategies:
            raise RuntimeError("훈련된 모델이 없습니다.")

        x_test, y_test = _preprocess_test(test_set["df"])
        if not x_test or not y_test:
            raise RuntimeError("채점용 테스트 피처가 비어 있습니다.")

        scored: list[dict[str, Any]] = []
        for algorithm_key, strategy in trained_strategies.items():
            try:
                predictions = strategy.predict(x_test)
                correct = sum(
                    prediction == label
                    for prediction, label in zip(predictions, y_test, strict=True)
                )
                test_accuracy = correct / len(y_test)
                scored.append(
                    {
                        "algorithm": algorithm_key,
                        "model_name": strategy.name,
                        "test_accuracy": test_accuracy,
                    }
                )
                logger.info(
                    "[CalTesterInteractor] %s | test_accuracy=%.4f",
                    strategy.name,
                    test_accuracy,
                )
            except Exception as error:
                logger.warning(
                    "[CalTesterInteractor] %s 채점 실패 | error=%s", algorithm_key, error
                )
                scored.append(
                    {
                        "algorithm": algorithm_key,
                        "model_name": algorithm_key,
                        "test_accuracy": -1.0,
                        "error": str(error),
                    }
                )

        scored.sort(key=lambda row: row["test_accuracy"], reverse=True)

        rankings: list[dict[str, Any]] = []
        for index, row in enumerate(scored, start=1):
            rankings.append(
                {
                    "rank": index,
                    **row,
                }
            )

        best = rankings[0]
        return {
            "role": "cal_tester",
            "action": "test",
            "sample_count_test": len(x_test),
            "sample_features": x_test[:1],
            "rankings": rankings,
            "best_rank": best["rank"],
            "best_algorithm": best["algorithm"],
            "best_model_name": best["model_name"],
            "best_test_accuracy": best["test_accuracy"],
        }

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        """칼 테스터의 자기소개 인터랙트"""

        return await self.repository.introduce_myself(
            CalTesterQuery(
                id=schema.id,
                name=schema.name,
            )
        )


def _normalize_test_columns(df: pd.DataFrame) -> pd.DataFrame:
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


def _preprocess_test(df: pd.DataFrame) -> tuple[list[list[float]], list[int]]:
    """캘 테스트용 피처 전처리. Jack 학습과 동일한 변환을 독립 적용한다."""
    frame = _normalize_test_columns(df.copy())

    y_test = frame["survived"].astype(int).tolist()
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

    return frame.values.tolist(), y_test


PassengerCalTesterInteractor = CalTesterInteractor
