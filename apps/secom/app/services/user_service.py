import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.models.schemas import UserResponse
from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import LoginRequest, UserSchema
from secom.app.services.password_hasher import hash_password, verify_password

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repository = UserRepository(session)

    async def save_user(self, user_schema: UserSchema) -> None:
        data = user_schema.to_user_create()

        if await self.user_repository.get_by_email(str(data.email)):
            raise HTTPException(status_code=409, detail="이미 사용 중인 이메일입니다.")
        if await self.user_repository.get_by_username(data.username):
            raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")

        user = await self.user_repository.save_user(
            email=str(data.email),
            username=data.username,
            nickname=data.nickname,
            password=hash_password(data.password),
            role=data.role,
        )
        user_schema.userId = user.id
        logger.info("[UserService] save_user 레이어 완료 — userId=%s", user_schema.userId)

    async def login(self, login_request: LoginRequest) -> UserResponse:
        user = await self.user_repository.get_by_email(str(login_request.email))
        if user is None or not verify_password(login_request.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )
        result = UserResponse.model_validate(user)
        logger.info("[UserService] login 레이어 완료 — id=%s", result.id)
        return result

