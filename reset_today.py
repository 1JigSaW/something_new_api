#!/usr/bin/env python3
"""
Script to reset today's progress for testing
"""
import asyncio
import sys
import os
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import delete, text

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5433/something_new")

async def reset_today_progress():
    """Reset today's progress for all users"""
    engine = create_async_engine(DATABASE_URL)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session_maker() as session:
        try:
            today = date.today()
            
            # Delete today's activities using raw SQL
            stmt_activities = text("""
                DELETE FROM user_activities 
                WHERE DATE(created_at) = :today
            """)
            result_activities = await session.execute(stmt_activities, {"today": today})
            print(f"Deleted {result_activities.rowcount} activities from today")
            
            # Delete today's favorites using raw SQL (optional - uncomment if needed)
            # stmt_favorites = text("""
            #     DELETE FROM user_favorites 
            #     WHERE DATE(created_at) = :today
            # """)
            # result_favorites = await session.execute(stmt_favorites, {"today": today})
            # print(f"Deleted {result_favorites.rowcount} favorites from today")
            
            await session.commit()
            print("✅ Today's progress has been reset successfully!")
            
        except Exception as e:
            print(f"❌ Error resetting today's progress: {e}")
            await session.rollback()
            sys.exit(1)
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(reset_today_progress())
