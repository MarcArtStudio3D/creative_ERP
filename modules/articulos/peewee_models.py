"""
Modelos Peewee para el módulo de Artículos.
Migración completa desde SQLModel a Peewee.
"""

from datetime import date
from peewee import (
    Model,
    AutoField,
    CharField,
    TextField,
    IntegerField,
    FloatField,
    BooleanField,
    DateField,
    DateTimeField,
    ForeignKeyField,
)

from core.peewee_db import database_proxy


class BaseModel(Model):
    """Modelo base que usa el proxy de base de datos."""
    class Meta:
        database = database_proxy


class Seccion(BaseModel):
    """Modelo de Sección - Primera división del almacén"""
    id = AutoField(primary_key=True)
    codigo = CharField(max_length=10, unique=True, index=True)
    seccion = CharField(max_length=100)

    class Meta:
        table_name = 'secciones'


class Familia(BaseModel):
    """Modelo de Familia - Segunda división del almacén"""
    id = AutoField(primary_key=True)
    id_seccion = ForeignKeyField(Seccion, backref='familias', on_delete='CASCADE')
    codigo = CharField(max_length=10, unique=True, index=True)
    familia = CharField(max_length=100)

    class Meta:
        table_name = 'familias'


class Subfamilia(BaseModel):
    """Modelo de Subfamilia - Tercera división del almacén"""
    id = AutoField(primary_key=True)
    id_familia = ForeignKeyField(Familia, backref='subfamilias', on_delete='CASCADE')
    codigo = CharField(max_length=10, unique=True, index=True)
    subfamilia = CharField(max_length=100)
    id_seccion = IntegerField(null=True)

    class Meta:
        table_name = 'subfamilias'


class ArticuloTipo(BaseModel):
    """Modelo de Tipo de Artículo"""
    id = AutoField(primary_key=True)
    codigo = CharField(max_length=10, unique=True, index=True)
    descripcion = CharField(max_length=100)
    requiere_ean = BooleanField(default=False)
    proveedor = BooleanField(default=False)

    class Meta:
        table_name = 'articulo_tipo'


class Articulo(BaseModel):
    """Modelo de Artículo - Refleja la estructura de RedFox SGC"""
    
    # Identificadores
    id = AutoField(primary_key=True)
    id_web = IntegerField(null=True)
    
    # Códigos
    codigo = CharField(max_length=50, unique=True, index=True)
    codigo_barras = CharField(max_length=50, null=True)
    codigo_fabricante = CharField(max_length=50, null=True)
    slug = CharField(max_length=255, null=True)
    
    # Descripciones
    descripcion = TextField(null=True)
    descripcion_reducida = CharField(max_length=255, null=True)
    
    # Clasificación
    id_seccion = IntegerField(null=True)
    id_familia = IntegerField(null=True)
    id_subfamilia = IntegerField(null=True)
    id_tipo = ForeignKeyField(ArticuloTipo, null=True, backref='articulos', on_delete='SET NULL')
    
    # Proveedor
    id_proveedor = IntegerField(null=True)
    
    # Precios y márgenes
    coste = FloatField(default=0.0)
    coste_real = FloatField(default=0.0)
    precio_venta = FloatField(default=0.0)
    porc_dto = FloatField(default=0.0)
    margen = FloatField(default=0.0)
    margen_min = FloatField(default=0.0)
    
    # IVA
    id_tipos_iva = IntegerField(null=True)
    tipo_iva = FloatField(default=0.0)
    pvp_incluye_iva = IntegerField(default=0)
    
    # Stock
    stock_real = FloatField(default=0.0)
    stock_fisico_almacen = FloatField(default=0.0)
    stock_minimo = FloatField(default=0.0)
    stock_maximo = FloatField(default=0.0)
    
    # Control
    activo = BooleanField(default=True)
    publicar_web = BooleanField(default=False)
    destacado_web = BooleanField(default=False)
    
    # Fechas
    fecha_alta = DateField(default=date.today)
    fecha_modificacion = DateTimeField(null=True)
    fecha_ultima_compra = DateField(null=True)
    fecha_ultima_venta = DateField(null=True)
    
    # Dimensiones y peso
    largo = FloatField(default=0.0)
    ancho = FloatField(default=0.0)
    alto = FloatField(default=0.0)
    peso = FloatField(default=0.0)
    volumen = FloatField(default=0.0)
    
    # Unidades
    unidad_medida = CharField(max_length=10, null=True)
    unidades_por_caja = IntegerField(default=1)
    
    # Observaciones
    observaciones = TextField(null=True)
    notas_internas = TextField(null=True)
    
    class Meta:
        table_name = 'articulos'


class TarifaTipo(BaseModel):
    """Modelo de Tipo de Tarifa"""
    id = AutoField(primary_key=True)
    codigo = CharField(max_length=10, unique=True)
    descripcion = CharField(max_length=100)
    activa = BooleanField(default=True)

    class Meta:
        table_name = 'tarifa_tipo'


class Tarifa(BaseModel):
    """Modelo de Tarifa de Artículo"""
    id = AutoField(primary_key=True)
    id_articulo = ForeignKeyField(Articulo, backref='tarifas', on_delete='CASCADE')
    id_tarifa_tipo = ForeignKeyField(TarifaTipo, backref='tarifas', on_delete='CASCADE')
    precio = FloatField(default=0.0)
    porc_dto = FloatField(default=0.0)
    precio_final = FloatField(default=0.0)

    class Meta:
        table_name = 'tarifas'
        indexes = (
            (('id_articulo', 'id_tarifa_tipo'), True),  # Unique constraint
        )


class Promocion(BaseModel):
    """Modelo de Promoción/Oferta de Artículo"""
    id = AutoField(primary_key=True)
    id_articulo = ForeignKeyField(Articulo, backref='promociones', on_delete='CASCADE')
    descripcion = CharField(max_length=255)
    fecha_inicio = DateField()
    fecha_fin = DateField()
    tipo_promocion = CharField(max_length=20)  # '3x2', 'dto', 'pvp', 'web'
    
    # Para 3x2
    por_cada = IntegerField(null=True)
    regalo = IntegerField(null=True)
    
    # Para descuentos
    dto_local = FloatField(null=True)
    dto_web = FloatField(null=True)
    
    # Para PVP fijo
    precio_final = FloatField(null=True)
    
    activa = BooleanField(default=True)

    class Meta:
        table_name = 'promociones'

