"""갤러리 비즈니스 로직."""

import logging

from gallery.app.repositories.gallery_repository import GalleryRepository
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class GalleryService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = GalleryRepository(session)
