from alembic import op
import sqlalchemy as sa


revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "auth_codes",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("code", sa.String(length=64)),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_auth_codes_user_id", "auth_codes", ["user_id"], unique=False)
    op.create_index("ix_auth_codes_code", "auth_codes", ["code"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_auth_codes_code", table_name="auth_codes")
    op.drop_index("ix_auth_codes_user_id", table_name="auth_codes")
    op.drop_table("auth_codes")


