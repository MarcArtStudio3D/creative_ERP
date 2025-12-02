"""add precio_venta to articulos

Revision ID: c4e5f6a1b2c3
Revises: ebabfdc0ca54
Create Date: 2025-12-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4e5f6a1b2c3'
down_revision: Union[str, Sequence[str], None] = 'ebabfdc0ca54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Añadimos columna precio_venta a articulos con valor por defecto 0.0
    op.add_column('articulos', sa.Column('precio_venta', sa.Float(), nullable=False, server_default=sa.text('0.0')))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('articulos', 'precio_venta')
