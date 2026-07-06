from __future__ import annotations

import logging

from ontology.adapter.inbound.api.schemas.spam_classifier_schema import (
    ClassifyEmailRequestSchema,
    ClassifyEmailResponseSchema,
)
from ontology.app.ports.input.spam_classifier_use_case import SpamClassifierUseCase
from ontology.app.ports.output.spam_ontology_port import SpamOntologyPort
from ontology.domain.entities.email_signal import EmailSignal
from ontology.domain.services.spam_heuristics import classify_with_heuristics

logger = logging.getLogger(__name__)


class SpamClassifierInteractor(SpamClassifierUseCase):
    def __init__(self, ontology: SpamOntologyPort) -> None:
        self._ontology = ontology

    async def classify(self, schema: ClassifyEmailRequestSchema) -> ClassifyEmailResponseSchema:
        signal = EmailSignal(
            sender=schema.sender,
            subject=schema.subject,
            body=schema.body,
        )
        base = classify_with_heuristics(signal)
        verdict = await self._ontology.enrich_verdict(signal, base)
        logger.info(
            "[SpamClassifierInteractor] label=%s score=%.2f blocked=%s",
            verdict.label,
            verdict.score,
            verdict.is_blocked,
        )
        return ClassifyEmailResponseSchema(
            label=verdict.label.value,
            score=verdict.score,
            is_blocked=verdict.is_blocked,
            reasons=list(verdict.reasons),
            matched_concepts=list(verdict.matched_concepts),
            source=self._ontology.__class__.__name__,
        )
