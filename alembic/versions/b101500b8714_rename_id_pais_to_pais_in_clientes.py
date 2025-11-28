"""rename_id_pais_to_pais_in_clientes

Revision ID: b101500b8714
Revises: 928293cff6a2
Create Date: 2025-11-28 17:18:16.765767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b101500b8714'
down_revision: Union[str, Sequence[str], None] = '928293cff6a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Renombrar columna id_pais a pais en la tabla clientes (MySQL requiere especificar el tipo)
    op.alter_column('clientes', 'id_pais', 
                   new_column_name='pais',
                   existing_type=sa.String(100),
                   existing_nullable=True)
    
    # Renombrar columna id_pais a pais en la tabla direcciones_alternativas si existe
    try:
        op.alter_column('direcciones_alternativas', 'id_pais', 
                       new_column_name='pais',
                       existing_type=sa.String(100),
                       existing_nullable=True)
    except Exception as e:
        print(f"Tabla direcciones_alternativas: {e}")
        # Si la tabla no existe o no tiene esa columna, continuar
        pass


def downgrade() -> None:
    """Downgrade schema."""
    # Revertir: renombrar columna pais de vuelta a id_pais
    op.alter_column('clientes', 'pais', 
                   new_column_name='id_pais',
                   existing_type=sa.String(100),
                   existing_nullable=True)
    
    # Revertir en direcciones_alternativas si existe
    try:
        op.alter_column('direcciones_alternativas', 'pais', 
                       new_column_name='id_pais',
                       existing_type=sa.String(100),
                       existing_nullable=True)
    except Exception as e:
        print(f"Tabla direcciones_alternativas: {e}")
        # Si la tabla no existe o no tiene esa columna, continuar
        pass
