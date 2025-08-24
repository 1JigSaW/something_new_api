from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repo import UserRepository


class UserService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.repo = UserRepository(
            session=session,
        )

    async def get_or_create_by_email(
        self,
        email: str,
    ) -> User:
        return await self.repo.create_if_not_exists(
            email=email,
        )


