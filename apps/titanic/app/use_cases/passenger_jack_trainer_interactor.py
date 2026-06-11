from __future__ import annotations

import pandas as pd

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository
from titanic.app.use_cases.crew_walter_roaster_reader import WalterReader
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository | None = None):
        self.repository = repository

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터랙트'''

        if self.repository is None:
            return JackTrainerResponse(id=schema.id, name=schema.name)

        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name,
        ))

    def train_rose_model(self, rose_model: RoseModelInteractor) -> tuple[str, float | None]:
        '''로즈(모델)를 학습시키는 잭의 역할'''

        reader = WalterReader()
        features, labels = reader.get_features_and_labels()

        if features.empty or labels.empty:
            features = pd.DataFrame(
                {
                    "Pclass": [1, 3, 3, 1],
                    "Sex": [1, 0, 0, 1],
                    "Age": [28, 20, 22, 35],
                    "SibSp": [0, 0, 1, 1],
                    "Parch": [0, 0, 0, 1],
                    "Fare": [80.0, 7.0, 9.0, 55.0],
                }
            )
            labels = pd.Series([1, 0, 0, 1])

        rose_model.train(features, labels)
        return (
            rose_model.get_model_name(),
            rose_model.get_accuracy(features, labels),
        )


PassengerJackTrainerInteractor = JackTrainerInteractor
