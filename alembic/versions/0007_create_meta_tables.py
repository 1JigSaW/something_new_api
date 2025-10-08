from alembic import op
import sqlalchemy as sa


revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(length=50), unique=True, nullable=False),
    )

    op.create_table(
        "sizes",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(length=16), unique=True, nullable=False),
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(length=50), unique=True, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("tags")
    op.drop_table("sizes")
    op.drop_table("categories")


