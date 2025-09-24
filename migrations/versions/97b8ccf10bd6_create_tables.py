"""Create tables

Revision ID: 97b8ccf10bd6
Revises:
Create Date: 2025-09-24 20:31:13.481827

"""
import sqlalchemy as sa
from alembic import op

revision = "97b8ccf10bd6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "priority",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "board",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("body", sa.String(length=255), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("priority_id", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["board.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["priority_id"],
            ["priority.id"],
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["status.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint(None, "board", ["name", "user_id"])


def downgrade() -> None:
    op.drop_table("task")
    op.drop_table("board")
    op.drop_table("user")
    op.drop_table("status")
    op.drop_table("priority")
