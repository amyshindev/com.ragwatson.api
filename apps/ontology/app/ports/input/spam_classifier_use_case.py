from __future__ import annotations

from abc import ABC, abstractmethod

from ontology.adapter.inbound.api.schemas.spam_classifier_schema import (
    ClassifyEmailRequestSchema,
    ClassifyEmailResponseSchema,
)


class SpamClassifierUseCase(ABC):
    @abstractmethod
    async def classify(self, schema: ClassifyEmailRequestSchema) -> ClassifyEmailResponseSchema:
        pass
