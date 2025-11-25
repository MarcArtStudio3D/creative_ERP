"""add_database_config_fields_to_empresas_table

Revision ID: 6accb119908d
Revises: 3bf5bd205a0f
Create Date: 2025-11-25 00:49:11.074678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6accb119908d'
down_revision: Union[str, Sequence[str], None] = '3bf5bd205a0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Agregar campos de configuración de base de datos a la tabla empresas
    op.add_column('empresas', sa.Column('motor_base_datos', sa.String(20), nullable=True, default='mariadb', comment='Motor de base de datos: mariadb o postgresql'))
    op.add_column('empresas', sa.Column('nombre_base_datos_maria_db', sa.String(100), nullable=True, comment='Nombre de la base de datos MariaDB/PostgreSQL'))
    op.add_column('empresas', sa.Column('nombre_base_datos_postgresql', sa.String(100), nullable=True, comment='Nombre de la base de datos PostgreSQL'))
    op.add_column('empresas', sa.Column('host_mariadb', sa.String(100), nullable=True, default='localhost', comment='Host del servidor MariaDB'))
    op.add_column('empresas', sa.Column('puerto_mariadb', sa.Integer(), nullable=True, default=3306, comment='Puerto del servidor MariaDB'))
    op.add_column('empresas', sa.Column('usuario_mariadb', sa.String(50), nullable=True, default='admin', comment='Usuario MariaDB'))
    op.add_column('empresas', sa.Column('password_mariadb', sa.String(255), nullable=True, default='admin123', comment='Contraseña MariaDB'))
    op.add_column('empresas', sa.Column('host_postgresql', sa.String(100), nullable=True, default='localhost', comment='Host del servidor PostgreSQL'))
    op.add_column('empresas', sa.Column('puerto_postgresql', sa.Integer(), nullable=True, default=5432, comment='Puerto del servidor PostgreSQL'))
    op.add_column('empresas', sa.Column('usuario_postgresql', sa.String(50), nullable=True, default='postgres', comment='Usuario PostgreSQL'))
    op.add_column('empresas', sa.Column('password_postgresql', sa.String(255), nullable=True, default='postgres', comment='Contraseña PostgreSQL'))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar campos de configuración de base de datos de la tabla empresas
    op.drop_column('empresas', 'password_postgresql')
    op.drop_column('empresas', 'usuario_postgresql')
    op.drop_column('empresas', 'puerto_postgresql')
    op.drop_column('empresas', 'host_postgresql')
    op.drop_column('empresas', 'password_mariadb')
    op.drop_column('empresas', 'usuario_mariadb')
    op.drop_column('empresas', 'puerto_mariadb')
    op.drop_column('empresas', 'host_mariadb')
    op.drop_column('empresas', 'nombre_base_datos_postgresql')
    op.drop_column('empresas', 'nombre_base_datos_maria_db')
    op.drop_column('empresas', 'motor_base_datos')
