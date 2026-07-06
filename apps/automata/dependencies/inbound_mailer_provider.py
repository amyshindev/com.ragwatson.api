import logging
import os
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from automata.adapter.outbound.memory.inbound_mail_memory_repository import (
    InboundMailMemoryRepository,
)
from automata.adapter.outbound.ollama.inbound_mail_embedding_adapter import (
    OllamaMailEmbeddingAdapter,
)
from automata.adapter.outbound.pg.inbound_mail_pg_repository import InboundMailPgRepository
from automata.app.ports.input.inbound_mail_use_case import InboundMailUseCase
from automata.app.ports.output.inbound_mail_port import InboundMailPort
from automata.app.use_cases.inbound_mailer_interactor import InboundMailerInteractor
from core.config import is_database_configured
from database import get_db

log = logging.getLogger(__name__)

_memory_singleton: InboundMailMemoryRepository | None = None
_embedder_singleton: OllamaMailEmbeddingAdapter | None = None


def _get_memory_repository() -> InboundMailMemoryRepository:
    global _memory_singleton
    if _memory_singleton is None:
        _memory_singleton = InboundMailMemoryRepository()
    return _memory_singleton


def _get_embedder() -> OllamaMailEmbeddingAdapter:
    global _embedder_singleton
    if _embedder_singleton is None:
        _embedder_singleton = OllamaMailEmbeddingAdapter()
    return _embedder_singleton


async def _get_optional_db() -> AsyncGenerator[AsyncSession | None, None]:
    if not is_database_configured():
        yield None
        return
    async for session in get_db():
        yield session


OptionalDbSession = Annotated[AsyncSession | None, Depends(_get_optional_db)]


def get_inbound_mail_repository(session: OptionalDbSession) -> InboundMailPort:
    if session is not None:
        return InboundMailPgRepository(session, _get_embedder())
    return _get_memory_repository()


def get_inbound_mail_use_case(
    repository: InboundMailPort = Depends(get_inbound_mail_repository),
) -> InboundMailUseCase:
    return InboundMailerInteractor(repository=repository)


def get_inbound_secret() -> str | None:
    secret = (os.getenv("AUTOMATA_INBOUND_SECRET") or os.getenv("N8N_INBOUND_SECRET") or "").strip()
    return secret or None
