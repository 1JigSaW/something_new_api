from alembic import op


revision = "0009_meta_unique_indexes"
down_revision = "29941213f5e3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_categories_name ON categories (name)")
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_sizes_name ON sizes (name)")
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_tags_name ON tags (name)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ux_categories_name")
    op.execute("DROP INDEX IF EXISTS ux_sizes_name")
    op.execute("DROP INDEX IF EXISTS ux_tags_name")
