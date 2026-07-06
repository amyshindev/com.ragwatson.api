from __future__ import annotations

from automata.app.ports.output.spam_guard_port import SpamGuardPort, SpamGuardVerdict
from ontology.adapter.inbound.api.schemas.spam_classifier_schema import ClassifyEmailRequestSchema
from ontology.app.ports.input.spam_classifier_use_case import SpamClassifierUseCase


class SpamGuardOntologyAdapter(SpamGuardPort):
    def __init__(self, classifier: SpamClassifierUseCase) -> None:
        self._classifier = classifier

    async def classify(self, *, sender: str | None, subject: str, body: str) -> SpamGuardVerdict:
        result = await self._classifier.classify(
            ClassifyEmailRequestSchema(sender=sender, subject=subject, body=body),
        )
        return SpamGuardVerdict(
            label=result.label,
            score=result.score,
            is_blocked=result.is_blocked,
            reasons=tuple(result.reasons),
        )
