"""Fix fecha_alta format to date only

Revision ID: a8347d9f4009
Revises: e401056e286b
Create Date: 2025-11-18 15:27:20.600245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8347d9f4009'
down_revision: Union[str, Sequence[str], None] = 'e401056e286b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Corregir el formato de fecha_alta de datetime a date
    op.execute("""
        UPDATE clientes 
        SET fecha_alta = date(fecha_alta)
        WHERE fecha_alta LIKE '% %'
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # No podemos deshacer esta conversión fácilmente
    pass
