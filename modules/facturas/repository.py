"""
Repositorio para el acceso a datos de Facturas.
Implementa el patrón Repository para aislar la lógica de base de datos.
"""

from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

from core.repositories import BaseRepository
from modules.facturas.models import Factura, LineaFactura, EstadoFactura, TipoFactura


class FacturaRepository(BaseRepository[Factura]):
    """
    Repositorio de facturas.
    Maneja toda la persistencia de facturas en la base de datos.
    """
    
    def __init__(self, db_connection):
        super().__init__(db_connection, "facturas")
    
    def get_by_numero(self, numero: str) -> Optional[Factura]:
        """Busca una factura por su número."""
        query = "SELECT * FROM facturas WHERE numero = ?"
        row = self.db.execute(query, (numero,)).fetchone()
        return self._row_to_entity(row) if row else None
    
    def get_by_cliente(self, cliente_id: int) -> List[Factura]:
        """Obtiene todas las facturas de un cliente."""
        query = """
            SELECT * FROM facturas 
            WHERE cliente_id = ? 
            ORDER BY fecha_emision DESC
        """
        rows = self.db.execute(query, (cliente_id,)).fetchall()
        return [self._row_to_entity(row) for row in rows]
    
    def get_by_estado(self, estado: EstadoFactura) -> List[Factura]:
        """Obtiene facturas por estado."""
        query = "SELECT * FROM facturas WHERE estado = ? ORDER BY fecha_emision DESC"
        rows = self.db.execute(query, (estado.value,)).fetchall()
        return [self._row_to_entity(row) for row in rows]
    
    def get_pendientes_cobro(self) -> List[Factura]:
        """Obtiene facturas emitidas pero no cobradas."""
        query = """
            SELECT * FROM facturas 
            WHERE estado = ? 
            ORDER BY fecha_vencimiento ASC
        """
        rows = self.db.execute(query, (EstadoFactura.EMITIDA.value,)).fetchall()
        return [self._row_to_entity(row) for row in rows]
    
    def get_by_fecha_range(self, fecha_desde: date, fecha_hasta: date) -> List[Factura]:
        """Obtiene facturas en un rango de fechas."""
        query = """
            SELECT * FROM facturas 
            WHERE fecha_emision BETWEEN ? AND ?
            ORDER BY fecha_emision DESC
        """
        rows = self.db.execute(query, (fecha_desde, fecha_hasta)).fetchall()
        return [self._row_to_entity(row) for row in rows]
    
    def get_ultimo_numero(self, serie: str, year: int) -> int:
        """
        Obtiene el último número de factura para una serie y año.
        Útil para generar el siguiente número.
        """
        query = """
            SELECT MAX(CAST(SUBSTR(numero, -4) AS INTEGER)) as ultimo
            FROM facturas 
            WHERE serie = ? AND CAST(SUBSTR(numero, 3, 4) AS INTEGER) = ?
        """
        row = self.db.execute(query, (serie, year)).fetchone()
        return row['ultimo'] if row and row['ultimo'] else 0
    
    def save(self, factura: Factura) -> Factura:
        """
        Guarda una factura (insert o update).
        También guarda sus líneas.
        """
        if factura.id is None:
            return self._insert(factura)
        else:
            return self._update(factura)
    
    def _insert(self, factura: Factura) -> Factura:
        """Inserta una nueva factura."""
        query = """
            INSERT INTO facturas (
                numero, serie, fecha_emision, fecha_vencimiento,
                cliente_id, proyecto_id, tipo, estado,
                observaciones, created_at, updated_at, created_by,
                exported_facturae, exported_facturx
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor = self.db.execute(query, (
            factura.numero,
            factura.serie,
            factura.fecha_emision,
            factura.fecha_vencimiento,
            factura.cliente_id,
            factura.proyecto_id,
            factura.tipo.value,
            factura.estado.value,
            factura.observaciones,
            factura.created_at,
            factura.updated_at,
            factura.created_by,
            factura.exported_facturae,
            factura.exported_facturx
        ))
        
        factura.id = cursor.lastrowid
        
        # Guardar líneas
        self._save_lineas(factura)
        
        self.db.commit()
        return factura
    
    def _update(self, factura: Factura) -> Factura:
        """Actualiza una factura existente."""
        query = """
            UPDATE facturas SET
                numero = ?, serie = ?, fecha_emision = ?, fecha_vencimiento = ?,
                cliente_id = ?, proyecto_id = ?, tipo = ?, estado = ?,
                observaciones = ?, updated_at = ?,
                exported_facturae = ?, exported_facturx = ?
            WHERE id = ?
        """
        
        factura.updated_at = datetime.now()
        
        self.db.execute(query, (
            factura.numero,
            factura.serie,
            factura.fecha_emision,
            factura.fecha_vencimiento,
            factura.cliente_id,
            factura.proyecto_id,
            factura.tipo.value,
            factura.estado.value,
            factura.observaciones,
            factura.updated_at,
            factura.exported_facturae,
            factura.exported_facturx,
            factura.id
        ))
        
        # Actualizar líneas (eliminar y recrear)
        self.db.execute("DELETE FROM lineas_factura WHERE factura_id = ?", (factura.id,))
        self._save_lineas(factura)
        
        self.db.commit()
        return factura
    
    def _save_lineas(self, factura: Factura):
        """Guarda las líneas de una factura."""
        query = """
            INSERT INTO lineas_factura (
                factura_id, articulo_id, descripcion,
                cantidad, precio_unitario, descuento, iva
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        for linea in factura.lineas:
            self.db.execute(query, (
                factura.id,
                linea.articulo_id,
                linea.descripcion,
                str(linea.cantidad),
                str(linea.precio_unitario),
                str(linea.descuento),
                str(linea.iva)
            ))
    
    def delete(self, factura_id: int) -> bool:
        """
        Elimina una factura y sus líneas.
        Solo se pueden eliminar facturas en estado BORRADOR.
        """
        # Verificar estado
        factura = self.get_by_id(factura_id)
        if not factura or factura.estado != EstadoFactura.BORRADOR:
            return False
        
        # Eliminar líneas primero (integridad referencial)
        self.db.execute("DELETE FROM lineas_factura WHERE factura_id = ?", (factura_id,))
        
        # Eliminar factura
        self.db.execute("DELETE FROM facturas WHERE id = ?", (factura_id,))
        self.db.commit()
        return True
    
    def _row_to_entity(self, row) -> Factura:
        """Convierte una fila de la base de datos a una entidad Factura."""
        if not row:
            return None
        
        factura = Factura(
            id=row['id'],
            numero=row['numero'],
            serie=row['serie'],
            fecha_emision=date.fromisoformat(row['fecha_emision']),
            fecha_vencimiento=date.fromisoformat(row['fecha_vencimiento']) if row['fecha_vencimiento'] else None,
            cliente_id=row['cliente_id'],
            proyecto_id=row['proyecto_id'],
            tipo=TipoFactura(row['tipo']),
            estado=EstadoFactura(row['estado']),
            observaciones=row['observaciones'] or "",
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at']),
            created_by=row['created_by'],
            exported_facturae=bool(row['exported_facturae']),
            exported_facturx=bool(row['exported_facturx'])
        )
        
        # Cargar líneas
        factura.lineas = self._load_lineas(factura.id)
        
        return factura
    
    def _load_lineas(self, factura_id: int) -> List[LineaFactura]:
        """Carga las líneas de una factura."""
        query = "SELECT * FROM lineas_factura WHERE factura_id = ? ORDER BY id"
        rows = self.db.execute(query, (factura_id,)).fetchall()
        
        lineas = []
        for row in rows:
            linea = LineaFactura(
                id=row['id'],
                factura_id=row['factura_id'],
                articulo_id=row['articulo_id'],
                descripcion=row['descripcion'],
                cantidad=Decimal(row['cantidad']),
                precio_unitario=Decimal(row['precio_unitario']),
                descuento=Decimal(row['descuento']),
                iva=Decimal(row['iva'])
            )
            lineas.append(linea)
        
        return lineas
