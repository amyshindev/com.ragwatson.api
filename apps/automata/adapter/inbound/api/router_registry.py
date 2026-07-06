from fastapi import APIRouter

from automata.adapter.inbound.api.v1.address_book_router import address_book_router
from automata.adapter.inbound.api.v1.faker_mailer_router import faker_mailer_router
from automata.adapter.inbound.api.v1.ford_director_router import ford_director_router
from automata.adapter.inbound.api.v1.inbound_mailer_router import inbound_mailer_router

automata_router = APIRouter()
automata_router.include_router(ford_director_router)
automata_router.include_router(faker_mailer_router)
automata_router.include_router(address_book_router)
automata_router.include_router(inbound_mailer_router)

__all__ = ["automata_router"]
