from typing import Sequence

from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db.session import get_db_session
from app.schemas.challenge import ChallengeRead
from app.services.challenge_service import ChallengeService
from app.api.deps.auth import get_current_user_id
from app.services.challenge_completion_service import ChallengeCompletionService
from app.repositories.challenge_completion_repo import ChallengeCompletionRepository


router = APIRouter(prefix="/challenges", tags=["challenges"])


@router.get("/", response_model=list[ChallengeRead])
async def list_challenges(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    category: str | None = Query(default=None),
    size: str | None = Query(default=None),
    q: str | None = Query(default=None),
    free_only: bool = Query(default=False),
    session=Depends(get_db_session),
):
    service = ChallengeService(session=session)
    items = await service.list(
        limit=limit,
        offset=offset,
        category=category,
        size=size,
        q=q,
        free_only=free_only,
    )
    return items


@router.get("/random", response_model=list[ChallengeRead])
async def get_random_challenges(
    limit: int = Query(default=5, ge=1, le=20),
    category: str | None = Query(default=None),
    size: str | None = Query(default=None),
    free_only: bool = Query(default=False),
    session=Depends(get_db_session),
):
    """Get random challenges for daily use"""
    service = ChallengeService(session=session)
    items = await service.get_random(
        limit=limit,
        category=category,
        size=size,
        free_only=free_only,
    )
    return items


@router.get("/{challenge_id}", response_model=ChallengeRead)
async def get_challenge(
    challenge_id: int,
    session=Depends(get_db_session),
):
    service = ChallengeService(session=session)
    item = await service.get(challenge_id=challenge_id)
    if not item:
        raise HTTPException(status_code=404)
    return item


@router.post("/{challenge_id}/complete", status_code=201)
async def complete_challenge(
    challenge_id: int,
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    service = ChallengeCompletionService(session=session)
    try:
        await service.complete_with_limit(
            user_id=user_id,
            challenge_id=challenge_id,
            today=date.today(),
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.get("/completions", response_model=list[dict])
async def list_completions(
    date_from: date = Query(...),
    date_to: date = Query(...),
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    repo = ChallengeCompletionRepository(session=session)
    items = await repo.list_for_period(user_id=user_id, date_from=date_from, date_to=date_to)
    return [
        {"id": i.id, "challenge_id": i.challenge_id, "created_at": i.created_at}
        for i in items
    ]


