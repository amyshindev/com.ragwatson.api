import logging

from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.models.schemas import UserResponse
from secom.app.schemas.user_schema import LoginRequest, UserSchema
from secom.app.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserController:
    def __init__(self, session: AsyncSession) -> None:
        self.user_service = UserService(session)

    async def save_user(self, user_schema: UserSchema) -> None:
        await self.user_service.save_user(user_schema)
        logger.info(
            "[UserController] save_user 레이어 완료 — userId=%s",
            user_schema.userId,
        )

    async def login(self, login_request: LoginRequest) -> UserResponse:
        result = await self.user_service.login(login_request)
        logger.info("[UserController] login 레이어 완료 — id=%s", result.id)
        return result

