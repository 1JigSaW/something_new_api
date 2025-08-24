from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        type_=BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    email: Mapped[str] = mapped_column(
        type_=String(320),
        unique=True,
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        type_=Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    premium_until: Mapped[datetime | None] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=True,
    )

    replacements_count_today: Mapped[int] = mapped_column(
        type_=Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    challenges_count_today: Mapped[int] = mapped_column(
        type_=Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    last_seen: Mapped[datetime | None] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=False,
        server_default="now()",
    )

    updated_at: Mapped[datetime] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=False,
        server_default="now()",
    )


