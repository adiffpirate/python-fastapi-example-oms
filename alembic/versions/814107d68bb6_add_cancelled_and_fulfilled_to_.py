"""add CANCELLED and FULFILLED to OrderStatus enum

Revision ID: 814107d68bb6
Revises: 084d9bd91fca
Create Date: 2026-04-27 05:13:11.551687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '814107d68bb6'
down_revision: Union[str, Sequence[str], None] = '084d9bd91fca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename old type, create new type with all values, reassign column
    op.execute("ALTER TYPE orderstatus RENAME TO orderstatus_old")
    op.execute(
        "CREATE TYPE orderstatus AS ENUM "
        "('RECEIVED', 'PROCESSING', 'FULFILLED', 'SHIPPED', 'DELIVERED', 'CANCELLED')"
    )
    op.execute(
        "ALTER TABLE orders ALTER COLUMN status TYPE orderstatus "
        "USING status::text::orderstatus"
    )
    op.execute("DROP TYPE orderstatus_old")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE orderstatus RENAME TO orderstatus_old")
    op.execute(
        "CREATE TYPE orderstatus AS ENUM "
        "('RECEIVED', 'PROCESSING', 'SHIPPED', 'DELIVERED')"
    )
    op.execute(
        "ALTER TABLE orders ALTER COLUMN status TYPE orderstatus "
        "USING status::text::orderstatus"
    )
    op.execute("DROP TYPE orderstatus_old")
