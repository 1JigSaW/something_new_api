from datetime import datetime

from pydantic import BaseModel


class ChallengeCreate(BaseModel):
    title: str
    short_description: str | None = None
    category: str | None = None
    tags: str | None = None
    size: str = "small"
    estimated_duration_min: int | None = None
    is_premium_only: bool = False


class ChallengeRead(BaseModel):
    id: int
    title: str
    short_description: str | None
    category: str | None
    tags: str | None
    size: str
    estimated_duration_min: int | None
    is_premium_only: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


