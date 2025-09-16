from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import Challenge
from app.repositories.challenge_repo import ChallengeRepository


class ChallengeService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.repo = ChallengeRepository(session=session)

    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        category: str | None = None,
        size: str | None = None,
        q: str | None = None,
        free_only: bool = False,
    ) -> Sequence[Challenge]:
        return await self.repo.list_all(
            limit=limit,
            offset=offset,
            category=category,
            size=size,
            q=q,
            free_only=free_only,
        )

    async def get(
        self,
        challenge_id: int,
    ) -> Challenge | None:
        return await self.repo.get_by_id(challenge_id=challenge_id)

    async def get_random(
        self,
        limit: int = 5,
        category: str | None = None,
        size: str | None = None,
        free_only: bool = False,
    ) -> Sequence[Challenge]:
        return await self.repo.get_random(
            limit=limit,
            category=category,
            size=size,
            free_only=free_only,
        )


