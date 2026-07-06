from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from vision.adapter.outbound.pg.optic_resnet_classifier_repository import ResnetClassifierPgRepository
from vision.app.ports.input.optic_resnet_classifier_use_case import ResnetClassifierUseCase
from vision.app.ports.output.optic_resnet_classifier_port import ResnetClassifierPort
from vision.app.use_cases.optic_resnet_classifier_interactor import ResnetClassifierInteractor


def get_optic_resnet_classifier_repository(
    db: AsyncSession = Depends(get_db),
) -> ResnetClassifierPort:
    return ResnetClassifierPgRepository(session=db)


def get_optic_resnet_classifier_use_case(
    repository: ResnetClassifierPort = Depends(get_optic_resnet_classifier_repository),
) -> ResnetClassifierUseCase:
    return ResnetClassifierInteractor(repository=repository)
