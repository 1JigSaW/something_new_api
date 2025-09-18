from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/reset-today")
async def reset_today_progress(
    session: AsyncSession = Depends(get_db_session),
):
    """Reset today's progress for testing purposes"""
    try:
        today = date.today()
        
        # Delete today's activities
        stmt_activities = text("""
            DELETE FROM user_activities 
            WHERE DATE(created_at) = :today
        """)
        result_activities = await session.execute(stmt_activities, {"today": today})
        
        await session.commit()
        
        return {
            "message": "Today's progress has been reset successfully!",
            "deleted_activities": result_activities.rowcount
        }
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error resetting today's progress: {str(e)}")