from datetime import date

from fastapi import APIRouter, Depends

from app.api.deps.auth import get_current_user_id
from app.db.session import get_db_session
from app.repositories.challenge_completion_repo import ChallengeCompletionRepository
from app.repositories.replacement_repo import ReplacementRepository


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/day")
async def profile_day(
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    today = date.today()
    cc_repo = ChallengeCompletionRepository(session=session)
    repl_repo = ReplacementRepository(session=session)
    cc = await cc_repo.count_for_day(user_id=user_id, d=today)
    repl = await repl_repo.count_for_day(user_id=user_id, d=today)
    passed = cc >= 1
    return {"challenges_today": cc, "replacements_today": repl, "day_passed": passed}


