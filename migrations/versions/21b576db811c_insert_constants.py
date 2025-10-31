"""Insert constants

Revision ID: 21b576db811c
Revises: 97b8ccf10bd6
Create Date: 2025-10-31 22:11:22.875866

"""

import sqlalchemy as sa
from alembic import op

revision = "21b576db811c"
down_revision = "97b8ccf10bd6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table("priority", sa.column("name")),
        [
            {"name": "Minor"},
            {"name": "Major"},
            {"name": "Critical"},
        ],
    )
    op.bulk_insert(
        sa.table("status", sa.column("name")),
        [
            {"name": "To Do"},
            {"name": "In Progress"},
            {"name": "Closed"},
        ],
    )


def downgrade() -> None:
    for table in ["priority", "status"]:
        op.execute(
            sa.table(table).delete()
        )
