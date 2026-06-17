from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatSchema,
    SmithCaptainSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import (
    ChatResponse,
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort
from titanic.app.use_cases.passenger_jack_trainer_interactor import TRAINING_BUNDLE
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor


logger = logging.getLogger(__name__)


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
        self,
        repository: SmithCaptainPort,
        andrews: AndrewsArchitectUseCase,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTesterUseCase,
        walter: WalterRoasterUseCase,
    ):
        self.repository = repository
        self.andrews = andrews
        self.jack = jack
        self.rose = rose
        self.cal = cal
        self.walter = walter

    def _equip_rose_with_best_model(self, algorithm_key: str) -> RoseModelInteractor:
        source = TRAINING_BUNDLE.models[algorithm_key]
        self.rose.set_algorithm(algorithm_key)
        self.rose.model = source.model
        self.rose._scaler = source._scaler
        return self.rose

    def _build_reply(
        self,
        intent: str,
        question: dict[str, Any],
        train_set: pd.DataFrame,
        train_result: dict[str, Any],
        test_result: dict[str, Any],
        best_model_name: str,
        best_accuracy: float,
    ) -> str:
        if intent == "STATISTICS":
            return f"탑승객은 {len(train_set)}명입니다. (학습 데이터 기준)"

        if intent == "MODEL_TRAIN":
            trained_count = len(train_result.get("train_results", []))
            return (
                f"잭이 {trained_count}개 모델을 훈련했습니다. "
                f"캘 테스터 결과 {best_model_name}이(가) test 정확도 {best_accuracy:.2%}로 1위입니다."
            )

        if intent == "SURVIVAL_PREDICT":
            bundle = TRAINING_BUNDLE
            if bundle.test_features is not None and not bundle.test_features.empty:
                sample = bundle.test_features.head(1)
                prediction = int(self.rose.predict(sample)[0])
                survived = "생존" if prediction == 1 else "사망"
                return (
                    f"로즈({best_model_name}) 예측: 해당 승객은 {survived}할 것으로 보입니다. "
                    f"(test 정확도 {best_accuracy:.2%})"
                )
            return f"예측할 승객 데이터가 없습니다. (모델: {best_model_name})"

        if intent == "PASSENGER_SEARCH":
            keywords = question.get("keywords", [])
            keyword_text = ", ".join(keywords) if keywords else "없음"
            return (
                f"검색 키워드: {keyword_text}. "
                f"현재 최적 모델은 {best_model_name} (test 정확도 {best_accuracy:.2%})입니다."
            )

        return (
            f"선장 스미스입니다. 로즈에게 장착된 최고 모델은 {best_model_name} "
            f"(test 정확도 {best_accuracy:.2%})입니다."
        )

    async def chat(self, schema: ChatSchema) -> ChatResponse:
        logger.info("[SmithCaptainInteractor] chat 진입 | message=%s", schema.message)

        train_set = self.walter.get_train_set()
        test_set = self.walter.get_test_set()
        train_result = await self.jack.get_model_train(train_set)
        test_result = await self.cal.get_model_test(test_set)
        question = self.andrews.analyze_intent(schema.message)

        best_algorithm = test_result["best_algorithm"]
        best_accuracy = float(test_result["best_test_accuracy"])
        best_model_name = test_result["best_model_name"]
        self._equip_rose_with_best_model(best_algorithm)

        reply = self._build_reply(
            intent=question["intent"],
            question=question,
            train_set=train_set,
            train_result=train_result,
            test_result=test_result,
            best_model_name=best_model_name,
            best_accuracy=best_accuracy,
        )

        logger.info(
            "[SmithCaptainInteractor] chat 완료 | intent=%s algorithm=%s accuracy=%.4f",
            question["intent"],
            best_algorithm,
            best_accuracy,
        )
        return ChatResponse(reply=reply, accuracy=best_accuracy)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))


CrewSmithCaptainInteractor = SmithCaptainInteractor
