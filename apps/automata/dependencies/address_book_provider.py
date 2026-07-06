from automata.adapter.outbound.memory.address_book_memory_repository import (
    AddressBookMemoryRepository,
)
from automata.adapter.outbound.neo4j.address_book_neo4j_repository import (
    AddressBookNeo4jRepository,
)
from automata.app.ports.input.address_book_use_case import AddressBookUseCase
from automata.app.ports.output.address_book_port import AddressBookPort
from automata.app.use_cases.address_book_interactor import AddressBookInteractor
from core.graph.neo4j_driver import get_neo4j_driver

_memory_singleton: AddressBookMemoryRepository | None = None
_repository_singleton: AddressBookPort | None = None


def _get_memory_repository() -> AddressBookMemoryRepository:
    global _memory_singleton
    if _memory_singleton is None:
        _memory_singleton = AddressBookMemoryRepository()
    return _memory_singleton


def get_address_book_repository() -> AddressBookPort:
    global _repository_singleton
    if _repository_singleton is not None:
        return _repository_singleton

    memory = _get_memory_repository()
    if get_neo4j_driver() is not None:
        _repository_singleton = AddressBookNeo4jRepository(fallback=memory)
    else:
        _repository_singleton = memory
    return _repository_singleton


def get_address_book_use_case() -> AddressBookUseCase:
    return AddressBookInteractor(repository=get_address_book_repository())
