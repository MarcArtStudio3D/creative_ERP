"""Add initial demo data

Revision ID: 6271f8dcd28d
Revises: 8af07ea74430
Create Date: 2025-11-18 09:57:57.784382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6271f8dcd28d'
down_revision: Union[str, Sequence[str], None] = '8af07ea74430'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insertar grupos empresariales
    op.execute("""
        INSERT INTO business_groups (id, name, code, description) VALUES
        (1, 'ArtStudio', 'AS', 'Grupo ArtStudio'),
        (2, 'Demo Group', 'DEMO', 'Grupo de demostración')
    """)
    
    # Insertar empresas
    op.execute("""
        INSERT INTO companies (id, group_id, name, legal_name, vat_number) VALUES
        (1, 1, 'ARTSTUDIOPRUEBAS', 'ArtStudio Software y Diseño 3D SL', 'B12345678'),
        (2, 1, 'ArtStudio Music', 'ArtStudio Sonido y Música SL', 'B87654321'),
        (3, 2, 'Demo Company', 'Empresa de Demostración SL', 'B99999999')
    """)
    
    # Insertar usuarios (contraseñas hasheadas)
    import hashlib
    admin_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    manager_hash = hashlib.sha256('manager123'.encode()).hexdigest()
    contable_hash = hashlib.sha256('contable123'.encode()).hexdigest()
    ventas_hash = hashlib.sha256('ventas123'.encode()).hexdigest()
    user_hash = hashlib.sha256('user123'.encode()).hexdigest()
    
    op.execute(f"""
        INSERT INTO users (id, username, email, full_name, password_hash, role, allowed_groups) VALUES
        (1, 'admin', 'admin@artstudio.com', 'Administrador', '{admin_hash}', 'admin', '[1,2]'),
        (2, 'manager', 'manager@artstudio.com', 'Gestor', '{manager_hash}', 'manager', '[1]'),
        (3, 'contable', 'contable@artstudio.com', 'Contable', '{contable_hash}', 'accountant', '[1]'),
        (4, 'ventas', 'ventas@artstudio.com', 'Vendedor', '{ventas_hash}', 'sales', '[1]'),
        (5, 'user', 'user@demo.com', 'Usuario Demo', '{user_hash}', 'employee', '[2]')
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar datos
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM companies")
    op.execute("DELETE FROM business_groups")
