from typing import Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class TitanicQueryPort(Protocol):
    async def get_passenger_data(self, session: AsyncSession) -> list[dict[str, Any]]:
        """첫 번째 승객 데이터를 조회한다."""

    async def get_passenger_count(self, session: AsyncSession) -> int:
        """승객 수를 조회한다."""

    def has_decision_tree_model(self) -> bool:
        """의사결정 트리 모델 파일 존재 여부."""

    def get_model_name(self) -> str:
        """모델 이름을 반환한다."""
