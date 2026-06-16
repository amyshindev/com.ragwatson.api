from __future__ import annotations

from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository
from titanic.app.use_cases.passenger_jack_trainer_interactor import TRAINING_BUNDLE


class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTesterRepository):
        self.repository = repository

    async def get_model_test(self, test_set) -> CalTesterResponse:
        '''로즈가 제안한 10개 모델의 트레이닝 정도를 점수화해서 최고 성능 모델을 뽑는 메소드'''

        bundle = TRAINING_BUNDLE

        if not bundle.models:
            raise RuntimeError("훈련된 모델이 없습니다. JackTrainerInteractor.get_model_train()을 먼저 실행하세요.")
        if bundle.test_features is None or bundle.test_labels is None:
            raise RuntimeError("테스트 데이터가 없습니다. JackTrainerInteractor.get_model_train()을 먼저 실행하세요.")

        scored: list[dict[str, Any]] = []
        for algorithm_key, rose in bundle.models.items():
            test_accuracy = rose.get_accuracy(bundle.test_features, bundle.test_labels)
            scored.append({
                "algorithm": algorithm_key,
                "model_name": rose.get_model_name(),
                "scaling": rose._strategy.scaling,
                "test_accuracy": test_accuracy,
            })

        scored.sort(key=lambda row: row["test_accuracy"], reverse=True)

        rankings: list[dict[str, Any]] = []
        for index, row in enumerate(scored, start=1):
            rankings.append({
                "rank": index,
                **row,
            })

        best = rankings[0]
        return {
            "role": "cal_tester",
            "action": "test",
            "sample_count_test": len(bundle.test_features),
            "rankings": rankings,
            "best_rank": best["rank"],
            "best_algorithm": best["algorithm"],
            "best_model_name": best["model_name"],
            "best_test_accuracy": best["test_accuracy"],
        }

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 테스터의 자기소개 인터랙트'''

        return await self.repository.introduce_myself(CalTesterQuery(
            id=schema.id,
            name=schema.name,
        ))


PassengerCalTesterInteractor = CalTesterInteractor
