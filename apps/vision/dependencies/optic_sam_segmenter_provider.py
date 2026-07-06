from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from vision.adapter.outbound.pg.optic_sam_segmenter_repository import SamSegmenterPgRepository
from vision.app.ports.input.optic_sam_segmenter_use_case import SamSegmenterUseCase
from vision.app.ports.output.optic_sam_segmenter_port import SamSegmenterPort
from vision.app.use_cases.optic_sam_segmenter_interactor import SamSegmenterInteractor


def get_optic_sam_segmenter_repository(
    db: AsyncSession = Depends(get_db),
) -> SamSegmenterPort:
    return SamSegmenterPgRepository(session=db)


def get_optic_sam_segmenter_use_case(
    repository: SamSegmenterPort = Depends(get_optic_sam_segmenter_repository),
) -> SamSegmenterUseCase:
    return SamSegmenterInteractor(repository=repository)
