"""
Modelos de datos para el módulo de Artículos
Basado en la estructura original de RedFox SGC (articulo.cpp)
"""

from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional


class Seccion(SQLModel, table=True):
    """Modelo de Sección - Primera división del almacén"""
    __tablename__ = 'secciones'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(max_length=10, unique=True, index=True)
    seccion: str = Field(max_length=100)

    def __repr__(self):
        return f"<Seccion(id={self.id}, codigo='{self.codigo}', seccion='{self.seccion}')>"


class Familia(SQLModel, table=True):
    """Modelo de Familia - Segunda división del almacén (pertenece a una sección)"""
    __tablename__ = 'familias'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_seccion: int = Field(foreign_key="secciones.id")
    codigo: str = Field(max_length=10, unique=True, index=True)
    familia: str = Field(max_length=100)

    def __repr__(self):
        return f"<Familia(id={self.id}, codigo='{self.codigo}', familia='{self.familia}')>"


class Subfamilia(SQLModel, table=True):
    """Modelo de Subfamilia - Tercera división del almacén (pertenece a una familia)"""
    __tablename__ = 'subfamilias'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_familia: int = Field(foreign_key="familias.id")
    codigo: str = Field(max_length=10, unique=True, index=True)
    subfamilia: str = Field(max_length=100)
    id_seccion: Optional[int] = None

    def __repr__(self):
        return f"<Subfamilia(id={self.id}, codigo='{self.codigo}', subfamilia='{self.subfamilia}')>"


class Articulo(SQLModel, table=True):
    """Modelo de Artículo - Refleja la estructura de RedFox SGC"""
    __tablename__ = 'articulos'
    
    # Identificadores
    id: Optional[int] = Field(default=None, primary_key=True)
    id_web: Optional[int] = None

    # Códigos
    codigo: str = Field(max_length=50, unique=True, index=True)
    codigo_barras: Optional[str] = Field(default=None, max_length=50)
    codigo_fabricante: Optional[str] = Field(default=None, max_length=50)
    slug: Optional[str] = Field(default=None, max_length=255)

    # Descripciones
    descripcion: Optional[str] = None
    descripcion_reducida: Optional[str] = Field(default=None, max_length=255)

    # Clasificación
    id_seccion: Optional[int] = None
    id_familia: Optional[int] = None
    id_subfamilia: Optional[int] = None
    id_tipo: Optional[int] = Field(default=None, foreign_key="articulo_tipo.id")

    # Proveedor
    id_proveedor: Optional[int] = None

    # Precios y márgenes
    coste: float = Field(default=0.0)
    coste_real: float = Field(default=0.0)
    precio_venta: float = Field(default=0.0)
    porc_dto: float = Field(default=0.0)
    margen: float = Field(default=0.0)
    margen_min: float = Field(default=0.0)

    # IVA
    id_tipos_iva: Optional[int] = None
    tipo_iva: float = Field(default=0.0)
    pvp_incluye_iva: int = Field(default=0)

    # Stock
    stock_real: float = Field(default=0.0)
    stock_fisico_almacen: float = Field(default=0.0)
    stock_maximo: float = Field(default=0.0)
    stock_minimo: float = Field(default=0.0)
    controlar_stock: bool = Field(default=True)
    localizacion_en_almacen: Optional[str] = Field(default=None, max_length=100)

    # Estadísticas de compras
    fecha_ultima_compra: Optional[date] = None
    unidades_compradas: float = Field(default=0.0)
    importe_acumulado_compras: float = Field(default=0.0)

    # Estadísticas de ventas
    fecha_ultima_venta: Optional[date] = None
    unidades_vendidas: float = Field(default=0.0)
    importe_acumulado_ventas: float = Field(default=0.0)

    # Pendientes
    cantidad_pendiente_recibir: float = Field(default=0.0)
    fecha_prevista_recepcion: Optional[date] = None
    unidades_reservadas: float = Field(default=0.0)

    # Características del producto
    tipo_unidad: Optional[str] = Field(default=None, max_length=20)
    modelo: Optional[str] = Field(default=None, max_length=100)
    talla: Optional[str] = Field(default=None, max_length=50)
    color: Optional[str] = Field(default=None, max_length=50)
    composicion: Optional[str] = Field(default=None, max_length=255)

    # Flags
    kit: bool = Field(default=False)
    mostrar_web: int = Field(default=0)
    articulo_promocionado: bool = Field(default=False)
    mostrar_en_cuadro: bool = Field(default=False)

    # Empaquetado
    etiquetas: int = Field(default=0)
    paquetes: int = Field(default=0)

    # Comentarios
    comentario: Optional[str] = None

    def __repr__(self):
        return f"<Articulo(id={self.id}, codigo='{self.codigo}', descripcion='{self.descripcion_reducida}')>"


class Tarifa(SQLModel, table=True):
    """Tarifas de precios por artículo, país y moneda"""
    __tablename__ = 'tarifas'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_articulo: int = Field(foreign_key="articulos.id")
    id_codigo_tarifa: int
    id_pais: int
    id_monedas: int

    margen: float = Field(default=0.0)
    margen_minimo: float = Field(default=0.0)
    pvp: float = Field(default=0.0)

    def __repr__(self):
        return f"<Tarifa(id={self.id}, id_articulo={self.id_articulo}, pvp={self.pvp})>"


class TarifaTipo(SQLModel, table=True):
    """Tipos de tarifa / códigos de tarifa (lookup)"""
    __tablename__ = 'tarifas_tipo'

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: Optional[str] = Field(default=None, max_length=50, unique=True)
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = None

    def __repr__(self):
        return f"<TarifaTipo(id={self.id}, codigo='{self.codigo}', nombre='{self.nombre}')>"


class ArticuloTipo(SQLModel, table=True):
    """Tipos de artículo (lookup): código + descripción"""
    __tablename__ = 'articulo_tipo'

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: Optional[str] = Field(default=None, max_length=50, unique=True)
    descripcion: str = Field(max_length=255)
    activo: bool = Field(default=True)

    def __repr__(self):
        return f"<ArticuloTipo(id={self.id}, codigo='{self.codigo}', descripcion='{self.descripcion}')>"


class ProveedorFrecuente(SQLModel, table=True):
    """Proveedores frecuentes de un artículo"""
    __tablename__ = 'proveedores_frecuentes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_art: int = Field(foreign_key="articulos.id")
    id_prov: int

    cod_pro: Optional[str] = Field(default=None, max_length=50)
    proveedor: Optional[str] = Field(default=None, max_length=255)
    codigo: Optional[str] = Field(default=None, max_length=50)
    pvd: float = Field(default=0.0)
    pvd_real: float = Field(default=0.0)
    moneda: Optional[str] = Field(default=None, max_length=10)
    descoferta: float = Field(default=0.0)

    def __repr__(self):
        return f"<ProveedorFrecuente(id={self.id}, proveedor='{self.proveedor}')>"


class ArticuloOferta(SQLModel, table=True):
    """Ofertas y promociones de artículos"""
    __tablename__ = 'articulos_ofertas'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_articulo: int = Field(foreign_key="articulos.id")
    id_tarifa: int

    descripcion: Optional[str] = Field(default=None, max_length=255)
    activa: bool = Field(default=False)

    # Tipo de oferta
    oferta32: bool = Field(default=False)
    oferta_dto: bool = Field(default=False)
    oferta_precio_final: bool = Field(default=False)
    oferta_web: bool = Field(default=False)

    # Valores de oferta
    unidades: float = Field(default=0.0)
    regalo: float = Field(default=0.0)
    dto_local: float = Field(default=0.0)
    dto_web: float = Field(default=0.0)
    precio_final: float = Field(default=0.0)

    # Fechas
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    def __repr__(self):
        return f"<ArticuloOferta(id={self.id}, descripcion='{self.descripcion}', activa={self.activa})>"


class ArticuloImagen(SQLModel, table=True):
    """Imágenes de artículos"""
    __tablename__ = 'articulos_imagenes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_articulo: int = Field(foreign_key="articulos.id", unique=True)

    imagen1: Optional[str] = Field(default=None, max_length=255)
    imagen2: Optional[str] = Field(default=None, max_length=255)
    imagen3: Optional[str] = Field(default=None, max_length=255)
    imagen4: Optional[str] = Field(default=None, max_length=255)

    def __repr__(self):
        return f"<ArticuloImagen(id_articulo={self.id_articulo})>"


class AcumArticulo(SQLModel, table=True):
    """Acumulados de artículos por empresa (estadísticas mensuales)"""
    __tablename__ = 'acum_articulos'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_articulo: int = Field(foreign_key="articulos.id")
    id_empresa: int

    # Unidades vendidas por mes
    unid_vent_enero: float = Field(default=0.0)
    unid_vent_febrero: float = Field(default=0.0)
    unid_vent_marzo: float = Field(default=0.0)
    unid_vent_abril: float = Field(default=0.0)
    unid_vent_mayo: float = Field(default=0.0)
    unid_vent_junio: float = Field(default=0.0)
    unid_vent_julio: float = Field(default=0.0)
    unid_vent_agosto: float = Field(default=0.0)
    unid_vent_septiembre: float = Field(default=0.0)
    unid_vent_octubre: float = Field(default=0.0)
    unid_vent_noviembre: float = Field(default=0.0)
    unid_vent_diciembre: float = Field(default=0.0)

    # Importe acumulado por mes
    acum_vent_enero: float = Field(default=0.0)
    acum_vent_febrero: float = Field(default=0.0)
    acum_vent_marzo: float = Field(default=0.0)
    acum_vent_abril: float = Field(default=0.0)
    acum_vent_mayo: float = Field(default=0.0)
    acum_vent_junio: float = Field(default=0.0)
    acum_vent_julio: float = Field(default=0.0)
    acum_vent_agosto: float = Field(default=0.0)
    acum_vent_septiembre: float = Field(default=0.0)
    acum_vent_octubre: float = Field(default=0.0)
    acum_vent_noviembre: float = Field(default=0.0)
    acum_vent_diciembre: float = Field(default=0.0)

    def __repr__(self):
        return f"<AcumArticulo(id_articulo={self.id_articulo}, id_empresa={self.id_empresa})>"


class Kit(SQLModel, table=True):
    """Componentes de kits (artículos compuestos)"""
    __tablename__ = 'kits'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo_kit: str = Field(max_length=50)
    id_componente: int = Field(foreign_key="articulos.id")
    cantidad: float = Field(default=1.0)

    def __repr__(self):
        return f"<Kit(codigo_kit='{self.codigo_kit}', id_componente={self.id_componente}, cantidad={self.cantidad})>"
