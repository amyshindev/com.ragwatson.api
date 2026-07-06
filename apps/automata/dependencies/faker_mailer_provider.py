from fastapi import Depends

from automata.adapter.outbound.n8n.faker_mailer_n8n_repository import FakerMailerN8nRepository
from automata.adapter.outbound.ontology.spam_guard_ontology_adapter import SpamGuardOntologyAdapter
from automata.app.ports.input.faker_mailer_use_case import FakerMailerUseCase
from automata.app.ports.output.faker_mailer_port import FakerMailerPort
from automata.app.ports.output.spam_guard_port import SpamGuardPort
from automata.app.use_cases.faker_mailer_interactor import FakerMailerInteractor
from automata.dependencies.ford_director_provider import _n8n_webhook_url
from core.lol.t1_mid_faker_orchestrator import (
    T1MidFakerOrchestrator,
    register_exaone_orchestrator,
)
from ontology.app.ports.output.spam_ontology_port import SpamOntologyPort
from ontology.app.use_cases.spam_classifier_interactor import SpamClassifierInteractor
from ontology.dependencies.spam_classifier_provider import get_spam_ontology_repository

_faker_singleton: T1MidFakerOrchestrator | None = None


def _get_faker_orchestrator() -> T1MidFakerOrchestrator:
    global _faker_singleton
    if _faker_singleton is None:
        _faker_singleton = register_exaone_orchestrator()
    return _faker_singleton


def get_faker_mailer_repository() -> FakerMailerPort:
    return FakerMailerN8nRepository(webhook_url=_n8n_webhook_url())


def get_spam_guard_port(
    ontology: SpamOntologyPort = Depends(get_spam_ontology_repository),
) -> SpamGuardPort:
    classifier = SpamClassifierInteractor(ontology=ontology)
    return SpamGuardOntologyAdapter(classifier=classifier)


def get_faker_mailer_use_case(
    repository: FakerMailerPort = Depends(get_faker_mailer_repository),
    faker: T1MidFakerOrchestrator = Depends(_get_faker_orchestrator),
    spam_guard: SpamGuardPort = Depends(get_spam_guard_port),
) -> FakerMailerUseCase:
    return FakerMailerInteractor(
        repository=repository,
        faker=faker,
        spam_guard=spam_guard,
    )
