"""add invoices table

Revision ID: 6e6b7e4f8a18
Revises: 814107d68bb6
Create Date: 2026-04-30 03:03:29.938373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e6b7e4f8a18'
down_revision: Union[str, Sequence[str], None] = '814107d68bb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'invoices',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id'), nullable=False, index=True),
        sa.Column('status', sa.Enum('PENDING', 'PAID', 'CANCELLED', name='invoicestatus'), nullable=False, default='PENDING'),
        sa.Column('external_invoice_id', sa.String(), nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('invoices')
