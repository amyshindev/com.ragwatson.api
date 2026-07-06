from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_holmes.adapter.outbound.pg.doctor_watson_chronicler_repository import WatsonChroniclerPgRepository
from sherlock_holmes.app.ports.input.doctor_watson_chronicler_use_case import WatsonChroniclerUseCase
from sherlock_holmes.app.ports.output.doctor_watson_chronicler_port import WatsonChroniclerPort
from sherlock_holmes.app.use_cases.doctor_watson_chronicler_interactor import WatsonChroniclerInteractor


def get_doctor_watson_chronicler_repository(
    db: AsyncSession = Depends(get_db),
) -> WatsonChroniclerPort:
    return WatsonChroniclerPgRepository(session=db)


def get_doctor_watson_chronicler_use_case(
    repository: WatsonChroniclerPort = Depends(get_doctor_watson_chronicler_repository),
) -> WatsonChroniclerUseCase:
    return WatsonChroniclerInteractor(repository=repository)
