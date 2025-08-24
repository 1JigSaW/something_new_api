from alembic import op
import sqlalchemy as sa


revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "challenges",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("short_description", sa.String(length=500), nullable=True),
        sa.Column("category", sa.String(length=50), nullable=True),
        sa.Column("tags", sa.String(length=200), nullable=True),
        sa.Column("size", sa.String(length=16), nullable=False, server_default=sa.text("'small'")),
        sa.Column("estimated_duration_min", sa.Integer(), nullable=True),
        sa.Column("is_premium_only", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_challenges_title", "challenges", ["title"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_challenges_title", table_name="challenges")
    op.drop_table("challenges")


