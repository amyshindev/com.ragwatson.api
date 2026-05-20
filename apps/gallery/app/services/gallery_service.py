"""갤러리 비즈니스 로직."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from gallery.app.repositories.gallery_repository import GalleryRepository

logger = logging.getLogger(__name__)


class GalleryService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = GalleryRepository(session)
