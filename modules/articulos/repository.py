from typing import List, Optional, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.db import get_session


class ArticuloRepository:
    def __init__(self, session: Session = None):
        self._external_session = session
    
    def _session(self) -> Session:
        """Obtener la sesión de base de datos a usar (internamente o externa si fue pasada)."""
        if self._external_session:
            return self._external_session
        return get_session()
    
    # ==================== CRUD Operations ====================
    
    def get_by_id(self, articulo_id: int) -> Optional[dict]:
        """Obtener un artículo por su ID"""
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
        """Obtener el siguiente artículo después del ID actual"""
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
        """Obtener el artículo anterior al ID actual"""
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
        """Obtener todos los artículos con paginación y orden opcionales"""
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
        """Obtener el número total de artículos"""
        session = self._session()
        try:
            result = session.execute(text("SELECT COUNT(*) as total FROM articulos"))
            return result.fetchone()[0]
        finally:
            if not self._external_session:
                session.close()
    
    def create(self, codigo: str = None) -> Optional[int]:
        """
        Crear un nuevo artículo con código temporal.
        Devuelve el ID del artículo creado.
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
        """Actualizar un artículo con los campos proporcionados en el diccionario data"""
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
            pass
            session.execute(text(sql), params)
            # Only commit when repository manages the session
            if not self._external_session:
                session.commit()
            return True
        except Exception as e:
            # Rollback only if repository manages the session
            if not self._external_session:
                session.rollback()
            raise e
        finally:
            if not self._external_session:
                session.close()
    
    def delete(self, articulo_id: int) -> bool:
        """Eliminar el artículo y los datos relacionados (tarifas, etc.)"""
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
        Buscar artículos por un campo específico.

        Args:
            search_term: Término a buscar
            field: Campo donde buscar (descripcion_reducida, codigo, codigo_barras, codigo_fabricante)
            order_by: Campo por el que ordenar
            order_dir: Dirección de orden (ASC/DESC)
            limit: Número máximo de resultados
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
        Buscar artículos en varios campos (codigo, descripcion_reducida, codigo_barras).
        Similar a clientes.repository.obtener_todos con parámetro filtro.

        Args:
            search_term: Término a buscar
            limit: Número máximo de resultados

        Returns:
            Lista de artículos que coinciden con el término en cualquiera de los campos
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
        """Obtener el nombre de la sección por su ID"""
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
        """Devolver la consulta SQL para listar secciones en DBConsultaView"""
        return "SELECT id, codigo, seccion FROM secciones ORDER BY codigo"
    
    def get_secciones_data(self) -> list:
        """Obtener datos de secciones como lista de diccionarios"""
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
        """Obtener el nombre de la familia por su ID"""
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
        """Devolver la consulta SQL para listar familias en DBConsultaView"""
        return "SELECT id, codigo, familia FROM familias ORDER BY codigo"

    def get_familias_data(self, id_seccion: int = None) -> list:
        """Obtener datos de familias como lista de diccionarios. Filtrar por id_seccion opcionalmente."""
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
        """Obtener el nombre de la subfamilia por su ID"""
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
        """Devolver la consulta SQL para listar subfamilias en DBConsultaView"""
        return "SELECT id, codigo, subfamilia FROM subfamilias ORDER BY codigo"

    def get_subfamilias_data(self, id_familia: int = None) -> list:
        """Obtener datos de subfamilias como lista de diccionarios. Filtrar por id_familia opcionalmente."""
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

    # ==================== Tarifas tipo (lookup) ====================

    def get_tarifa_tipos(self) -> list:
        """Obtener todos los tipos de tarifa (tabla tarifas_tipo)"""
        session = self._session()
        try:
            # Table tarifas_tipo does not include an 'activo' column in this schema.
            result = session.execute(text("SELECT id, codigo, nombre, descripcion FROM tarifas_tipo ORDER BY nombre"))
            return [dict(row._mapping) for row in result.fetchall()]
        finally:
            if not self._external_session:
                session.close()

    def get_tarifa_tipo(self, tipo_id: int) -> dict | None:
        session = self._session()
        try:
            result = session.execute(text("SELECT id, codigo, nombre, descripcion FROM tarifas_tipo WHERE id = :id LIMIT 1"), {"id": tipo_id})
            row = result.fetchone()
            return dict(row._mapping) if row else None
        finally:
            if not self._external_session:
                session.close()

    def create_tarifa_tipo(self, payload: dict) -> int:
        """Crear un nuevo tipo de tarifa. payload: {'codigo', 'nombre', 'descripcion', 'activo'}"""
        session = self._session()
        try:
            result = session.execute(
                text("INSERT INTO tarifas_tipo (codigo, nombre, descripcion) VALUES (:codigo, :nombre, :descripcion)"),
                {
                    "codigo": payload.get("codigo"),
                    "nombre": payload.get("nombre"),
                    "descripcion": payload.get("descripcion"),
                }
            )
            if not self._external_session:
                session.commit()
            return result.lastrowid
        except Exception:
            if not self._external_session:
                session.rollback()
            raise
        finally:
            if not self._external_session:
                session.close()

    def update_tarifa_tipo(self, tipo_id: int, data: dict) -> bool:
        session = self._session()
        try:
            if not data:
                return True
            set_clauses = []
            params = {"id": tipo_id}
            for key, val in data.items():
                # Avoid trying to update nonexistent 'activo' column
                if key == 'activo':
                    continue
                set_clauses.append(f"{key} = :{key}")
                params[key] = val

            sql = f"UPDATE tarifas_tipo SET {', '.join(set_clauses)} WHERE id = :id"
            session.execute(text(sql), params)
            if not self._external_session:
                session.commit()
            return True
        except Exception:
            if not self._external_session:
                session.rollback()
            raise
        finally:
            if not self._external_session:
                session.close()

    def delete_tarifa_tipo(self, tipo_id: int) -> bool:
        session = self._session()
        try:
            session.execute(text("DELETE FROM tarifas_tipo WHERE id = :id"), {"id": tipo_id})
            if not self._external_session:
                session.commit()
            return True
        except Exception:
            if not self._external_session:
                session.rollback()
            raise
        finally:
            if not self._external_session:
                session.close()
    
    def get_proveedor(self, proveedor_id: int) -> Optional[Tuple[str, str]]:
        """Obtener código y nombre del proveedor por ID. Devuelve (codigo, proveedor)"""
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
        Comprobar si ya existe un artículo con los códigos indicados.
        Devuelve el artículo existente si se encuentra.
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
        Generar el siguiente código secuencial con el prefijo dado.

        Args:
            prefix: Prefijo del código (p.ej. código de sección+familia+subfamilia)
            code_length: Longitud total del código
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
        Obtener el ID de tarifa predeterminada desde la configuración.
        Devuelve 1 si no está configurado.
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
        """Crear entradas de tarifas para un nuevo artículo basadas en codigotarifa"""
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
        Obtener tipos de IVA desde la tabla TVAIVA, filtrando opcionalmente por país.

        Args:
            pais: Código/nombre de país para filtrar. Si es None, se obtiene del contexto de la compañía.

        Returns:
            Lista de tipos de IVA con campos id, codigo, descripcion, porcentaje
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
                            print(f"Company country: {pais}")
                    finally:
                        set_current_database(original_db)
                        main_session.close()
            
            # Default to España if still no country
            if not pais:
                pais = 'España'
                print(f"Using default country: {pais}")
            
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
                print(f"Total IVA types in table: {len(all_iva)}")
                if all_iva:
                    print(f"Available countries: {set(row['pais'] for row in all_iva)}")
            
            return iva_types
            
        except Exception as e:
            print(f"❌ Error getting IVA types: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if not self._external_session:
                session.close()

    # ==================== Ofertas (Promociones) ====================

    def get_oferta_for_article(self, articulo_id: int, id_tarifa: int = None) -> Optional[dict]:
        """Devolver el registro de oferta para el artículo y tarifa indicados (o tarifa por defecto)"""
        session = self._session()
        try:
            if id_tarifa is None:
                id_tarifa = self.get_default_tarifa()

            result = session.execute(
                text("SELECT * FROM articulos_ofertas WHERE id_articulo = :id_articulo AND id_tarifa = :id_tarifa LIMIT 1"),
                {"id_articulo": articulo_id, "id_tarifa": id_tarifa}
            )
            row = result.fetchone()
            return dict(row._mapping) if row else None
        finally:
            if not self._external_session:
                session.close()

    def upsert_oferta(self, articulo_id: int, id_tarifa: int, oferta_data: dict) -> bool:
        """Insertar o actualizar una oferta para el artículo/tarifa indicados.

        oferta_data puede contener: fecha_inicio, fecha_fin, activa, descripcion, oferta_dto, precio_final, etc.
        Solo los campos presentes se actualizan/insertan.
        """
        session = self._session()
        try:
            # See if oferta exists
            existing = session.execute(
                text("SELECT id FROM articulos_ofertas WHERE id_articulo = :id_articulo AND id_tarifa = :id_tarifa LIMIT 1"),
                {"id_articulo": articulo_id, "id_tarifa": id_tarifa}
            ).fetchone()

            params = {"id_articulo": articulo_id, "id_tarifa": id_tarifa}
            # Prepare only recognized keys (avoid SQL injection)
            allowed_keys = set([
                'descripcion', 'activa', 'oferta32', 'oferta_dto', 'oferta_precio_final', 'oferta_web',
                'unidades', 'regalo', 'dto_local', 'dto_web', 'precio_final',
                'fecha_inicio', 'fecha_fin'
            ])

            if existing:
                # Build update
                set_clauses = []
                for k, v in oferta_data.items():
                    if k in allowed_keys:
                        set_clauses.append(f"{k} = :{k}")
                        # Coerce booleans to integers for databases that store booleans as tinyint
                        params[k] = int(v) if isinstance(v, bool) else v

                if not set_clauses:
                    return True

                sql = f"UPDATE articulos_ofertas SET {', '.join(set_clauses)} WHERE id = :id"
                params['id'] = existing[0]
                session.execute(text(sql), params)
                # Debug: fetch back the saved row to inspect values
                try:
                    r = session.execute(text("SELECT id, fecha_inicio, fecha_fin, activa FROM articulos_ofertas WHERE id_articulo = :id_articulo AND id_tarifa = :id_tarifa LIMIT 1"), {"id_articulo": articulo_id, "id_tarifa": id_tarifa}).fetchone()
                except Exception:
                    pass
            else:
                # Insert new oferta - include required columns and fill defaults for missing fields
                # Provide sane defaults for fields that the DB schema may not default
                defaults = {
                    'descripcion': None,
                    'activa': False,
                    'oferta32': False,
                    'oferta_dto': False,
                    'oferta_precio_final': False,
                    'oferta_web': False,
                    'unidades': 0.0,
                    'regalo': 0.0,
                    'dto_local': 0.0,
                    'dto_web': 0.0,
                    'precio_final': 0.0,
                    'fecha_inicio': None,
                    'fecha_fin': None
                }

                # Start with base columns
                cols = ["id_articulo", "id_tarifa"]
                vals = [":id_articulo", ":id_tarifa"]

                # Merge defaults but allow oferta_data to override
                merged = {**defaults, **{k: v for k, v in oferta_data.items() if k in allowed_keys}}

                for k, v in merged.items():
                    cols.append(k)
                    vals.append(f":{k}")
                    params[k] = int(v) if isinstance(v, bool) else v

                sql = f"INSERT INTO articulos_ofertas ({', '.join(cols)}) VALUES ({', '.join(vals)})"
                session.execute(text(sql), params)
                # Debug: fetch back the saved row to inspect values
                try:
                    r = session.execute(text("SELECT id, fecha_inicio, fecha_fin, activa FROM articulos_ofertas WHERE id_articulo = :id_articulo AND id_tarifa = :id_tarifa LIMIT 1"), {"id_articulo": articulo_id, "id_tarifa": id_tarifa}).fetchone()
                except Exception:
                    pass

            # Only commit when repository manages the session
            if not self._external_session:
                session.commit()
            return True
        except Exception:
            # Rollback only if repository manages the session
            if not self._external_session:
                session.rollback()
            raise
        finally:
            if not self._external_session:
                session.close()
