from fastapi import Depends

from core.graph.neo4j_driver import is_neo4j_configured
from ontology.adapter.outbound.memory.spam_ontology_memory_repository import (
    SpamOntologyMemoryRepository,
)
from ontology.adapter.outbound.neo4j.spam_ontology_neo4j_repository import (
    SpamOntologyNeo4jRepository,
)
from ontology.app.ports.input.spam_classifier_use_case import SpamClassifierUseCase
from ontology.app.ports.output.spam_ontology_port import SpamOntologyPort
from ontology.app.use_cases.spam_classifier_interactor import SpamClassifierInteractor


def get_spam_ontology_repository() -> SpamOntologyPort:
    memory = SpamOntologyMemoryRepository()
    if is_neo4j_configured():
        return SpamOntologyNeo4jRepository(fallback=memory)
    return memory


def get_spam_classifier_use_case(
    ontology: SpamOntologyPort = Depends(get_spam_ontology_repository),
) -> SpamClassifierUseCase:
    return SpamClassifierInteractor(ontology=ontology)
