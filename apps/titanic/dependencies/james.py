from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

"""
James 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(JamesPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(JamesUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from core.matrix.oracle_database import get_db
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository
from titanic.app.use_cases.james_interactor import JamesInteractor


def get_james_use_case(
    db: AsyncSession = Depends(get_db),
) -> JamesUseCase:
    repository: JamesRepository = JamesPgRepository(session=db)
    return JamesInteractor(session=db, repository=repository)
