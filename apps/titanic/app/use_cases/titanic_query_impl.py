import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.input.titanic_query_port import TitanicQueryPort
from titanic.app.use_cases.jack_service import JackService

log = logging.getLogger(__name__)


class TitanicQueryUseCase(TitanicQueryPort):
    async def get_passenger_data(self, session: AsyncSession) -> list[dict[str, Any]]:
        jack = JackService(session)
        df = await jack.get_data_db()
        records = df.to_dict(orient="records") if not df.empty else []
        log.info("[TitanicQueryUseCase] get_passenger_data 완료 — rows=%s", len(records))
        return records

    async def get_passenger_count(self, session: AsyncSession) -> int:
        jack = JackService(session)
        count = await jack.get_count_db()
        log.info("[TitanicQueryUseCase] get_passenger_count 완료 — count=%s", count)
        return count

    def has_decision_tree_model(self) -> bool:
        return JackService().has_decision_tree_model()

    def get_model_name(self) -> str:
        return JackService().get_model_name_and_accuracy()
