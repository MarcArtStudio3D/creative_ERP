"""
Modelos de datos del módulo de Facturas.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from enum import Enum


class TipoFactura(Enum):
    """Tipos de factura según legislación española."""
    ORDINARIA = "ordinaria"
    RECTIFICATIVA = "rectificativa"
    SIMPLIFICADA = "simplificada"
    PROFORMA = "proforma"


class EstadoFactura(Enum):
    """Estados del ciclo de vida de una factura."""
    BORRADOR = "borrador"
    EMITIDA = "emitida"
    COBRADA = "cobrada"
    IMPAGADA = "impagada"
    ANULADA = "anulada"


@dataclass
class LineaFactura:
    """
    Línea individual de una factura.
    Representa un artículo o servicio facturado.
    """
    id: Optional[int] = None
    factura_id: Optional[int] = None
    articulo_id: Optional[int] = None
    
    descripcion: str = ""              # Descripción del artículo/servicio
    cantidad: Decimal = Decimal("1.0")
    precio_unitario: Decimal = Decimal("0.0")
    descuento: Decimal = Decimal("0.0")  # Porcentaje de descuento
    iva: Decimal = Decimal("21.0")      # Porcentaje de IVA
    
    @property
    def subtotal(self) -> Decimal:
        """Subtotal sin IVA (cantidad × precio - descuento)."""
        base = self.cantidad * self.precio_unitario
        descuento_importe = base * (self.descuento / Decimal("100"))
        return base - descuento_importe
    
    @property
    def importe_iva(self) -> Decimal:
        """Importe del IVA."""
        return self.subtotal * (self.iva / Decimal("100"))
    
    @property
    def total(self) -> Decimal:
        """Total con IVA."""
        return self.subtotal + self.importe_iva


@dataclass
class Factura:
    """
    Factura de venta.
    Documento que registra una transacción comercial.
    """
    id: Optional[int] = None
    numero: str = ""                    # Número de factura (ej: 2024/001)
    serie: str = "A"                    # Serie de la factura
    
    # Fechas
    fecha_emision: date = field(default_factory=date.today)
    fecha_vencimiento: Optional[date] = None
    
    # Relaciones
    cliente_id: int = 0
    proyecto_id: Optional[int] = None   # Opcional: vincular a proyecto
    
    # Tipo y estado
    tipo: TipoFactura = TipoFactura.ORDINARIA
    estado: EstadoFactura = EstadoFactura.BORRADOR
    
    # Líneas de factura
    lineas: List[LineaFactura] = field(default_factory=list)
    
    # Observaciones
    observaciones: str = ""
    
    # Auditoría
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None    # Usuario que la creó
    
    # Datos exportación (Facturae, FacturX)
    exported_facturae: bool = False
    exported_facturx: bool = False
    
    @property
    def base_imponible(self) -> Decimal:
        """Base imponible total (suma de subtotales sin IVA)."""
        return sum((linea.subtotal for linea in self.lineas), Decimal("0.0"))
    
    @property
    def total_iva(self) -> Decimal:
        """Total de IVA."""
        return sum((linea.importe_iva for linea in self.lineas), Decimal("0.0"))
    
    @property
    def total(self) -> Decimal:
        """Total de la factura (base + IVA)."""
        return self.base_imponible + self.total_iva
    
    def agregar_linea(self, linea: LineaFactura):
        """Añade una línea a la factura."""
        linea.factura_id = self.id
        self.lineas.append(linea)
    
    def eliminar_linea(self, index: int):
        """Elimina una línea por su índice."""
        if 0 <= index < len(self.lineas):
            del self.lineas[index]
    
    def generar_numero(self, ultimo_numero: int) -> str:
        """
        Genera el número de factura automáticamente.
        Formato: SERIE/AÑO/NÚMERO
        """
        year = self.fecha_emision.year
        numero = ultimo_numero + 1
        self.numero = f"{self.serie}/{year}/{numero:04d}"
        return self.numero
    
    def puede_modificarse(self) -> bool:
        """Verifica si la factura puede ser modificada."""
        return self.estado in [EstadoFactura.BORRADOR, EstadoFactura.EMITIDA]
    
    def emitir(self):
        """Marca la factura como emitida."""
        if self.estado == EstadoFactura.BORRADOR:
            self.estado = EstadoFactura.EMITIDA
            self.updated_at = datetime.now()
    
    def marcar_cobrada(self):
        """Marca la factura como cobrada."""
        if self.estado == EstadoFactura.EMITIDA:
            self.estado = EstadoFactura.COBRADA
            self.updated_at = datetime.now()
    
    def anular(self):
        """Anula la factura."""
        self.estado = EstadoFactura.ANULADA
        self.updated_at = datetime.now()
