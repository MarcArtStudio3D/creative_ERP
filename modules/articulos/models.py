"""
Modelos de datos para el módulo de Artículos.
Dataclasses para mantener arquitectura MVC pura sin ORM.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import date
from decimal import Decimal


@dataclass
class Seccion:
    """Modelo para Secciones del almacén"""
    id: Optional[int] = None
    codigo: str = ""
    seccion: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'Seccion':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            codigo=data.get('codigo', ''),
            seccion=data.get('seccion', '')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'codigo': self.codigo,
            'seccion': self.seccion
        }
        if self.id is not None:
            result['id'] = self.id
        return result


@dataclass
class Familia:
    """Modelo para Familias del almacén"""
    id: Optional[int] = None
    codigo: str = ""
    familia: str = ""
    id_seccion: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Familia':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            codigo=data.get('codigo', ''),
            familia=data.get('familia', ''),
            id_seccion=data.get('id_seccion')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'codigo': self.codigo,
            'familia': self.familia,
            'id_seccion': self.id_seccion
        }
        if self.id is not None:
            result['id'] = self.id
        return result


@dataclass
class Subfamilia:
    """Modelo para Subfamilias del almacén"""
    id: Optional[int] = None
    codigo: str = ""
    subfamilia: str = ""
    id_familia: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Subfamilia':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            codigo=data.get('codigo', ''),
            subfamilia=data.get('subfamilia', ''),
            id_familia=data.get('id_familia')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'codigo': self.codigo,
            'subfamilia': self.subfamilia,
            'id_familia': self.id_familia
        }
        if self.id is not None:
            result['id'] = self.id
        return result


@dataclass
class Articulo:
    """Modelo para Artículos"""
    id: Optional[int] = None
    codigo: str = ""
    codigo_barras: Optional[str] = None
    descripcion_reducida: str = ""
    descripcion_ampliada: Optional[str] = None
    id_seccion: Optional[int] = None
    id_familia: Optional[int] = None
    id_subfamilia: Optional[int] = None
    id_proveedor: Optional[int] = None
    coste: Decimal = Decimal('0.00')
    stock_real: Decimal = Decimal('0.00')
    stock_maximo: Decimal = Decimal('0.00')
    stock_minimo: Decimal = Decimal('0.00')
    precio_venta: Decimal = Decimal('0.00')
    iva: Decimal = Decimal('21.00')
    activo: bool = True
    fecha_alta: Optional[date] = None
    fecha_modificacion: Optional[date] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Articulo':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            codigo=data.get('codigo', ''),
            codigo_barras=data.get('codigo_barras'),
            descripcion_reducida=data.get('descripcion_reducida', ''),
            descripcion_ampliada=data.get('descripcion_ampliada'),
            id_seccion=data.get('id_seccion'),
            id_familia=data.get('id_familia'),
            id_subfamilia=data.get('id_subfamilia'),
            id_proveedor=data.get('id_proveedor'),
            coste=Decimal(str(data.get('coste', 0))),
            stock_real=Decimal(str(data.get('stock_real', 0))),
            stock_maximo=Decimal(str(data.get('stock_maximo', 0))),
            stock_minimo=Decimal(str(data.get('stock_minimo', 0))),
            precio_venta=Decimal(str(data.get('precio_venta', 0))),
            iva=Decimal(str(data.get('iva', 21))),
            activo=bool(data.get('activo', True)),
            fecha_alta=data.get('fecha_alta'),
            fecha_modificacion=data.get('fecha_modificacion')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'codigo': self.codigo,
            'codigo_barras': self.codigo_barras,
            'descripcion_reducida': self.descripcion_reducida,
            'descripcion_ampliada': self.descripcion_ampliada,
            'id_seccion': self.id_seccion,
            'id_familia': self.id_familia,
            'id_subfamilia': self.id_subfamilia,
            'id_proveedor': self.id_proveedor,
            'coste': float(self.coste),
            'stock_real': float(self.stock_real),
            'stock_maximo': float(self.stock_maximo),
            'stock_minimo': float(self.stock_minimo),
            'precio_venta': float(self.precio_venta),
            'iva': float(self.iva),
            'activo': self.activo,
            'fecha_alta': self.fecha_alta,
            'fecha_modificacion': self.fecha_modificacion
        }
        if self.id is not None:
            result['id'] = self.id
        return result


@dataclass
class Promocion:
    """Modelo para Promociones de artículos"""
    id: Optional[int] = None
    id_articulo: Optional[int] = None
    descripcion: str = ""
    precio_oferta: Decimal = Decimal('0.00')
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activa: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> 'Promocion':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            id_articulo=data.get('id_articulo'),
            descripcion=data.get('descripcion', ''),
            precio_oferta=Decimal(str(data.get('precio_oferta', 0))),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin'),
            activa=bool(data.get('activa', True))
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'id_articulo': self.id_articulo,
            'descripcion': self.descripcion,
            'precio_oferta': float(self.precio_oferta),
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'activa': self.activa
        }
        if self.id is not None:
            result['id'] = self.id
        return result

