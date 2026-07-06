from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from vision.adapter.outbound.pg.optic_clip_embedder_repository import ClipEmbedderPgRepository
from vision.app.ports.input.optic_clip_embedder_use_case import ClipEmbedderUseCase
from vision.app.ports.output.optic_clip_embedder_port import ClipEmbedderPort
from vision.app.use_cases.optic_clip_embedder_interactor import ClipEmbedderInteractor


def get_optic_clip_embedder_repository(
    db: AsyncSession = Depends(get_db),
) -> ClipEmbedderPort:
    return ClipEmbedderPgRepository(session=db)


def get_optic_clip_embedder_use_case(
    repository: ClipEmbedderPort = Depends(get_optic_clip_embedder_repository),
) -> ClipEmbedderUseCase:
    return ClipEmbedderInteractor(repository=repository)
