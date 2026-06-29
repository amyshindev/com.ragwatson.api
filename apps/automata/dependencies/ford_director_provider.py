import os

from fastapi import Depends

from automata.adapter.outbound.n8n.ford_director_n8n_repository import FordDirectorN8nRepository
from automata.app.ports.input.ford_director_use_case import FordDirectorUseCase
from automata.app.ports.output.ford_director_port import FordDirectorPort
from automata.app.use_cases.ford_director_interactor import FordDirectorInteractor


def _n8n_webhook_url() -> str:
    return os.getenv("N8N_WEBHOOK_URL", "http://127.0.0.1:5678/webhook/automata").strip()


def get_ford_director_repository() -> FordDirectorPort:
    return FordDirectorN8nRepository(webhook_url=_n8n_webhook_url())


def get_ford_director_use_case(
    repository: FordDirectorPort = Depends(get_ford_director_repository),
) -> FordDirectorUseCase:
    return FordDirectorInteractor(repository=repository)
