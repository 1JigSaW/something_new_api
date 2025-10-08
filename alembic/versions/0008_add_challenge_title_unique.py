from alembic import op
import sqlalchemy as sa


revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("ix_challenges_title", table_name="challenges")
    op.create_index(
        "ix_challenges_title",
        "challenges",
        ["title"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_challenges_title", table_name="challenges")
    op.create_index(
        "ix_challenges_title",
        "challenges",
        ["title"],
        unique=False,
    )
