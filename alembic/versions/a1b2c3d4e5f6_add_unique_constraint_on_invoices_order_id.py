"""add unique constraint on invoices.order_id

Revision ID: a1b2c3d4e5f6
Revises: 6e6b7e4f8a18
Create Date: 2026-04-30 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '6e6b7e4f8a18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('uq_invoices_order_id', 'invoices', ['order_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_invoices_order_id', 'invoices', type_='unique')
