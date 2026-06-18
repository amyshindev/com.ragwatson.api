from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.adapter.outbound.pg.crew_hartley_violin_repository import HartleyViolinPgRepository
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort
from titanic.app.use_cases.crew_hartley_violin_interactor import HartleyViolinInteractor


def get_hartley_violin_repository(
    db: AsyncSession = Depends(get_db),
) -> HartleyViolinPort:
    return HartleyViolinPgRepository(session=db)


def get_hartley_violin_use_case(
    repository: HartleyViolinPort = Depends(get_hartley_violin_repository),
) -> HartleyViolinUseCase:
    return HartleyViolinInteractor(repository=repository)


def get_hartley_violin_correlation_use_case() -> HartleyViolinUseCase:
    '''상관 히트맵 전용 — WalterReader(CSV)만 사용, Neon DB 연결 불필요'''
    return HartleyViolinInteractor(repository=None)

# --- 기존 correlation DI (DB Depends 체인 — Neon 비밀번호 오류 시 /correlation 실패) ---
# def get_hartley_violin_correlation_use_case(
#     repository: HartleyViolinPort = Depends(get_hartley_violin_repository),
# ) -> HartleyViolinUseCase:
#     return HartleyViolinInteractor(repository=repository)
