from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.outbound.pg.user_event_pg_repository import UserEventPgRepository
from audio.app.ports.input.user_event_use_case import UserEventUseCase
from audio.app.ports.output.user_event_repository import UserEventRepository
from audio.app.use_cases.user_event_interactor import UserEventInteractor
from core.matrix.oracle_database import get_db


def get_user_event_use_case(
    db: AsyncSession = Depends(get_db),
) -> UserEventUseCase:
    repository: UserEventRepository = UserEventPgRepository(session=db)
    return UserEventInteractor(session=db, repository=repository)
