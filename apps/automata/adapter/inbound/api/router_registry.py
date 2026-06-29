from fastapi import APIRouter

from automata.adapter.inbound.api.v1.faker_mailer_router import faker_mailer_router
from automata.adapter.inbound.api.v1.ford_director_router import ford_director_router

automata_router = APIRouter()
automata_router.include_router(ford_director_router)
automata_router.include_router(faker_mailer_router)

__all__ = ["automata_router"]
