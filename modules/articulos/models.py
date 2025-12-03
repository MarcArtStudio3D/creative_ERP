"""
Modelos de datos para el módulo de Artículos
Basado en la estructura original de RedFox SGC (articulo.cpp)
"""

from sqlalchemy import Integer, String, Float, Date, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime
from typing import Optional
from core.db import Base


class Seccion(Base):
    """Modelo de Sección - Primera división del almacén"""
    __tablename__ = 'secciones'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    seccion: Mapped[str] = mapped_column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<Seccion(id={self.id}, codigo='{self.codigo}', seccion='{self.seccion}')>"


class Familia(Base):
    """Modelo de Familia - Segunda división del almacén (pertenece a una sección)"""
    __tablename__ = 'familias'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_seccion: Mapped[int] = mapped_column(Integer, ForeignKey('secciones.id'), nullable=False)
    codigo: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    familia: Mapped[str] = mapped_column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<Familia(id={self.id}, codigo='{self.codigo}', familia='{self.familia}')>"


class Subfamilia(Base):
    """Modelo de Subfamilia - Tercera división del almacén (pertenece a una familia)"""
    __tablename__ = 'subfamilias'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_familia: Mapped[int] = mapped_column(Integer, ForeignKey('familias.id'), nullable=False)
    codigo: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    subfamilia: Mapped[str] = mapped_column(String(100), nullable=False)
    id_seccion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<Subfamilia(id={self.id}, codigo='{self.codigo}', subfamilia='{self.subfamilia}')>"


class Articulo(Base):
    """Modelo de Artículo - Refleja la estructura de RedFox SGC"""
    __tablename__ = 'articulos'
    
    # Identificadores
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_web: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Códigos
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    codigo_barras: Mapped[Optional[str]] = mapped_column(String(50))
    codigo_fabricante: Mapped[Optional[str]] = mapped_column(String(50))
    slug: Mapped[Optional[str]] = mapped_column(String(255))  # URL-friendly name
    
    # Descripciones
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    descripcion_reducida: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Clasificación
    id_seccion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    id_familia: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    id_subfamilia: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Proveedor
    id_proveedor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Precios y márgenes
    coste: Mapped[float] = mapped_column(Float, default=0.0)
    coste_real: Mapped[float] = mapped_column(Float, default=0.0)
    # Precio de venta base del artículo
    precio_venta: Mapped[float] = mapped_column(Float, default=0.0)
    porc_dto: Mapped[float] = mapped_column(Float, default=0.0)  # Descuento del proveedor
    margen: Mapped[float] = mapped_column(Float, default=0.0)  # Margen de beneficio %
    margen_min: Mapped[float] = mapped_column(Float, default=0.0)  # Margen mínimo %
    
    # IVA
    id_tipos_iva: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tipo_iva: Mapped[float] = mapped_column(Float, default=0.0)
    pvp_incluye_iva: Mapped[int] = mapped_column(Integer, default=0)
    
    # Stock
    stock_real: Mapped[float] = mapped_column(Float, default=0.0)
    stock_fisico_almacen: Mapped[float] = mapped_column(Float, default=0.0)
    stock_maximo: Mapped[float] = mapped_column(Float, default=0.0)
    stock_minimo: Mapped[float] = mapped_column(Float, default=0.0)
    controlar_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    localizacion_en_almacen: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Estadísticas de compras
    fecha_ultima_compra: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    unidades_compradas: Mapped[float] = mapped_column(Float, default=0.0)
    importe_acumulado_compras: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Estadísticas de ventas
    fecha_ultima_venta: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    unidades_vendidas: Mapped[float] = mapped_column(Float, default=0.0)
    importe_acumulado_ventas: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Pendientes
    cantidad_pendiente_recibir: Mapped[float] = mapped_column(Float, default=0.0)
    fecha_prevista_recepcion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    unidades_reservadas: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Características del producto
    tipo_unidad: Mapped[Optional[str]] = mapped_column(String(20))  # ud, kg, m, etc.
    modelo: Mapped[Optional[str]] = mapped_column(String(100))
    talla: Mapped[Optional[str]] = mapped_column(String(50))
    color: Mapped[Optional[str]] = mapped_column(String(50))
    composicion: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Flags
    kit: Mapped[bool] = mapped_column(Boolean, default=False)
    mostrar_web: Mapped[int] = mapped_column(Integer, default=0)
    articulo_promocionado: Mapped[bool] = mapped_column(Boolean, default=False)
    mostrar_en_cuadro: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Empaquetado
    etiquetas: Mapped[int] = mapped_column(Integer, default=0)
    paquetes: Mapped[int] = mapped_column(Integer, default=0)
    
    # Comentarios
    comentario: Mapped[Optional[str]] = mapped_column(Text)
    
    def __repr__(self):
        return f"<Articulo(id={self.id}, codigo='{self.codigo}', descripcion='{self.descripcion_reducida}')>"


class Tarifa(Base):
    """Tarifas de precios por artículo, país y moneda"""
    __tablename__ = 'tarifas'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_articulo: Mapped[int] = mapped_column(Integer, ForeignKey('articulos.id'), nullable=False)
    id_codigo_tarifa: Mapped[int] = mapped_column(Integer, nullable=False)
    id_pais: Mapped[int] = mapped_column(Integer, nullable=False)
    id_monedas: Mapped[int] = mapped_column(Integer, nullable=False)
    
    margen: Mapped[float] = mapped_column(Float, default=0.0)
    margen_minimo: Mapped[float] = mapped_column(Float, default=0.0)
    pvp: Mapped[float] = mapped_column(Float, default=0.0)
    
    def __repr__(self):
        return f"<Tarifa(id={self.id}, id_articulo={self.id_articulo}, pvp={self.pvp})>"


class TarifaTipo(Base):
    """Tipos de tarifa / códigos de tarifa (lookup)"""
    __tablename__ = 'tarifas_tipo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        {'sqlite_autoincrement': True},
    )

    def __repr__(self):
        return f"<TarifaTipo(id={self.id}, codigo='{self.codigo}', nombre='{self.nombre}')>"


class ProveedorFrecuente(Base):
    """Proveedores frecuentes de un artículo"""
    __tablename__ = 'proveedores_frecuentes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_art: Mapped[int] = mapped_column(Integer, ForeignKey('articulos.id'), nullable=False)
    id_prov: Mapped[int] = mapped_column(Integer, nullable=False)
    
    cod_pro: Mapped[Optional[str]] = mapped_column(String(50))  # Código del proveedor
    proveedor: Mapped[Optional[str]] = mapped_column(String(255))  # Nombre del proveedor
    codigo: Mapped[Optional[str]] = mapped_column(String(50))  # Código del artículo en el proveedor
    pvd: Mapped[float] = mapped_column(Float, default=0.0)  # Precio venta distribuidor
    pvd_real: Mapped[float] = mapped_column(Float, default=0.0)  # PVD real con descuentos
    moneda: Mapped[Optional[str]] = mapped_column(String(10))
    descoferta: Mapped[float] = mapped_column(Float, default=0.0)  # Descuento oferta
    
    def __repr__(self):
        return f"<ProveedorFrecuente(id={self.id}, proveedor='{self.proveedor}')>"


class ArticuloOferta(Base):
    """Ofertas y promociones de artículos"""
    __tablename__ = 'articulos_ofertas'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_articulo: Mapped[int] = mapped_column(Integer, ForeignKey('articulos.id'), nullable=False)
    id_tarifa: Mapped[int] = mapped_column(Integer, nullable=False)
    
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))
    activa: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Tipo de oferta
    oferta32: Mapped[bool] = mapped_column(Boolean, default=False)  # 3x2, etc.
    oferta_dto: Mapped[bool] = mapped_column(Boolean, default=False)  # Descuento %
    oferta_precio_final: Mapped[bool] = mapped_column(Boolean, default=False)  # Precio fijo
    oferta_web: Mapped[bool] = mapped_column(Boolean, default=False)  # Oferta web
    
    # Valores de oferta
    unidades: Mapped[float] = mapped_column(Float, default=0.0)  # Para 3x2: compra X
    regalo: Mapped[float] = mapped_column(Float, default=0.0)  # Para 3x2: lleva Y gratis
    dto_local: Mapped[float] = mapped_column(Float, default=0.0)  # Descuento local %
    dto_web: Mapped[float] = mapped_column(Float, default=0.0)  # Descuento web %
    precio_final: Mapped[float] = mapped_column(Float, default=0.0)  # Precio final oferta
    
    # Fechas
    fecha_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    def __repr__(self):
        return f"<ArticuloOferta(id={self.id}, descripcion='{self.descripcion}', activa={self.activa})>"


class ArticuloImagen(Base):
    """Imágenes de artículos"""
    __tablename__ = 'articulos_imagenes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_articulo: Mapped[int] = mapped_column(Integer, ForeignKey('articulos.id'), unique=True, nullable=False)
    
    imagen1: Mapped[Optional[str]] = mapped_column(String(255))  # URL o path
    imagen2: Mapped[Optional[str]] = mapped_column(String(255))
    imagen3: Mapped[Optional[str]] = mapped_column(String(255))
    imagen4: Mapped[Optional[str]] = mapped_column(String(255))
    
    def __repr__(self):
        return f"<ArticuloImagen(id_articulo={self.id_articulo})>"


class AcumArticulo(Base):
    """Acumulados de artículos por empresa (estadísticas mensuales)"""
    __tablename__ = 'acum_articulos'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_articulo: Mapped[int] = mapped_column(Integer, ForeignKey('articulos.id'), nullable=False)
    id_empresa: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Unidades vendidas por mes
    unid_vent_enero: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_febrero: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_marzo: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_abril: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_mayo: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_junio: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_julio: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_agosto: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_septiembre: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_octubre: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_noviembre: Mapped[float] = mapped_column(Float, default=0.0)
    unid_vent_diciembre: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Importe acumulado por mes
    acum_vent_enero: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_febrero: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_marzo: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_abril: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_mayo: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_junio: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_julio: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_agosto: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_septiembre: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_octubre: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_noviembre: Mapped[float] = mapped_column(Float, default=0.0)
    acum_vent_diciembre: Mapped[float] = mapped_column(Float, default=0.0)
    
    def __repr__(self):
        return f"<AcumArticulo(id_articulo={self.id_articulo}, id_empresa={self.id_empresa})>"


class Kit(Base):
    """Componentes de kits (artículos compuestos)"""
    __tablename__ = 'kits'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_kit: Mapped[str] = mapped_column(String(50), nullable=False)  # Código del artículo kit
    id_componente: Mapped[int] = mapped_column(Integer, ForeignKey('articulos.id'), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, default=1.0)
    
    def __repr__(self):
        return f"<Kit(codigo_kit='{self.codigo_kit}', id_componente={self.id_componente}, cantidad={self.cantidad})>"
