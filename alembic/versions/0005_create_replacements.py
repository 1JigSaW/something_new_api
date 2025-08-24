from alembic import op
import sqlalchemy as sa


revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "replacements",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("from_item", sa.String(length=120), nullable=False),
        sa.Column("to_item", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_replacements_user_id", "replacements", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_replacements_user_id", table_name="replacements")
    op.drop_table("replacements")


