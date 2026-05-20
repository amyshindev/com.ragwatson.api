"""갤러리 영속화."""

from sqlalchemy.ext.asyncio import AsyncSession


class GalleryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
