from alembic import op
import sqlalchemy as sa


revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "challenge_completions",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True),
        sa.Column("challenge_id", sa.BigInteger(), sa.ForeignKey("challenges.id", ondelete="CASCADE"), index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_cc_user_id", "challenge_completions", ["user_id"], unique=False)
    op.create_index("ix_cc_challenge_id", "challenge_completions", ["challenge_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_cc_challenge_id", table_name="challenge_completions")
    op.drop_index("ix_cc_user_id", table_name="challenge_completions")
    op.drop_table("challenge_completions")


