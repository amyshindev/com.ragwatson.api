from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatSchema,
    SmithCaptainSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import (
    ChatResponse,
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case
from titanic.dependencies.passenger_cal_tester_provider import get_cal_tester_use_case
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_walter_roaster_use_case


from fastapi import Depends

logger = logging.getLogger(__name__)


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository
        self.jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case)
        self.rose: RoseModelUseCase = Depends(get_rose_model_use_case)
        self.cal: CalTesterUseCase = Depends(get_cal_tester_use_case)
        self.walter: WalterRoasterUseCase = Depends(get_walter_roaster_use_case)


    async def chat(self, schema: ChatSchema) -> ChatResponse:
        logger.info(f"[SmithCaptainInteractor] chat 진입 | message={schema.message}")
        train_set = self.walter.get_train_set()
        test_set = self.walter.get_test_set()
        self.jack.get_model_train(train_set)
        self.cal.get_model_test(test_set)
        return ChatResponse(text="1309명 입니다")



    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터랙트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))


CrewSmithCaptainInteractor = SmithCaptainInteractor
