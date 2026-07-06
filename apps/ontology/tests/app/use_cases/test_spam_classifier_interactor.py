"""Tests for spam classifier interactor."""

import pytest

from ontology.adapter.inbound.api.schemas.spam_classifier_schema import ClassifyEmailRequestSchema
from ontology.adapter.outbound.memory.spam_ontology_memory_repository import (
    SpamOntologyMemoryRepository,
)
from ontology.app.use_cases.spam_classifier_interactor import SpamClassifierInteractor


@pytest.mark.asyncio
async def test_classify_spam_email() -> None:
    interactor = SpamClassifierInteractor(ontology=SpamOntologyMemoryRepository())
    result = await interactor.classify(
        ClassifyEmailRequestSchema(
            sender="spam@example.com",
            subject="You won the lottery!!!",
            body="Claim your free money now. lottery winner!",
        ),
    )
    assert result.is_blocked
    assert result.label in {"spam", "phishing", "promo"}
