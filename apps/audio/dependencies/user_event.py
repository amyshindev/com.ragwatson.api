from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from ml_data.adapter.outbound.pg.user_event_pg_repository import UserEventPgRepository
from ml_data.app.ports.input.user_event_use_case import UserEventUseCase
from ml_data.app.ports.output.user_event_repository import UserEventRepository
from ml_data.app.use_cases.user_event_interactor import UserEventInteractor


def get_user_event_use_case(
    db: AsyncSession = Depends(get_db),
) -> UserEventUseCase:
    repository: UserEventRepository = UserEventPgRepository(session=db)
    return UserEventInteractor(session=db, repository=repository)
