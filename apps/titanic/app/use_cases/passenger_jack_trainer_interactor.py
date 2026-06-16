from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from kiwipiepy import Kiwi
from sklearn.model_selection import train_test_split

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository
from titanic.app.use_cases.crew_walter_roaster_reader import WalterReader
from titanic.app.use_cases.passenger_rose_model_interactor import (
    ROSE_SUGGESTED_ALGORITHMS,
    RoseModelInteractor,
)


logger = logging.getLogger(__name__)


class JackTrainingBundle:
    '''잭 훈련 결과 — 캘 테스터가 hold-out 테스트·순위 산출에 사용'''

    models: dict[str, RoseModelInteractor] = {}
    train_features: pd.DataFrame | None = None
    train_labels: pd.Series | None = None
    test_features: pd.DataFrame | None = None
    test_labels: pd.Series | None = None


TRAINING_BUNDLE = JackTrainingBundle()


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository
        self.kiwi = Kiwi()

    def _resolve_training_data(self) -> tuple[pd.DataFrame, pd.Series]:
        reader = WalterReader()
        features, labels = reader.get_features_and_labels()

        if features.empty or labels.empty:
            features = pd.DataFrame(
                {
                    "Pclass": [1, 3, 3, 1, 1, 3, 3, 1],
                    "Sex": [1, 0, 0, 1, 1, 0, 0, 1],
                    "Age": [28, 20, 22, 35, 30, 19, 24, 40],
                    "SibSp": [0, 0, 1, 1, 0, 1, 0, 1],
                    "Parch": [0, 0, 0, 1, 0, 0, 1, 0],
                    "Fare": [80.0, 7.0, 9.0, 55.0, 60.0, 8.0, 10.0, 50.0],
                }
            )
            labels = pd.Series([1, 0, 0, 1, 1, 0, 0, 1])

        return features, labels

    async def get_model_train(self) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''

        features, labels = self._resolve_training_data()
        x_train, x_test, y_train, y_test = train_test_split(
            features,
            labels,
            test_size=0.2,
            random_state=42,
            stratify=labels,
        )

        bundle = TRAINING_BUNDLE
        bundle.train_features = x_train
        bundle.train_labels = y_train
        bundle.test_features = x_test
        bundle.test_labels = y_test
        bundle.models.clear()

        train_results: list[dict[str, Any]] = []

        for algorithm in ROSE_SUGGESTED_ALGORITHMS:
            rose = RoseModelInteractor(algorithm=algorithm)
            rose.train(x_train, y_train)
            bundle.models[algorithm.value] = rose
            train_results.append({
                "algorithm": algorithm.value,
                "model_name": rose.get_model_name(),
                "scaling": rose._strategy.scaling,
                "train_accuracy": rose.get_accuracy(x_train, y_train),
            })
            logger.info(
                "[JackTrainerInteractor] trained | %s | train_accuracy=%.4f",
                algorithm.value,
                train_results[-1]["train_accuracy"],
            )

        return {
            "role": "jack_trainer",
            "action": "train",
            "sample_count_train": len(x_train),
            "sample_count_test": len(x_test),
            "feature_columns": list(features.columns),
            "target_name": "Survived",
            "trained_models": list(bundle.models.keys()),
            "train_results": train_results,
        }

    async def analyze_message_intent(self, user_message: str) -> dict:
        '''사용자의 질문(message)을 형태소 분석하여 키워드와 의도를 파악한다'''

        logger.info("[JackTrainerInteractor] 전처리 및 분석 시작 | message: %s", user_message)

        tokens = self.kiwi.tokenize(user_message)

        keywords: list[str] = []
        has_quantity_modifier = False
        has_count_unit = False

        for t in tokens:
            if t.tag in ("NNG", "NNP"):
                keywords.append(t.form)

            if t.tag == "MM" and t.form == "몇":
                has_quantity_modifier = True

            if t.tag == "NNB" and t.form in ("명", "개", "사람", "분"):
                has_count_unit = True

        is_count_query = has_quantity_modifier or has_count_unit or ("몇" in user_message)

        analysis_result = {
            "keywords": keywords,
            "is_count_query": is_count_query,
        }

        logger.info("[JackTrainerInteractor] 분석 완료 | 결과: %s", analysis_result)
        return analysis_result

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터랙트'''

        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name,
        ))

    def train_rose_model(self, rose_model: RoseModelInteractor) -> tuple[str, float | None]:
        '''로즈(모델)를 학습시키는 잭의 역할'''

        features, labels = self._resolve_training_data()

        rose_model.train(features, labels)
        return (
            rose_model.get_model_name(),
            rose_model.get_accuracy(features, labels),
        )


PassengerJackTrainerInteractor = JackTrainerInteractor
