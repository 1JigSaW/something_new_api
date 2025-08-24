from datetime import datetime, timedelta
import secrets

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuthCode(Base):
    __tablename__ = "auth_codes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(String(64), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    @staticmethod
    def make_code() -> str:
        return secrets.token_urlsafe(16)

    @staticmethod
    def expiry(minutes: int = 10) -> datetime:
        return datetime.utcnow() + timedelta(minutes=minutes)


