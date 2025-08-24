from datetime import date, datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.models.user import User
from app.repositories.auth_code_repo import AuthCodeRepository
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.auth_repo = AuthCodeRepository(session=session)
        self.user_repo = UserRepository(session=session)

    async def request_code(
        self,
        email: str,
    ) -> None:
        user = await self.user_repo.create_if_not_exists(email=email)
        today = date.today()
        if await self.auth_repo.count_requests_today(user_id=user.id, d=today) >= 1:
            raise ValueError("rate_limited")
        await self.auth_repo.delete_for_user(user_id=user.id)
        await self.auth_repo.create(
            user_id=user.id,
            code=user.email.split("@")[0],
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        )
        await self.session.commit()

    async def verify_code(
        self,
        email: str,
        code: str,
    ) -> str:
        user = await self.user_repo.create_if_not_exists(email=email)
        now = datetime.now(timezone.utc)
        auth = await self.auth_repo.get_valid(user_id=user.id, code=code, now=now)
        if not auth:
            raise ValueError("invalid_code")
        token = create_access_token(subject=str(user.id))
        return token


