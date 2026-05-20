"""커뮤니티 갤러리 (/explore): 공개 작품 메타·태그·노출 순서."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from gallery.app.services.gallery_service import GalleryService

logger = logging.getLogger(__name__)


class GalleryController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = GalleryService(session)
