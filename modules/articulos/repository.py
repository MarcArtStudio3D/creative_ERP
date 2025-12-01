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
            # Insert with default values for mandatory fields to avoid "Field doesn't have a default value" error
            result = session.execute(
                text("""
                    INSERT INTO articulos (
                        codigo, coste, coste_real, porc_dto, margen, margen_min, 
                        tipo_iva, stock_real, stock_fisico_almacen, stock_maximo, stock_minimo,
                        unidades_compradas, importe_acumulado_compras, unidades_vendidas, importe_acumulado_ventas,
                        cantidad_pendiente_recibir, unidades_reservadas, mostrar_web, etiquetas, paquetes
                    ) VALUES (
                        :codigo, 0, 0, 0, 0, 0, 
                        0, 0, 0, 0, 0,
                        0, 0, 0, 0,
                        0, 0, 0, 0, 0
                    )
                """),
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
    
    def search_multi_field(self, search_term: str, limit: int = 500) -> List[dict]:
        """
        Search articles across multiple fields (codigo, descripcion_reducida, codigo_barras)
        Similar to clientes.repository.obtener_todos with filtro parameter
        
        Args:
            search_term: Term to search for
            limit: Maximum results
            
        Returns:
            List of articles matching the search term in any field
        """
        session = self._session()
        try:
            # Get default tarifa for search view
            # Fallback to 1 if configuracion table doesn't exist or is empty
            try:
                tarifa_result = session.execute(
                    text("SELECT id_tarifa_predeterminada FROM configuracion LIMIT 1")
                )
                tarifa_row = tarifa_result.fetchone()
                id_tarifa = tarifa_row[0] if tarifa_row else 1
            except Exception:
                # If table doesn't exist or any other error, default to 1
                id_tarifa = 1

            
            # Search across multiple fields using OR conditions
            sql = """
                SELECT DISTINCT a.id, a.codigo, a.descripcion_reducida, a.codigo_barras, 
                       a.codigo_fabricante, a.stock_real, a.coste, a.margen
                FROM articulos a
                WHERE (
                    UPPER(a.codigo) LIKE :search OR
                    UPPER(a.descripcion_reducida) LIKE :search OR
                    UPPER(a.codigo_barras) LIKE :search OR
                    UPPER(a.codigo_fabricante) LIKE :search
                )
                ORDER BY a.descripcion_reducida ASC
                LIMIT :limit
            """
            
            result = session.execute(
                text(sql),
                {
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
    
    def get_secciones_for_lookup(self) -> str:
        """Get SQL query for sections lookup in DBConsultaView"""
        return "SELECT id, codigo, seccion FROM secciones ORDER BY codigo"
    
    def get_secciones_data(self) -> list:
        """Get sections data as list of dictionaries"""
        session = self._session()
        try:
            result = session.execute(
                text("SELECT id, codigo, seccion FROM secciones ORDER BY codigo")
            )
            rows = result.fetchall()
            return [{
                'id': row[0],
                'codigo': row[1], 
                'seccion': row[2]
            } for row in rows]
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

    def get_familias_for_lookup(self) -> str:
        """Get SQL query for families lookup in DBConsultaView"""
        return "SELECT id, codigo, familia FROM familias ORDER BY codigo"

    def get_familias_data(self, id_seccion: int = None) -> list:
        """Get families data as list of dictionaries. Optionally filter by section id."""
        session = self._session()
        try:
            if id_seccion:
                result = session.execute(
                    text("SELECT id, codigo, familia FROM familias WHERE id_seccion = :sid ORDER BY codigo"),
                    {"sid": id_seccion}
                )
            else:
                result = session.execute(
                    text("SELECT id, codigo, familia FROM familias ORDER BY codigo")
                )

            rows = result.fetchall()
            return [{
                'id': row[0],
                'codigo': row[1],
                'familia': row[2]
            } for row in rows]
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

    def get_subfamilias_for_lookup(self) -> str:
        """Get SQL query for subfamilies lookup in DBConsultaView"""
        return "SELECT id, codigo, subfamilia FROM subfamilias ORDER BY codigo"

    def get_subfamilias_data(self, id_familia: int = None) -> list:
        """Get subfamilias data as list of dictionaries. Optionally filter by family id."""
        session = self._session()
        try:
            if id_familia:
                result = session.execute(
                    text("SELECT id, codigo, subfamilia FROM subfamilias WHERE id_familia = :fid ORDER BY codigo"),
                    {"fid": id_familia}
                )
            else:
                result = session.execute(text("SELECT id, codigo, subfamilia FROM subfamilias ORDER BY codigo"))

            rows = result.fetchall()
            return [{
                'id': row[0],
                'codigo': row[1],
                'subfamilia': row[2]
            } for row in rows]
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
    
    def get_default_tarifa(self) -> int:
        """
        Get default tarifa ID from configuration
        Returns 1 if not configured
        """
        session = self._session()
        try:
            result = session.execute(
                text("SELECT id_tarifa_predeterminada FROM configuracion LIMIT 1")
            )
            row = result.fetchone()
            return row[0] if row and row[0] else 1
        except Exception as e:
            print(f"Error getting default tarifa: {e}")
            return 1
        finally:
            if not self._external_session:
                session.close()
    
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
    
    def get_iva_types(self, pais: str = None) -> List[dict]:
        """
        Get IVA types from TVAIVA table, optionally filtered by country
        
        Args:
            pais: Country code/name to filter by. If None, gets from current company
            
        Returns:
            List of IVA types with id, codigo, descripcion, porcentaje
        """
        session = self._session()
        try:
            # If no country specified, get from current company
            if not pais:
                from core.company_manager import get_current_company_context
                company_ctx = get_current_company_context()
                if company_ctx.get('has_company'):
                    # Get company's country from database
                    from core.db import get_session as get_main_session, set_current_database, get_current_database
                    from core.models import Empresa
                    
                    original_db = get_current_database()
                    set_current_database('main')
                    try:
                        main_session = get_main_session()
                        empresa = main_session.query(Empresa).filter_by(
                            id=company_ctx['company_id']
                        ).first()
                        if empresa:
                            pais = empresa.pais
                            print(f"📍 País de la empresa: {pais}")
                    finally:
                        set_current_database(original_db)
                        main_session.close()
            
            # Default to España if still no country
            if not pais:
                pais = 'España'
                print(f"📍 Usando país por defecto: {pais}")
            
            # First, check if table exists
            try:
                check_sql = """
                    SELECT COUNT(*) as count FROM TVAIVA LIMIT 1
                """
                check_result = session.execute(text(check_sql))
                print(f"✓ Tabla TVAIVA existe")
            except Exception as table_error:
                print(f"❌ Tabla TVAIVA no existe o error: {table_error}")
                return []
            
            # Query TVAIVA table (case-insensitive comparison)
            sql = """
                SELECT id, codigo, descripcion, porcentaje, pais
                FROM TVAIVA
                WHERE LOWER(pais) = LOWER(:pais)
                ORDER BY porcentaje ASC
            """
            
            result = session.execute(text(sql), {"pais": pais})
            iva_types = [dict(row._mapping) for row in result.fetchall()]
            
            if not iva_types:
                # Try without country filter to see if there's any data
                print(f"⚠️ No se encontraron tipos de IVA para país '{pais}', intentando sin filtro...")
                sql_all = "SELECT id, codigo, descripcion, porcentaje, pais FROM TVAIVA ORDER BY porcentaje ASC"
                result_all = session.execute(text(sql_all))
                all_iva = [dict(row._mapping) for row in result_all.fetchall()]
                print(f"📊 Total de tipos de IVA en la tabla: {len(all_iva)}")
                if all_iva:
                    print(f"📋 Países disponibles: {set(row['pais'] for row in all_iva)}")
            
            return iva_types
            
        except Exception as e:
            print(f"❌ Error getting IVA types: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if not self._external_session:
                session.close()
