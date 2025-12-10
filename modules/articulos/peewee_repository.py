# peewee_repository.py
# Adaptador sencillo usando playhouse.db_url.connect para exponer la misma API
# pública que ArticuloRepository pero implementada con consultas SQL crudas vía peewee.

import logging
from typing import Any, Dict, List, Optional, Tuple

from playhouse.db_url import connect

from core.db import get_database_url, get_current_database

logger = logging.getLogger(__name__)


def _row_to_dict(cursor, row) -> Dict[str, Any]:
    """Convierte una fila de cursor a dict de forma robusta.

    Soporta varias implementaciones de `row` que pueden venir de distintos DB-API:
    - diccionarios (p. ej. pymysql DictCursor)
    - sqlite3.Row (mapeo por nombre y por índice)
    - tuplas/listas (índice numérico) usando cursor.description
    - objetos con .keys() y .get()

    Se intenta seguir este orden de preferencia y siempre devolver un dict con
    las columnas listadas en cursor.description cuando sea posible.
    """
    if not row:
        return {}

    # Si ya es un dict simple, devolver copia
    try:
        if isinstance(row, dict):
            return dict(row)
    except Exception:
        pass

    # Obtener columnas desde cursor.description si está disponible
    cols = None
    try:
        if getattr(cursor, "description", None):
            cols = [c[0] for c in cursor.description]
    except Exception:
        cols = None

    # Si el row es mapeo (has keys/get), intentar obtener por nombre
    try:
        if hasattr(row, "keys"):
            out = {}
            # Si tenemos columnas, respetarlas en orden
            if cols:
                for col in cols:
                    try:
                        out[col] = row[col]
                    except Exception:
                        try:
                            out[col] = row.get(col)
                        except Exception:
                            try:
                                out[col] = getattr(row, col)
                            except Exception:
                                out[col] = None
            else:
                # No hay descripción: iterar keys
                for k in row.keys():
                    try:
                        out[k] = row[k]
                    except Exception:
                        try:
                            out[k] = row.get(k)
                        except Exception:
                            out[k] = None
            return out
    except Exception:
        pass

    # Si es indexable por entero (tupla/list), mapear por índice usando cols
    try:
        if cols:
            out = {}
            for i, col in enumerate(cols):
                try:
                    out[col] = row[i]
                except Exception:
                    try:
                        out[col] = row[col]
                    except Exception:
                        try:
                            out[col] = row.get(col)
                        except Exception:
                            out[col] = None
            return out
    except Exception:
        pass

    # Último recurso: intentar enumerar el iterable
    try:
        return {str(i): v for i, v in enumerate(row)}
    except Exception:
        return {}


class ArticuloRepository:
    def __init__(self, db=None):
        # Conectar usando la URL configurada para la BD actual
        try:
            if db:
                self.db = db
            else:
                # Store URL and defer connection until needed (lazy connect)
                self._db_url = get_database_url(get_current_database())
                self.db = None
        except Exception:
            logger.exception("Error initializing Peewee DB connection")
            raise

    def _ensure_connection(self):
        """Ensure `self.db` is a DB connection object exposing execute_sql and commit.

        Support both sqlite URLs and mysql+pymysql scheme by using pymysql for the latter.
        This function is defensive: if connection fails, it raises and callers should handle.
        """
        if getattr(self, "db", None) is not None:
            return
        url = getattr(self, "_db_url", None)
        if not url:
            raise RuntimeError("No database URL configured")

        # Handle mysql+pymysql://host... by using pymysql.connect
        try:
            if url.startswith("mysql+pymysql://"):
                import pymysql
                # Parse naive: strip prefix and split user@host/db
                # Use sqlalchemy style URL parsing could be heavier; do simple fallback
                from urllib.parse import urlparse

                parsed = urlparse(url.replace("+pymysql", ""))
                host = parsed.hostname or "localhost"
                port = parsed.port or 3306
                user = parsed.username or ""
                password = parsed.password or ""
                database = parsed.path.lstrip("/")

                conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)

                # Thin wrapper matching `cursor` interface used in this module
                class _PymysqlDBWrapper:
                    def __init__(self, conn):
                        self._conn = conn

                    def execute_sql(self, sql, params=()):
                        cur = self._conn.cursor()
                        cur.execute(sql, params)
                        return cur

                    def commit(self):
                        try:
                            self._conn.commit()
                        except Exception:
                            pass

                self.db = _PymysqlDBWrapper(conn)
                return
        except Exception:
            # fallthrough to try playhouse connect
            pass

        # Try playhouse db_url connect (works for sqlite and some other schemes)
        try:
            self.db = connect(url)
            # Detect paramstyle: sqlite (qmark) vs others (pyformat)
            try:
                if url.startswith("sqlite"):
                    self._paramstyle = "qmark"
                else:
                    self._paramstyle = "pyformat"
            except Exception:
                self._paramstyle = "pyformat"
        except Exception:
            logger.exception("Could not connect to DB using playhouse or pymysql for URL: %s", url)
            raise

    def _format_sql(self, sql: str) -> str:
        """Convert generic %s placeholders to DB paramstyle (qmark => '?').

        We keep using %s in code for readability; convert when needed for sqlite.
        """
        try:
            if getattr(self, "_paramstyle", None) == "qmark":
                return sql.replace("%s", "?")
        except Exception:
            pass
        return sql

    # Helper to execute and fetchone
    def _fetchone(self, sql: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        self._ensure_connection()
        sql2 = self._format_sql(sql)
        cur = self.db.execute_sql(sql2, params)
        row = cur.fetchone()
        # Utilizar _row_to_dict de forma consistente
        try:
            return _row_to_dict(cur, row) if row is not None else None
        except Exception:
            # Fallback simple
            try:
                if isinstance(row, dict):
                    return dict(row)
            except Exception:
                pass
            return None

    def _fetchall(self, sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        self._ensure_connection()
        sql2 = self._format_sql(sql)
        cur = self.db.execute_sql(sql2, params)
        rows = cur.fetchall()

        # Si vienen dicts ya (ej. DictCursor), devolver copias
        try:
            if rows and isinstance(rows[0], dict):
                return [dict(r) for r in rows]
        except Exception:
            pass

        # Mapear usando description + _row_to_dict
        result = []
        try:
            for r in rows:
                try:
                    result.append(_row_to_dict(cur, r))
                except Exception:
                    # último recurso
                    try:
                        result.append({str(i): v for i, v in enumerate(r)})
                    except Exception:
                        result.append({})
            return result
        except Exception:
            # fallback robusto
            out = []
            for r in rows:
                try:
                    out.append(_row_to_dict(cur, r))
                except Exception:
                    try:
                        out.append({str(i): v for i, v in enumerate(r)})
                    except Exception:
                        out.append({})
            return out

    def _execute(self, sql: str, params: Tuple = ()) -> Any:
        self._ensure_connection()
        sql2 = self._format_sql(sql)
        cur = self.db.execute_sql(sql2, params)
        # commit if using transactional DB
        try:
            if hasattr(self.db, "commit"):
                self.db.commit()
        except Exception:
            try:
                # ignore commit failures
                pass
            except Exception:
                pass
        # Devolver cursor o lastrowid si está disponible
        try:
            if hasattr(cur, "lastrowid"):
                return cur.lastrowid
        except Exception:
            pass
        return cur

    # ============= Basic article API =============
    def get_by_id(self, articulo_id: int) -> Optional[dict]:
        sql = "SELECT * FROM articulos WHERE id = %s LIMIT 1"
        return self._fetchone(sql, (articulo_id,))

    def get_all(self, limit: int = None, offset: int = 0, order_by: str = "descripcion_reducida", order_dir: str = "ASC") -> List[dict]:
        ob = order_by if order_by else "descripcion_reducida"
        od = order_dir if order_dir else "ASC"
        sql = f"SELECT * FROM articulos ORDER BY {ob} {od}"
        if limit:
            sql += " LIMIT %s OFFSET %s"
            return self._fetchall(sql, (limit, offset))
        return self._fetchall(sql)

    def count_all(self) -> int:
        sql = "SELECT COUNT(1) FROM articulos"
        self._ensure_connection()
        cur = self.db.execute_sql(sql)
        row = cur.fetchone()
        # If row is mapping, try to get first value
        try:
            if isinstance(row, dict):
                # dict may have numeric keys or column name
                vals = list(row.values())
                return int(vals[0]) if vals else 0
        except Exception:
            pass
        try:
            return int(row[0]) if row else 0
        except Exception:
            return 0

    def get_default_tarifa(self) -> int:
        try:
            row = self._fetchone("SELECT id_tarifa_predeterminada FROM configuracion LIMIT 1")
            return int(row.get("id_tarifa_predeterminada")) if row and row.get("id_tarifa_predeterminada") else 1
        except Exception:
            return 1

    # ============= Oferta (promociones) API =============
    def insert_oferta(self, articulo_id: int, tarifa_id: int, payload: dict) -> Optional[dict]:
        # Ensure sensible defaults to satisfy NOT NULL columns
        if payload is None:
            payload = {}

        # Sanitize placeholder descriptions
        try:
            if isinstance(payload.get("descripcion"), str):
                desc = payload.get("descripcion").strip()
                if desc and desc.lower() == "other":
                    logger.warning("Sanitizando descripcion de oferta no válida en repository.insert_oferta: '%s'", desc)
                    payload["descripcion"] = None
        except Exception:
            pass

        # Helper to decide if payload contains meaningful data
        def _meaningful(v):
            if v is None:
                return False
            if isinstance(v, str) and v.strip() == "":
                return False
            if isinstance(v, bool) and v is False:
                return False
            try:
                if isinstance(v, (int, float)) and float(v) == 0.0:
                    return False
            except Exception:
                pass
            return True

        # If payload has no meaningful values, avoid creating empty oferta
        try:
            has_meaningful = any(_meaningful(payload.get(k)) for k in payload.keys())
        except Exception:
            has_meaningful = False

        if not has_meaningful:
            # Nothing meaningful to insert
            logger.debug("Skipping insert_oferta because payload has no meaningful values: %s", payload)
            return None

        oferta_precio_final = bool(payload.get("oferta_precio_final")) if payload.get("oferta_precio_final") is not None else False
        precio_final = payload.get("precio_final") if payload.get("precio_final") is not None else 0.0
        unidades = payload.get("unidades") if payload.get("unidades") is not None else 0.0
        regalo = payload.get("regalo") if payload.get("regalo") is not None else 0.0
        dto_local = payload.get("dto_local") if payload.get("dto_local") is not None else 0.0
        dto_web = payload.get("dto_web") if payload.get("dto_web") is not None else 0.0
        oferta32 = bool(payload.get("oferta32")) if payload.get("oferta32") is not None else False
        oferta_dto = bool(payload.get("oferta_dto")) if payload.get("oferta_dto") is not None else False
        oferta_web = bool(payload.get("oferta_web")) if payload.get("oferta_web") is not None else False
        activa = bool(payload.get("activa")) if payload.get("activa") is not None else False

        sql = (
            "INSERT INTO articulos_ofertas (id_articulo, id_tarifa, descripcion, fecha_inicio, fecha_fin, activa, unidades, regalo, oferta_precio_final, precio_final, dto_local, dto_web, oferta32, oferta_dto, oferta_web)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        params = (
            articulo_id,
            tarifa_id,
            payload.get("descripcion"),
            payload.get("fecha_inicio"),
            payload.get("fecha_fin"),
            activa,
            unidades,
            regalo,
            oferta_precio_final,
            precio_final,
            dto_local,
            dto_web,
            oferta32,
            oferta_dto,
            oferta_web,
        )
        cur = self._execute(sql, params)
        try:
            last = cur.lastrowid
        except Exception:
            last = None
        row = dict(payload) if payload else {}
        row.update({"id": last, "id_articulo": articulo_id, "id_tarifa": tarifa_id, "oferta_precio_final": oferta_precio_final, "precio_final": precio_final, "unidades": unidades, "regalo": regalo, "dto_local": dto_local, "dto_web": dto_web, "oferta32": oferta32, "oferta_dto": oferta_dto, "oferta_web": oferta_web, "activa": activa})
        return row

    def get_oferta_for_article(self, articulo_id: int, tarifa_id: int = None) -> Optional[dict]:
        sql = "SELECT id, id_articulo, id_tarifa, descripcion, fecha_inicio, fecha_fin, activa, unidades, regalo, oferta_precio_final, precio_final, dto_local, dto_web, oferta32, oferta_dto, oferta_web FROM articulos_ofertas WHERE id_articulo = %s"
        params: Tuple = (articulo_id,)
        if tarifa_id:
            sql += " AND id_tarifa = %s"
            params = (articulo_id, tarifa_id)
        sql += " ORDER BY id DESC LIMIT 1"
        return self._fetchone(sql, params)

    def get_oferta_by_id(self, oferta_id: int) -> Optional[dict]:
        return self._fetchone("SELECT id, id_articulo, id_tarifa, descripcion, fecha_inicio, fecha_fin, activa, unidades, regalo, oferta_precio_final, precio_final, dto_local, dto_web, oferta32, oferta_dto, oferta_web FROM articulos_ofertas WHERE id = %s", (oferta_id,))

    def get_ofertas_for_article(self, articulo_id: int) -> List[dict]:
        return self._fetchall("SELECT id, id_articulo, id_tarifa, descripcion, fecha_inicio, fecha_fin, activa, unidades, regalo, oferta_precio_final, precio_final, dto_local, dto_web, oferta32, oferta_dto, oferta_web FROM articulos_ofertas WHERE id_articulo = %s ORDER BY id DESC", (articulo_id,))

    def upsert_oferta(self, articulo_id: int, tarifa_id: int, payload: dict) -> bool:
        """Actualizar si existe oferta para articulo+tarifa; si no, insertar. Devuelve True si operación OK.

        Añadimos protección para evitar crear ofertas vacías cuando no hay datos significativos.
        """
        # Sanitize description placeholder
        try:
            if payload and isinstance(payload.get("descripcion"), str):
                d = payload.get("descripcion").strip()
                if d and d.lower() == "other":
                    logger.warning("Sanitizando descripcion de oferta no válida en repository.upsert_oferta: '%s'", d)
                    payload["descripcion"] = None
        except Exception:
            pass

        def _meaningful(v):
            if v is None:
                return False
            if isinstance(v, str) and v.strip() == "":
                return False
            if isinstance(v, bool) and v is False:
                return False
            try:
                if isinstance(v, (int, float)) and float(v) == 0.0:
                    return False
            except Exception:
                pass
            return True

        try:
            sql = "SELECT id FROM articulos_ofertas WHERE id_articulo = %s AND id_tarifa = %s ORDER BY id DESC LIMIT 1"
            res = self._fetchone(sql, (articulo_id, tarifa_id))
            existing = res.get("id") if res else None
        except Exception:
            existing = None

        # If payload lacks meaningful data and there is no existing oferta, skip insert
        has_meaningful = False
        try:
            if payload and isinstance(payload, dict):
                has_meaningful = any(_meaningful(payload.get(k)) for k in payload.keys())
        except Exception:
            has_meaningful = False

        if not existing and not has_meaningful:
            logger.debug("Skipping upsert_oferta: no existing oferta and payload has no meaningful values")
            return True

        if existing:
            # build update statements from payload
            set_clauses = []
            params = {"id": existing}
            for k, v in (payload or {}).items():
                set_clauses.append(f"{k} = %s")
                params[k] = v
            if not set_clauses:
                return True
            sql = f"UPDATE articulos_ofertas SET {', '.join(set_clauses)} WHERE id = %s"
            # params order must match placeholders: values then id
            vals = tuple(params[k] for k in params if k != "id") + (params["id"],)
            self._execute(sql, vals)
            return True
        else:
            # insert
            row = self.insert_oferta(articulo_id, tarifa_id, payload or {})
            return True if row else False

    def delete_oferta_by_id(self, oferta_id: int) -> bool:
        self._execute("DELETE FROM articulos_ofertas WHERE id = %s", (oferta_id,))
        return True

    def delete_oferta(self, articulo_id: int, tarifa_id: int) -> bool:
        self._execute("DELETE FROM articulos_ofertas WHERE id_articulo = %s AND id_tarifa = %s", (articulo_id, tarifa_id))
        return True

    def delete_ofertas_for_article(self, articulo_id: int) -> bool:
        """Eliminar todas las ofertas de un artículo (helper para tests)."""
        self._execute("DELETE FROM articulos_ofertas WHERE id_articulo = %s", (articulo_id,))
        return True

    # ============= Lookups =============
    def get_secciones_for_lookup(self) -> str:
        return "SELECT id, codigo, seccion FROM secciones ORDER BY codigo"

    def get_secciones_data(self) -> List[dict]:
        return self._fetchall("SELECT id, codigo, seccion FROM secciones ORDER BY codigo")

    def get_familias_data(self, id_seccion: int = None) -> List[dict]:
        if id_seccion:
            return self._fetchall("SELECT id, codigo, familia, id_seccion FROM familias WHERE id_seccion = %s ORDER BY codigo", (id_seccion,))
        return self._fetchall("SELECT id, codigo, familia, id_seccion FROM familias ORDER BY codigo")

    def get_subfamilias_data(self, id_familia: int = None) -> List[dict]:
        if id_familia:
            return self._fetchall("SELECT id, codigo, subfamilia, id_familia FROM subfamilias WHERE id_familia = %s ORDER BY codigo", (id_familia,))
        return self._fetchall("SELECT id, codigo, subfamilia, id_familia FROM subfamilias ORDER BY codigo")

    def get_proveedor(self, proveedor_id: int) -> Tuple[Optional[str], Optional[str]]:
        row = self._fetchone("SELECT codigo, proveedor FROM proveedores WHERE id = %s LIMIT 1", (proveedor_id,))
        if not row:
            return (None, None)
        return (row.get("codigo"), row.get("proveedor"))

    def get_tarifa_tipos(self) -> List[dict]:
        return self._fetchall("SELECT id, codigo, nombre, descripcion FROM tarifas_tipo ORDER BY nombre")

    # Placeholder stubs for operations not yet migrated (raise to highlight missing)
    def create_tarifas_for_article(self, articulo_id: int) -> bool:
        """Crear entradas de tarifas para un nuevo artículo basadas en codigotarifa.

        Implementación migrada para Peewee: copia la lógica del repository SQLAlchemy
        usando ejecuciones SQL directas (execute_sql) para insertar en `tarifas`.
        """
        try:
            # Read all code-tarifa rows
            rows = self._fetchall("SELECT id, id_pais, id_monedas, margen, margen_min FROM codigotarifa")
            if not rows:
                return True
            for r in rows:
                try:
                    self._execute(
                        "INSERT INTO tarifas (id_articulo, id_pais, id_monedas, margen, margen_minimo, id_codigo_tarifa) VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                            articulo_id,
                            r.get("id_pais"),
                            r.get("id_monedas"),
                            r.get("margen"),
                            r.get("margen_min"),
                            r.get("id"),
                        ),
                    )
                except Exception:
                    # Continue inserting other tarifa rows even if one fails
                    logger.exception("Error inserting tarifa row for articulo %s and codigo %s", articulo_id, r.get("id"))
                    continue
            return True
        except Exception:
            logger.exception("Error creating tarifas for article %s", articulo_id)
            return False

    def update(self, articulo_id: int, data: dict) -> bool:
        # Simple update builder
        if not data:
            return True
        cols = []
        params = []
        for k, v in data.items():
            cols.append(f"{k} = %s")
            params.append(v)
        params.append(articulo_id)
        sql = f"UPDATE articulos SET {', '.join(cols)} WHERE id = %s"
        self._execute(sql, tuple(params))
        return True

    def delete(self, articulo_id: int) -> bool:
        self._execute("DELETE FROM tarifas WHERE id_articulo = %s", (articulo_id,))
        self._execute("DELETE FROM articulos WHERE id = %s", (articulo_id,))
        return True

    def create(self, codigo: str = None) -> Optional[int]:
        """Crear un nuevo artículo con código temporal.

        Inserta valores mínimos y devuelve el id insertado (lastrowid).
        """
        import random
        try:
            temp_code = codigo if codigo else f"_{random.randint(1000,9999)}_"
            # Insert with minimal required fields; columns adjusted to avoid NOT NULL failures
            sql = (
                "INSERT INTO articulos (codigo, coste, coste_real, porc_dto, margen, margen_min, "
                "tipo_iva, stock_real, stock_fisico_almacen, unidades_compradas) "
                "VALUES (%s, 0, 0, 0, 0, 0, 0, 0, 0, 0)"
            )
            cur = self._execute(sql, (temp_code,))
            try:
                return cur.lastrowid
            except Exception:
                return None
        except Exception:
            logger.exception("Error creating new articulo")
            return None

    def get_next(self, current_id: int) -> Optional[dict]:
        sql = "SELECT * FROM articulos WHERE id > %s ORDER BY id ASC LIMIT 1"
        return self._fetchone(sql, (current_id,))

    def get_prev(self, current_id: int) -> Optional[dict]:
        sql = "SELECT * FROM articulos WHERE id < %s ORDER BY id DESC LIMIT 1"
        return self._fetchone(sql, (current_id,))

    # ==================== Search & Filter ====================
    def search(self, search_term: str, field: str = "descripcion_reducida", order_by: str = "descripcion_reducida", order_dir: str = "ASC", limit: int = 500) -> List[dict]:
        """Buscar artículos por un campo específico. Intenta usar `vistaart_tarifa` si existe."""
        try:
            # Try vistaart_tarifa first (may not exist)
            try:
                sql = f"SELECT id, codigo, descripcion_reducida, codigo_barras, codigo_fabricante, tipo_iva, kit, pvp, pvp_con_iva, stock_fisico_almacen FROM vistaart_tarifa WHERE tarifa = %s AND {field} LIKE %s ORDER BY {order_by} {order_dir} LIMIT %s"
                # get default tarifa
                tarifa = self.get_default_tarifa()
                return self._fetchall(sql, (tarifa, f"%{search_term.upper()}%", limit))
            except Exception:
                # Fallback to simple search on articulos
                sql2 = f"SELECT DISTINCT id, codigo, descripcion_reducida, codigo_barras, codigo_fabricante, stock_real FROM articulos WHERE UPPER({field}) LIKE %s ORDER BY {order_by} {order_dir} LIMIT %s"
                return self._fetchall(sql2, (f"%{search_term.upper()}%", limit))
        except Exception:
            logger.exception("Error searching articles")
            return []

    def search_multi_field(self, search_term: str, limit: int = 500) -> List[dict]:
        try:
            sql = """
                SELECT DISTINCT a.id, a.codigo, a.descripcion_reducida, a.codigo_barras,
                       a.codigo_fabricante, a.stock_real, a.coste, a.margen
                FROM articulos a
                WHERE (
                    UPPER(a.codigo) LIKE %s OR
                    UPPER(a.descripcion_reducida) LIKE %s OR
                    UPPER(a.codigo_barras) LIKE %s OR
                    UPPER(a.codigo_fabricante) LIKE %s
                )
                ORDER BY a.descripcion_reducida ASC
                LIMIT %s
            """
            q = f"%{search_term.upper()}%"
            return self._fetchall(sql, (q, q, q, q, limit))
        except Exception:
            logger.exception("Error in search_multi_field")
            return []

    # ==================== Code checks & generation ====================
    def check_code_exists(self, codigo: str = None, codigo_barras: str = None, codigo_fabricante: str = None, exclude_id: int = None) -> Optional[dict]:
        """Comprobar si ya existe un artículo con los códigos indicados. Devuelve el artículo si existe."""
        conditions = []
        params = []
        if codigo:
            conditions.append("codigo = %s")
            params.append(codigo)
        if codigo_barras:
            conditions.append("codigo_barras = %s")
            params.append(codigo_barras)
        if codigo_fabricante:
            conditions.append("codigo_fabricante = %s")
            params.append(codigo_fabricante)
        if not conditions:
            return None
        where = " OR ".join(conditions)
        sql = f"SELECT * FROM articulos WHERE ({where})"
        if exclude_id:
            sql += " AND id != %s"
            params.append(exclude_id)
        sql += " LIMIT 1"
        try:
            return self._fetchone(sql, tuple(params))
        except Exception:
            logger.exception("Error checking existing code")
            return None

    def get_next_code(self, prefix: str, code_length: int) -> str:
        """Calcular el siguiente código secuencial con el prefijo dado."""
        try:
            like_pattern = f"{prefix}%"
            sql = "SELECT codigo FROM articulos WHERE codigo LIKE %s ORDER BY codigo DESC LIMIT 10"
            rows = self._fetchall(sql, (like_pattern,))
            codes = [r.get("codigo") for r in rows if r.get("codigo")]
            max_num = 0
            for code in codes:
                if len(code) >= len(prefix):
                    num_part = code[len(prefix):]
                    if num_part.isdigit():
                        max_num = max(max_num, int(num_part))
            next_num = max_num + 1
            num_length = max(1, code_length - len(prefix))
            return f"{prefix}{next_num:0{num_length}d}"
        except Exception:
            logger.exception("Error generating next code")
            # Fallback simple
            import random
            return f"ART{random.randint(10000,99999)}"

    # ==================== Lookups single-item getters ====================
    def get_seccion(self, seccion_id: int) -> Optional[str]:
        row = self._fetchone("SELECT seccion FROM secciones WHERE id = %s LIMIT 1", (seccion_id,))
        return row.get("seccion") if row else None

    def get_familia(self, familia_id: int) -> Optional[str]:
        row = self._fetchone("SELECT familia FROM familias WHERE id = %s LIMIT 1", (familia_id,))
        return row.get("familia") if row else None

    def get_subfamilia(self, subfamilia_id: int) -> Optional[str]:
        row = self._fetchone("SELECT subfamilia FROM subfamilias WHERE id = %s LIMIT 1", (subfamilia_id,))
        return row.get("subfamilia") if row else None

    # ==================== Articulo tipo & IVA lookups ====================
    def get_articulo_tipo_por_codigo(self, codigo: str) -> dict | None:
        try:
            row = self._fetchone("SELECT id, codigo, descripcion, requiere_ean, proveedor_flag FROM articulo_tipo WHERE LOWER(codigo) = LOWER(%s) LIMIT 1", (codigo,))
            return row
        except Exception:
            # fallback try with ilike
            try:
                row = self._fetchone("SELECT id, codigo, descripcion, requiere_ean, proveedor_flag FROM articulo_tipo WHERE codigo LIKE %s LIMIT 1", (codigo,))
                return row
            except Exception:
                logger.exception("Error looking up articulo tipo by codigo")
                return None

    def get_iva_types(self, pais: str = None) -> List[dict]:
        try:
            if pais:
                sql = "SELECT id, codigo, descripcion, porcentaje FROM TVAIVA WHERE pais = %s OR pais IS NULL ORDER BY codigo"
                return self._fetchall(sql, (pais,))
            sql2 = "SELECT id, codigo, descripcion, porcentaje FROM TVAIVA ORDER BY codigo"
            return self._fetchall(sql2)
        except Exception:
            logger.exception("Error getting IVA types")
            return []
