"""create empresas table

Revision ID: 88c124189360
Revises: a8347d9f4009
Create Date: 2025-11-20 02:08:46.879711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88c124189360'
down_revision: Union[str, Sequence[str], None] = 'a8347d9f4009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('empresas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo_empresa', sa.String(50), nullable=False),
        sa.Column('nombre_fiscal', sa.String(200), nullable=False),
        sa.Column('nombre_comercial', sa.String(200)),
        sa.Column('cif_nif_siren', sa.String(50), nullable=False),
        sa.Column('direccion', sa.String(255)),
        sa.Column('cp', sa.String(10)),
        sa.Column('poblacion', sa.String(100)),
        sa.Column('provincia', sa.String(100)),
        sa.Column('id_pais', sa.Integer(), default=1),
        sa.Column('telefono1', sa.String(50)),
        sa.Column('email', sa.String(200)),
        sa.Column('web', sa.String(200)),
        sa.Column('fecha_alta', sa.DateTime(), default=sa.func.now()),
        sa.Column('activa', sa.Boolean(), default=True),
        sa.Column('notas', sa.Text()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo_empresa'),
        sa.UniqueConstraint('cif_nif')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('empresas')
