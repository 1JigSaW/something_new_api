from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def get_by_email(
        self,
        email: str,
    ) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_if_not_exists(
        self,
        email: str,
    ) -> User:
        existing = await self.get_by_email(email=email)
        if existing:
            return existing
        user = User(
            email=email,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_by_id(
        self,
        user_id: int,
    ) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


