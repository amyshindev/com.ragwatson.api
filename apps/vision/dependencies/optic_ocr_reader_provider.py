from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from vision.adapter.outbound.pg.optic_ocr_reader_repository import OcrReaderPgRepository
from vision.app.ports.input.optic_ocr_reader_use_case import OcrReaderUseCase
from vision.app.ports.output.optic_ocr_reader_port import OcrReaderPort
from vision.app.use_cases.optic_ocr_reader_interactor import OcrReaderInteractor


def get_optic_ocr_reader_repository(
    db: AsyncSession = Depends(get_db),
) -> OcrReaderPort:
    return OcrReaderPgRepository(session=db)


def get_optic_ocr_reader_use_case(
    repository: OcrReaderPort = Depends(get_optic_ocr_reader_repository),
) -> OcrReaderUseCase:
    return OcrReaderInteractor(repository=repository)
