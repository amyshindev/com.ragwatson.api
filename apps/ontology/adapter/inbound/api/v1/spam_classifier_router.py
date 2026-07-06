import logging

from fastapi import APIRouter, Depends

from ontology.adapter.inbound.api.schemas.spam_classifier_schema import (
    ClassifyEmailRequestSchema,
    ClassifyEmailResponseSchema,
)
from ontology.app.ports.input.spam_classifier_use_case import SpamClassifierUseCase
from ontology.dependencies.spam_classifier_provider import get_spam_classifier_use_case

logger = logging.getLogger(__name__)

spam_classifier_router = APIRouter(prefix="/ontology/spam", tags=["ontology", "spam"])


@spam_classifier_router.post("/classify", response_model=ClassifyEmailResponseSchema)
async def classify_email(
    body: ClassifyEmailRequestSchema,
    classifier: SpamClassifierUseCase = Depends(get_spam_classifier_use_case),
) -> ClassifyEmailResponseSchema:
    return await classifier.classify(body)


@spam_classifier_router.get("/myself")
async def introduce_myself() -> dict[str, str]:
    return {
        "name": "Ontology Spam Classifier",
        "role": "이메일 스팸·피싱·프로모 온톨로지 분류",
    }
