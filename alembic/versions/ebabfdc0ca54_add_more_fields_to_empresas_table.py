"""add more fields to empresas table

Revision ID: ebabfdc0ca54
Revises: 88c124189360
Create Date: 2025-11-20 02:17:15.434571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebabfdc0ca54'
down_revision: Union[str, Sequence[str], None] = '88c124189360'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Añadir campos adicionales a la tabla empresas

    # Información fiscal adicional
    op.add_column('empresas', sa.Column('forma_juridica', sa.String(100)))  # S.L., S.A., etc.
    op.add_column('empresas', sa.Column('pais', sa.String(100)))
    op.add_column('empresas', sa.Column('dia_cierre_ejercicio', sa.Integer()))
    op.add_column('empresas', sa.Column('mes_cierre_ejercicio', sa.Integer()))
    #pour france
    op.add_column('empresas', sa.Column('siret', sa.String(20)))    
    op.add_column('empresas', sa.Column('ape_naf', sa.String(20)))
    op.add_column('empresas', sa.Column('rcs', sa.String(50)))
    op.add_column('empresas', sa.Column('inscrcion', sa.String(50)))
    # Contacto adicional
    op.add_column('empresas', sa.Column('telefono2', sa.String(16)))
    op.add_column('empresas', sa.Column('movil', sa.String(16)))

    # Datos de acceso a la web 
    op.add_column('empresas', sa.Column('enlace_web', sa.Boolean(), default=False))

    # Datos Internacionales
    op.add_column('empresas', sa.Column('activar_modo_internacional', sa.Boolean(), default=False))
    op.add_column('empresas', sa.Column('actualizar_valores_divisa', sa.Boolean(), default=False))
    op.add_column('empresas', sa.Column('id_moneda_principal', sa.Integer()))
  

    # Configuración fiscal
    op.add_column('empresas', sa.Column('regimen_iva', sa.String(50), default='General'))
    op.add_column('empresas', sa.Column('tipo_retencion', sa.String(50)))
    op.add_column('empresas', sa.Column('aplicar_retencion', sa.Boolean(), default=False))
    op.add_column('empresas', sa.Column('porcentaje_retencion', sa.Float(), default=0.0))
    op.add_column('empresas', sa.Column('exento_iva', sa.Boolean(), default=False))
    op.add_column('empresas', sa.Column('intracomunitario', sa.Boolean(), default=False))
    op.add_column('empresas', sa.Column('digitos_factura', sa.Integer(), default=8))
    op.add_column('empresas', sa.Column('serie_factura', sa.String(10), default='A'))

    # Límites y condiciones comerciales
    op.add_column('empresas', sa.Column('auto_codificar_nuevo_articulo', sa.Boolean(), default=True))
    op.add_column('empresas', sa.Column('tamano_codigo_articulo', sa.Integer(), default=16))
    op.add_column('empresas', sa.Column('id_tarifa_predeterminada', sa.Integer()))
    op.add_column('empresas', sa.Column('margen_beneficio_predeterminado', sa.Float(), default=0.0))
    op.add_column('empresas', sa.Column('margen_minimo_predeterminado', sa.Float(), default=0.0))
    op.add_column('empresas', sa.Column('decimales_en_precios', sa.Integer(), default=2))
    op.add_column('empresas', sa.Column('decimales_en_importes_finales', sa.Integer(), default=2))

   
    # Información adicional
    op.add_column('empresas', sa.Column('sitio_web', sa.String(200)))  # Campo adicional para web
    op.add_column('empresas', sa.Column('comentarios_albaranes', sa.Text()))
    op.add_column('empresas', sa.Column('comentarios_facturas', sa.Text()))
    op.add_column('empresas', sa.Column('ruta_logotipo', sa.String(255)))
    op.add_column('empresas', sa.Column('horario_lunes', sa.String(100)))
    op.add_column('empresas', sa.Column('horario_martes', sa.String(100)))
    op.add_column('empresas', sa.Column('horario_miercoles', sa.String(100)))
    op.add_column('empresas', sa.Column('horario_jueves', sa.String(100)))
    op.add_column('empresas', sa.Column('horario_viernes', sa.String(100)))
    op.add_column('empresas', sa.Column('horario_sabado', sa.String(100)))
    op.add_column('empresas', sa.Column('horario_domingo', sa.String(100)))

    # google calendar
    op.add_column('empresas', sa.Column('google_calendar_id', sa.String(255)))
    op.add_column('empresas', sa.Column('google_calendar_token', sa.String(255)))
    op.add_column('empresas', sa.Column('google_calendar_refresh_token', sa.String(255)))
    op.add_column('empresas', sa.Column('google_calendar_token_expiry', sa.String(255)))

    #contabilidad
    op.add_column('empresas', sa.Column('digitos_cuenta_contable', sa.Integer(), default=8))
    op.add_column('empresas', sa.Column('cuenta_contable_clientes', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_proveedores', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_acreedores', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_venta_mercaderias', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_venta_servicios', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_soportado_general', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_soportado_reducido', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_soportado_superreducido', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_soportado_exento', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_soportado_recargo_equivalencia_general', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_soportado_recargo_equivalencia_reducido', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_soportado_recargo_equivalencia_superreducido', sa.String(50))) 
    op.add_column('empresas', sa.Column('cuenta_contable_iva_soportado_recargo_equivalencia_exento', sa.String(50)))    

    op.add_column('empresas', sa.Column('cuenta_contable_iva_repercutido_general', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_repercutido_reducido', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_repercutido_superreducido', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_repercutido_exento', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_repercutido_recargo_equivalencia_general', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_repercutido_recargo_equivalencia_reducido', sa.String(50)))
    op.add_column('empresas', sa.Column('cuenta_contable_iva_repercutido_recargo_equivalencia_superreducido', sa.String(50))) 
    op.add_column('empresas', sa.Column('cuenta_contable_iva_repercutido_recargo_equivalencia_exento', sa.String(50)))
    # Accesos y seguridad
    op.add_column('empresas', sa.Column('motor_base_datos', sa.String(50), default='sqlite'))
    op.add_column('empresas', sa.Column('ruta_sqlite_general', sa.String(255)))
    op.add_column('empresas', sa.Column('ruta_sqlite_contabilidad', sa.String(255)))

    op.add_column('empresas', sa.Column('host_maria_db', sa.String(100)))
    op.add_column('empresas', sa.Column('puerto_maria_db', sa.Integer(), default=3306))
    op.add_column('empresas', sa.Column('usuario_maria_db', sa.String(100)))
    op.add_column('empresas', sa.Column('contrasena_maria_db', sa.String(100)))
    op.add_column('empresas', sa.Column('nombre_base_datos_maria_db', sa.String(100)))

    op.add_column('empresas', sa.Column('host_postgresql', sa.String(100)))
    op.add_column('empresas', sa.Column('puerto_postgresql', sa.Integer(), default=5432))
    op.add_column('empresas', sa.Column('usuario_postgresql', sa.String(100)))
    op.add_column('empresas', sa.Column('contrasena_postgresql', sa.String(100)))
    op.add_column('empresas', sa.Column('nombre_base_datos_postgresql', sa.String(100)))
    # Metadatos
    op.add_column('empresas', sa.Column('fecha_modificacion', sa.DateTime(), default=sa.func.now()))
    op.add_column('empresas', sa.Column('usuario_modificacion', sa.String(100)))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar las columnas añadidas (en orden inverso)
    op.drop_column('empresas', 'usuario_modificacion')
    op.drop_column('empresas', 'fecha_modificacion')
    op.drop_column('empresas', 'observaciones_internas')
    op.drop_column('empresas', 'sitio_web')
    op.drop_column('empresas', 'facturacion_anual')
    op.drop_column('empresas', 'numero_empleados')
    op.drop_column('empresas', 'sector_actividad')
    op.drop_column('empresas', 'forma_pago_predeterminada')
    op.drop_column('empresas', 'descuento_general')
    op.drop_column('empresas', 'dias_pago')
    op.drop_column('empresas', 'limite_credito')
    op.drop_column('empresas', 'intracomunitario')
    op.drop_column('empresas', 'exento_iva')
    op.drop_column('empresas', 'porcentaje_retencion')
    op.drop_column('empresas', 'tipo_retencion')
    op.drop_column('empresas', 'regimen_iva')
    op.drop_column('empresas', 'swift_bic')
    op.drop_column('empresas', 'iban')
    op.drop_column('empresas', 'numero_cuenta')
    op.drop_column('empresas', 'dc')
    op.drop_column('empresas', 'sucursal')
    op.drop_column('empresas', 'banco')
    op.drop_column('empresas', 'provincia_fiscal')
    op.drop_column('empresas', 'poblacion_fiscal')
    op.drop_column('empresas', 'cp_fiscal')
    op.drop_column('empresas', 'direccion_fiscal')
    op.drop_column('empresas', 'fax')
    op.drop_column('empresas', 'movil_contacto')
    op.drop_column('empresas', 'telefono_contacto')
    op.drop_column('empresas', 'cargo_contacto')
    op.drop_column('empresas', 'persona_contacto')
    op.drop_column('empresas', 'moneda_capital')
    op.drop_column('empresas', 'capital_social')
    op.drop_column('empresas', 'objeto_social')
    op.drop_column('empresas', 'fecha_constitucion')
    op.drop_column('empresas', 'tipo_sociedad')
