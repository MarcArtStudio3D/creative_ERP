"""Fix client table name and migrate data

Revision ID: e401056e286b
Revises: 1cb380bca415
Create Date: 2025-11-18 14:36:24.817061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e401056e286b'
down_revision: Union[str, Sequence[str], None] = '1cb380bca415'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Migrar datos de clients a clientes
    # Primero, obtener el máximo ID actual en clientes para evitar conflictos
    result = op.get_bind().execute(sa.text("SELECT COALESCE(MAX(id), 0) FROM clientes"))
    max_id = result.fetchone()[0]
    
    # Insertar datos de clients en clientes, asignando nuevos IDs
    op.get_bind().execute(sa.text("""
        INSERT INTO clientes (
            id, codigo_cliente, nombre, nombre_fiscal, cif_nif_siren, 
            email, direccion1, id_pais, fecha_alta, acumulado_ventas, 
            ventas_ejercicio, riesgo_maximo, deuda_actual, importe_pendiente, 
            bloqueado, porc_dto_cliente, recargo_equivalencia, irpf, grupo_iva, 
            dia_pago1, dia_pago2, importe_a_cuenta, vales, visa1_caduca_mes, 
            visa2_caduca_mes, visa1_caduca_ano, visa2_caduca_ano, visa1_cod_valid, 
            visa2_cod_valid, id_divisa, id_idioma_documentos
        )
        SELECT 
            id + :max_id, 
            'CLI-' || (id + :max_id), 
            name, 
            name, 
            vat_number, 
            email, 
            address, 
            1,  -- id_pais por defecto (asumiendo España)
            datetime('now'), 
            0.0,  -- acumulado_ventas
            0.0,  -- ventas_ejercicio
            0.0,  -- riesgo_maximo
            0.0,  -- deuda_actual
            0.0,  -- importe_pendiente
            0,    -- bloqueado
            0.0,  -- porc_dto_cliente
            0,    -- recargo_equivalencia
            0,    -- irpf
            1,    -- grupo_iva
            1,    -- dia_pago1
            15,   -- dia_pago2
            0.0,  -- importe_a_cuenta
            0.0,  -- vales
            1,    -- visa1_caduca_mes
            1,    -- visa2_caduca_mes
            2025, -- visa1_caduca_ano
            2025, -- visa2_caduca_ano
            0,    -- visa1_cod_valid
            0,    -- visa2_cod_valid
            1,    -- id_divisa
            1     -- id_idioma_documentos
        FROM clients
    """), {"max_id": max_id})
    
    # Actualizar las referencias en invoices
    op.get_bind().execute(sa.text("""
        UPDATE invoices 
        SET client_id = client_id + :max_id
        WHERE client_id IN (SELECT id FROM clients)
    """), {"max_id": max_id})
    
    # Eliminar la tabla clients
    op.drop_table('clients')


def downgrade() -> None:
    """Downgrade schema."""
    # Recrear tabla clients
    op.create_table('clients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('vat_number', sa.String(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Nota: No podemos deshacer completamente la migración de datos
    # porque los IDs han cambiado
