from fastapi import APIRouter

from ontology.adapter.inbound.api.v1.spam_classifier_router import spam_classifier_router

ontology_router = APIRouter()
ontology_router.include_router(spam_classifier_router)

__all__ = ["ontology_router"]
