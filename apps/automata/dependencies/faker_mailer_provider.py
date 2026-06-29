from fastapi import Depends

from automata.adapter.outbound.n8n.faker_mailer_n8n_repository import FakerMailerN8nRepository
from automata.app.ports.input.faker_mailer_use_case import FakerMailerUseCase
from automata.app.ports.output.faker_mailer_port import FakerMailerPort
from automata.app.use_cases.faker_mailer_interactor import FakerMailerInteractor
from automata.dependencies.ford_director_provider import _n8n_webhook_url
from core.lol.t1_mid_faker_orchestrator import (
    T1MidFakerOrchestrator,
    register_exaone_orchestrator,
)

_faker_singleton: T1MidFakerOrchestrator | None = None


def _get_faker_orchestrator() -> T1MidFakerOrchestrator:
    global _faker_singleton
    if _faker_singleton is None:
        _faker_singleton = register_exaone_orchestrator()
    return _faker_singleton


def get_faker_mailer_repository() -> FakerMailerPort:
    return FakerMailerN8nRepository(webhook_url=_n8n_webhook_url())


def get_faker_mailer_use_case(
    repository: FakerMailerPort = Depends(get_faker_mailer_repository),
    faker: T1MidFakerOrchestrator = Depends(_get_faker_orchestrator),
) -> FakerMailerUseCase:
    return FakerMailerInteractor(repository=repository, faker=faker)
