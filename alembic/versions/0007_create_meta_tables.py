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
        sa.Column("name", sa.String(length=50), unique=True, index=True, nullable=False),
    )
    op.create_index("ix_categories_name", "categories", ["name"], unique=True)

    op.create_table(
        "sizes",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(length=16), unique=True, index=True, nullable=False),
    )
    op.create_index("ix_sizes_name", "sizes", ["name"], unique=True)

    op.create_table(
        "tags",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(length=50), unique=True, index=True, nullable=False),
    )
    op.create_index("ix_tags_name", "tags", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_tags_name", table_name="tags")
    op.drop_table("tags")
    op.drop_index("ix_sizes_name", table_name="sizes")
    op.drop_table("sizes")
    op.drop_index("ix_categories_name", table_name="categories")
    op.drop_table("categories")


