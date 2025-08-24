from datetime import datetime

from pydantic import BaseModel


class ReplacementCreate(BaseModel):
    from_item: str
    to_item: str


class ReplacementRead(BaseModel):
    id: int
    user_id: int
    from_item: str
    to_item: str
    created_at: datetime

    class Config:
        from_attributes = True


