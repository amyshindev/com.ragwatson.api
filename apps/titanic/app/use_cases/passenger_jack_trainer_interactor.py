from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from kiwipiepy import Kiwi
from sklearn.model_selection import train_test_split

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort
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

    def __init__(self, repository: JackTrainerPort):
        self.repository = repository
        self.kiwi = Kiwi()

    def _resolve_training_data(self, train_set: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        if not train_set.empty and "Survived" in train_set.columns:
            reader = WalterReader()
            features = reader._build_features(train_set)
            labels = pd.to_numeric(train_set["Survived"], errors="coerce").fillna(0).astype(int)
            return features, labels

        reader = WalterReader()
        return reader.get_features_and_labels()

    async def get_model_train(self, train_set: pd.DataFrame) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")

        features, labels = self._resolve_training_data(train_set)
        if features.empty or labels.empty:
            raise RuntimeError("훈련 데이터가 비어 있습니다.")

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

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name,
        ))


PassengerJackTrainerInteractor = JackTrainerInteractor
