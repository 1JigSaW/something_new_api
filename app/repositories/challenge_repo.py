from typing import Sequence
import random

from sqlalchemy import and_, or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import Challenge


class ChallengeRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def list_all(
        self,
        limit: int = 50,
        offset: int = 0,
        category: str | None = None,
        size: str | None = None,
        q: str | None = None,
        free_only: bool = False,
    ) -> Sequence[Challenge]:
        stmt = select(Challenge)
        conds = []
        if category:
            conds.append(Challenge.category == category)
        if size:
            conds.append(Challenge.size == size)
        if q:
            like = f"%{q}%"
            conds.append(or_(Challenge.title.ilike(like), Challenge.short_description.ilike(like)))
        if free_only:
            conds.append(Challenge.is_premium_only.is_(False))
        if conds:
            stmt = stmt.where(and_(*conds))
        stmt = stmt.order_by(Challenge.id).limit(limit).offset(offset)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_by_id(
        self,
        challenge_id: int,
    ) -> Challenge | None:
        stmt = select(Challenge).where(Challenge.id == challenge_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_random(
        self,
        limit: int = 5,
        category: str | None = None,
        size: str | None = None,
        free_only: bool = False,
    ) -> Sequence[Challenge]:
        """Get random challenges with optional filters"""
        stmt = select(Challenge)
        conds = []
        
        if category:
            conds.append(Challenge.category == category)
        if size:
            conds.append(Challenge.size == size)
        if free_only:
            conds.append(Challenge.is_premium_only.is_(False))
            
        if conds:
            stmt = stmt.where(and_(*conds))
        
        # Используем func.random() для получения случайных записей
        stmt = stmt.order_by(func.random()).limit(limit)
        
        res = await self.session.execute(stmt)
        return list(res.scalars().all())


