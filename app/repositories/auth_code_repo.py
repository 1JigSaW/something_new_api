from datetime import date, datetime, time, timezone
from typing import Optional

from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_code import AuthCode


class AuthCodeRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        user_id: int,
        code: str,
        expires_at: datetime,
    ) -> AuthCode:
        auth = AuthCode(
            user_id=user_id,
            code=code,
            expires_at=expires_at,
        )
        self.session.add(auth)
        await self.session.flush()
        return auth

    async def count_requests_today(
        self,
        user_id: int,
        d: date,
    ) -> int:
        start = datetime.combine(d, time.min, tzinfo=timezone.utc)
        end = datetime.combine(d, time.max, tzinfo=timezone.utc)
        stmt = select(func.count(AuthCode.id)).where(
            AuthCode.user_id == user_id,
            AuthCode.created_at >= start,
            AuthCode.created_at <= end,
        )
        res = await self.session.execute(stmt)
        return int(res.scalar_one() or 0)

    async def get_valid(
        self,
        user_id: int,
        code: str,
        now: datetime,
    ) -> Optional[AuthCode]:
        stmt = select(AuthCode).where(
            AuthCode.user_id == user_id,
            AuthCode.code == code,
            AuthCode.expires_at >= now,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_for_user(
        self,
        user_id: int,
    ) -> None:
        stmt = delete(AuthCode).where(AuthCode.user_id == user_id)
        await self.session.execute(stmt)


