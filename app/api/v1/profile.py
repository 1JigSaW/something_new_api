from datetime import date, timedelta, datetime, timezone
from typing import List

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
    today = datetime.now(timezone.utc).date()
    cc_repo = ChallengeCompletionRepository(session=session)
    repl_repo = ReplacementRepository(session=session)
    cc = await cc_repo.count_for_day(user_id=user_id, d=today)
    repl = await repl_repo.count_for_day(user_id=user_id, d=today)
    passed = cc >= 1
    return {"challenges_today": cc, "replacements_today": repl, "day_passed": passed}


@router.get("/stats")
async def get_progress_stats(
    user_id: int = Depends(get_current_user_id),
    session=Depends(get_db_session),
):
    """Get user's progress statistics for calendar and charts"""
    cc_repo = ChallengeCompletionRepository(session=session)
    
    # Get completion data for the last 30 days
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=30)
    
    daily_stats = []
    current_date = start_date
    
    while current_date <= end_date:
        completed_count = await cc_repo.count_for_day(user_id=user_id, d=current_date)
        daily_stats.append({
            "date": current_date.isoformat(),
            "completed": completed_count
        })
        current_date += timedelta(days=1)
    
    # Calculate streak
    streak = 0
    check_date = end_date
    while check_date >= start_date:
        day_stats = next((stat for stat in daily_stats if stat["date"] == check_date.isoformat()), None)
        if day_stats and day_stats["completed"] > 0:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    # Get total completed challenges
    total_completed = sum(stat["completed"] for stat in daily_stats)
    
    return {
        "daily_stats": daily_stats,
        "streak": streak,
        "total_completed": total_completed,
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    }


@router.get("/stats/test")
async def get_progress_stats_test(
    session=Depends(get_db_session),
):
    """Test endpoint without authentication - returns mock data"""
    # Return mock data for testing
    today = date.today()
    daily_stats = []
    
    for i in range(30):
        current_date = today - timedelta(days=29-i)
        daily_stats.append({
            "date": current_date.isoformat(),
            "completed": 1 if i % 3 == 0 else 0  # Mock: completed every 3rd day
        })
    
    return {
        "daily_stats": daily_stats,
        "streak": 5,  # Mock streak
        "total_completed": 10,  # Mock total
        "period": {
            "start_date": (today - timedelta(days=29)).isoformat(),
            "end_date": today.isoformat()
        }
    }


