from typing import List, Optional, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.db import get_session


class ArticuloRepository:
    def __init__(self, session: Session = None):
        self._external_session = session
    
    def _session(self) -> Session:
        """Get database session"""
        if self._external_session:
            return self._external_session
        return get_session()
    
    # ==================== CRUD Operations ====================
    
    def get_by_id(self, articulo_id: int) -> Optional[dict]:
        """Get article by ID"""
        session = self._session()
        try:
            result = session.execute(
                text("SELECT * FROM articulos WHERE id = :id LIMIT 1"),
                {"id": articulo_id}
            )
            row = result.fetchone()
            return dict(row._mapping) if row else None
        finally:
            if not self._external_session:
                session.close()
    
    def get_next(self, current_id: int) -> Optional[dict]:
        """Get next article after current ID"""
        session = self._session()
        try:
            result = session.execute(
                text("SELECT * FROM articulos WHERE id > :id ORDER BY id ASC LIMIT 1"),
                {"id": current_id}
            )
            row = result.fetchone()
            return dict(row._mapping) if row else None
        finally:
            if not self._external_session:
                session.close()
    
    def get_prev(self, current_id: int) -> Optional[dict]:
        """Get previous article before current ID"""
        session = self._session()
        try:
            result = session.execute(
                text("SELECT * FROM articulos WHERE id < :id ORDER BY id DESC LIMIT 1"),
                {"id": current_id}
            )
            row = result.fetchone()
            return dict(row._mapping) if row else None
        finally:
            if not self._external_session:
                session.close()
    
    def get_all(self, limit: int = None, offset: int = 0, order_by: str = "descripcion_reducida", order_dir: str = "ASC") -> List[dict]:
        """Get all articles with optional pagination and ordering"""
        session = self._session()
        try:
            query = f"SELECT * FROM articulos ORDER BY {order_by} {order_dir}"
            if limit:
                query += f" LIMIT {limit} OFFSET {offset}"
            
            result = session.execute(text(query))
            return [dict(row._mapping) for row in result.fetchall()]
        finally:
            if not self._external_session:
                session.close()
    
    def count_all(self) -> int:
        """Get total count of articles"""
        session = self._session()
        try:
            result = session.execute(text("SELECT COUNT(*) as total FROM articulos"))
            return result.fetchone()[0]
        finally:
            if not self._external_session:
                session.close()
    
    def create(self, codigo: str = None) -> Optional[int]:
        """
        Create new article with temporary code
        Returns the new article ID
        """
        import random
        session = self._session()
        try:
            temp_code = codigo if codigo else f"_{random.randint(1000, 9999)}_"
            result = session.execute(
                text("INSERT INTO articulos (codigo) VALUES (:codigo)"),
                {"codigo": temp_code}
            )
            session.commit()
            return result.lastrowid
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if not self._external_session:
                session.close()
    
    def update(self, articulo_id: int, data: dict) -> bool:
        """Update article with given data"""
        session = self._session()
        try:
            # Build SET clause dynamically
            set_clauses = []
            params = {"id": articulo_id}
            
            for key, value in data.items():
                set_clauses.append(f"{key} = :{key}")
                params[key] = value
            
            if not set_clauses:
                return True
            
            sql = f"UPDATE articulos SET {', '.join(set_clauses)} WHERE id = :id"
            session.execute(text(sql), params)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if not self._external_session:
                session.close()
    
    def delete(self, articulo_id: int) -> bool:
        """Delete article and related data"""
        session = self._session()
        try:
            # Delete related tarifas first
            session.execute(
                text("DELETE FROM tarifas WHERE id_articulo = :id"),
                {"id": articulo_id}
            )
            
            # Delete article
            session.execute(
                text("DELETE FROM articulos WHERE id = :id"),
                {"id": articulo_id}
            )
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if not self._external_session:
                session.close()
    
    # ==================== Search & Filter ====================
    
    def search(self, search_term: str, field: str = "descripcion_reducida", 
               order_by: str = "descripcion_reducida", order_dir: str = "ASC",
               limit: int = 500) -> List[dict]:
        """
        Search articles by field
        
        Args:
            search_term: Term to search for
            field: Field to search in (descripcion_reducida, codigo, codigo_barras, codigo_fabricante)
            order_by: Field to order by
            order_dir: Order direction (ASC/DESC)
            limit: Maximum results
        """
        session = self._session()
        try:
            # Get default tarifa for search view
            tarifa_result = session.execute(
                text("SELECT id_tarifa_predeterminada FROM configuracion LIMIT 1")
            )
            tarifa_row = tarifa_result.fetchone()
            id_tarifa = tarifa_row[0] if tarifa_row else 1
            
            # Search in vistaart_tarifa view
            sql = f"""
                SELECT id, codigo, descripcion_reducida, codigo_barras, codigo_fabricante,
                       tipo_iva, kit, pvp, pvp_con_iva, stock_fisico_almacen
                FROM vistaart_tarifa
                WHERE tarifa = :tarifa AND {field} LIKE :search
                ORDER BY {order_by} {order_dir}
                LIMIT :limit
            """
            
            result = session.execute(
                text(sql),
                {
                    "tarifa": id_tarifa,
                    "search": f"%{search_term.upper()}%",
                    "limit": limit
                }
            )
            
            return [dict(row._mapping) for row in result.fetchall()]
        finally:
            if not self._external_session:
                session.close()
    
    # ==================== Lookups ====================
    
    def get_seccion(self, seccion_id: int) -> Optional[str]:
        """Get section name by ID"""
        session = self._session()
        try:
            result = session.execute(
                text("SELECT seccion FROM secciones WHERE id = :id"),
                {"id": seccion_id}
            )
            row = result.fetchone()
            return row[0] if row else None
        finally:
            if not self._external_session:
                session.close()
    
    def get_familia(self, familia_id: int) -> Optional[str]:
        """Get family name by ID"""
        session = self._session()
        try:
            result = session.execute(
                text("SELECT familia FROM familias WHERE id = :id"),
                {"id": familia_id}
            )
            row = result.fetchone()
            return row[0] if row else None
        finally:
            if not self._external_session:
                session.close()
    
    def get_subfamilia(self, subfamilia_id: int) -> Optional[str]:
        """Get subfamily name by ID"""
        session = self._session()
        try:
            result = session.execute(
                text("SELECT subfamilia FROM subfamilias WHERE id = :id"),
                {"id": subfamilia_id}
            )
            row = result.fetchone()
            return row[0] if row else None
        finally:
            if not self._external_session:
                session.close()
    
    def get_proveedor(self, proveedor_id: int) -> Optional[Tuple[str, str]]:
        """Get provider code and name by ID. Returns (codigo, proveedor)"""
        session = self._session()
        try:
            result = session.execute(
                text("SELECT codigo, proveedor FROM proveedores WHERE id = :id"),
                {"id": proveedor_id}
            )
            row = result.fetchone()
            return (row[0], row[1]) if row else (None, None)
        finally:
            if not self._external_session:
                session.close()
    
    # ==================== Code Generation ====================
    
    def check_code_exists(self, codigo: str = None, codigo_barras: str = None,
                         codigo_fabricante: str = None, exclude_id: int = None) -> Optional[dict]:
        """
        Check if article with given codes already exists
        Returns the existing article if found
        """
        session = self._session()
        try:
            conditions = []
            params = {}
            
            if codigo:
                conditions.append("codigo = :codigo")
                params["codigo"] = codigo
            if codigo_barras:
                conditions.append("codigo_barras = :codigo_barras")
                params["codigo_barras"] = codigo_barras
            if codigo_fabricante:
                conditions.append("codigo_fabricante = :codigo_fabricante")
                params["codigo_fabricante"] = codigo_fabricante
            
            if not conditions:
                return None
            
            where_clause = " OR ".join(conditions)
            if exclude_id:
                where_clause = f"({where_clause}) AND id != :exclude_id"
                params["exclude_id"] = exclude_id
            
            sql = f"SELECT * FROM articulos WHERE {where_clause} LIMIT 1"
            result = session.execute(text(sql), params)
            row = result.fetchone()
            return dict(row._mapping) if row else None
        finally:
            if not self._external_session:
                session.close()
    
    def get_next_code(self, prefix: str, code_length: int) -> str:
        """
        Generate next sequential code with given prefix
        
        Args:
            prefix: Code prefix (e.g., section+family+subfamily codes)
            code_length: Total length of code
        """
        session = self._session()
        try:
            # Get existing codes with this prefix
            result = session.execute(
                text("SELECT codigo FROM articulos WHERE codigo LIKE :prefix ORDER BY codigo DESC LIMIT 10"),
                {"prefix": f"{prefix}%"}
            )
            
            codes = [row[0] for row in result.fetchall()]
            
            # Calculate next number
            max_num = 0
            for code in codes:
                if code and len(code) >= len(prefix):
                    num_part = code[len(prefix):]
                    if num_part.isdigit():
                        max_num = max(max_num, int(num_part))
            
            # Format next code
            next_num = max_num + 1
            num_length = code_length - len(prefix)
            return f"{prefix}{next_num:0{num_length}d}"
        finally:
            if not self._external_session:
                session.close()
    
    # ==================== Tarifas ====================
    
    def create_tarifas_for_article(self, articulo_id: int) -> bool:
        """Create tarifa entries for new article based on codigotarifa"""
        session = self._session()
        try:
            # Get all tarifa codes
            result = session.execute(
                text("SELECT id, id_pais, id_monedas, margen, margen_min FROM codigotarifa")
            )
            
            for row in result.fetchall():
                session.execute(
                    text("""
                        INSERT INTO tarifas (id_articulo, id_pais, id_monedas, margen, margen_minimo, id_codigo_tarifa)
                        VALUES (:id_articulo, :id_pais, :id_monedas, :margen, :margen_min, :id_codigo)
                    """),
                    {
                        "id_articulo": articulo_id,
                        "id_pais": row[1],
                        "id_monedas": row[2],
                        "margen": row[3],
                        "margen_min": row[4],
                        "id_codigo": row[0]
                    }
                )
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if not self._external_session:
                session.close()
