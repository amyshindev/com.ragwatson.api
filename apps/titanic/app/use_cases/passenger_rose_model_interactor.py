from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository


class RoseModelInteractor(RoseModelUseCase):
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        if self.repository is None:
            return RoseModelResponse(id=schema.id, name=schema.name)

        return await self.repository.introduce_myself(RoseModelQuery(
            id=schema.id,
            name=schema.name,
        ))



    def __init__(self, repository: RoseModelRepository | None = None) -> None:
        self.repository = repository
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


PassengerRoseModelInteractor = RoseModelInteractor
RoseModelTrainInteractor = RoseModelInteractor
