from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.models.role import UserRole
from secom.app.models.schemas import UserCreate, UserResponse
from secom.app.repositories.user_repository import UserRepository
from secom.app.services.password_hasher import hash_password

# 초기 시드: 관리자·일반유저 각 1명
SEED_USERS: tuple[UserCreate, ...] = (
    UserCreate(
        email="dd@dfd.com",
        username="dfdf",
        nickname="dfdf",
        password="dfdfd",
        role=UserRole.ADMIN,
    ),
    UserCreate(
        email="user@dfd.com",
        username="userdf",
        nickname="userdf",
        password="dfdfd",
        role=UserRole.USER,
    ),
)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserRepository(session)

    async def register(self, data: UserCreate) -> UserResponse:
        if await self._repo.get_by_email(str(data.email)):
            raise HTTPException(status_code=409, detail="이미 사용 중인 이메일입니다.")
        if await self._repo.get_by_username(data.username):
            raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")

        user = await self._repo.create(
            email=str(data.email),
            username=data.username,
            nickname=data.nickname,
            password=hash_password(data.password),
            role=data.role,
        )
        return UserResponse.model_validate(user)

    async def seed_defaults_if_empty(self) -> None:
        if await self._repo.count() > 0:
            return
        for seed in SEED_USERS:
            if await self._repo.get_by_email(str(seed.email)):
                continue
            if await self._repo.get_by_username(seed.username):
                continue
            await self._repo.create(
                email=str(seed.email),
                username=seed.username,
                nickname=seed.nickname,
                password=hash_password(seed.password),
                role=seed.role,
            )
