from typing import List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.db import get_session, get_database_url
from core.models import Empresa, BusinessGroup


def remove_accents(input_str):
    import unicodedata
    if input_str is None:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', str(input_str))
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

class EmpresaRepository:
    def __init__(self, session=None):
        self._external_session = session
        self._main_session = None
        self._engine = None

    def _session(self):
        # Si se proporcionó una sesión externa, usarla (útil para tests)
        if self._external_session:
            return self._external_session
            
        # Si ya tenemos una sesión dedicada a main, verificar que esté activa
        if self._main_session:
            try:
                # Simple check to see if session is valid
                self._main_session.execute(text("SELECT 1"))
                return self._main_session
            except Exception:
                # Si falla, recrear
                if self._main_session:
                    self._main_session.close()
                self._main_session = None

        # Crear conexión explícita a la base de datos 'main'
        # Esto es necesario porque el contexto global de la app puede estar apuntando
        # a una base de datos de empresa (tenant), pero las empresas siempre están en 'main'.
        try:
            if not self._engine:
                db_url = get_database_url('main')
                self._engine = create_engine(db_url)
            
            Session = sessionmaker(bind=self._engine)
            self._main_session = Session()
            return self._main_session
        except Exception as e:
            print(f"Error connecting to main database: {e}")
            # Fallback to global session if specific connection fails
            return get_session()

    def obtener_todos(self) -> List[Empresa]:
        sess = self._session()
        return sess.query(Empresa).order_by(Empresa.nombre_fiscal).all()
        
    def obtener_grupos(self) -> List[BusinessGroup]:
        """Obtiene todos los grupos empresariales de la BD principal."""
        sess = self._session()
        return sess.query(BusinessGroup).all()

    def obtener_por_id(self, id_: int) -> Optional[Empresa]:
        sess = self._session()
        return sess.query(Empresa).get(id_)

    def guardar(self, empresa: Empresa) -> Empresa:
        sess = self._session()
        sess.add(empresa)
        sess.commit()
        sess.refresh(empresa)
        return empresa

    def borrar(self, empresa: Empresa) -> None:
        sess = self._session()
        sess.delete(empresa)
        sess.commit()

    # Métodos para utilidades geográficas (Países y CP)
    def obtener_paises(self):
        """Obtiene la lista de países (es, fr) desde la base de datos auxiliar."""
        import sqlite3
        import os
        
        # Ruta a la base de datos
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, 'datos', 'paises_es_fr.sqlite')
        
        if not os.path.exists(db_path):
            return []
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT pais_es, pais_fr FROM paises ORDER BY pais_es")
            paises = cursor.fetchall()
            conn.close()
            return paises
        except Exception as e:
            print(f"Error en repositorio obteniendo países: {e}")
            return []

    def buscar_poblacion(self, cp: str, pais: str):
        """
        Busca población por código postal.
        Retorna una tupla: (resultados, db_path, db_config)
        resultados: lista de tuplas (poblacion, provincia) si es único, o raw rows si hay varios
        db_path: ruta a la BD usada
        db_config: configuración de columnas (para uso en vista si es necesario)
        """
        import sqlite3
        import os
        
        # Map country names to database files and table structures
        country_db_map = {
            'francia': ('france.db', 'villes', 'code_postal', 'nom_standard_majuscule', 'dep_nom'),
            'france': ('france.db', 'villes', 'code_postal', 'nom_standard_majuscule', 'dep_nom'),
            'españa': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia'),
            'spain': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia'),
            'espagne': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia')
        }
        
        db_config = country_db_map.get(pais.lower())
        if not db_config:
            # Default to France if country not found
            db_config = country_db_map['francia']
        
        db_filename, table_name, cp_col, city_col, prov_col = db_config
        
        # Connect to country database
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, 'datos', db_filename)
        
        if not os.path.exists(db_path):
            return [], db_path, db_config
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query for postal code
            cursor.execute(f"""
                SELECT {city_col}, {prov_col} 
                FROM {table_name} 
                WHERE {cp_col} = ? 
                ORDER BY {city_col}
            """, (cp,))
            
            results = cursor.fetchall()
            conn.close()
            
            return results, db_path, db_config
            
        except Exception as e:
            print(f"Error en repositorio buscando población: {e}")
            return [], db_path, db_config


    def buscar_codigos_postales(self, poblacion: str, pais: str):
        """
        Busca códigos postales por nombre de población.
        Retorna una tupla: (resultados, db_path, db_config)
        """
        import sqlite3
        import os
        
        # Map country names to database files and table structures
        country_db_map = {
            'francia': ('france.db', 'villes', 'code_postal', 'nom_standard_majuscule', 'dep_nom'),
            'france': ('france.db', 'villes', 'code_postal', 'nom_standard_majuscule', 'dep_nom'),
            'españa': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia'),
            'spain': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia'),
            'espagne': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia')
        }
        
        db_config = country_db_map.get(pais.lower())
        if not db_config:
            # Default to France if country not found
            db_config = country_db_map['francia']
        
        db_filename, table_name, cp_col, city_col, prov_col = db_config
        
        # Connect to country database
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, 'datos', db_filename)
        
        if not os.path.exists(db_path):
            return [], db_path, db_config
            
        try:
            conn = sqlite3.connect(db_path)
            conn.create_function("REMOVE_ACCENTS", 1, remove_accents)
            cursor = conn.cursor()
            
            # Query for city name (case-insensitive and accent-insensitive LIKE search)
            # We select ROWID to help the view filter specifically these results
            cursor.execute(f"""
                SELECT {cp_col}, {city_col}, {prov_col}, ROWID 
                FROM {table_name} 
                WHERE REMOVE_ACCENTS({city_col}) LIKE ? 
                ORDER BY {city_col}, {cp_col}
                LIMIT 500
            """, (f"%{remove_accents(poblacion).upper()}%",))
            
            results = cursor.fetchall()
            conn.close()
            
            return results, db_path, db_config
            
        except Exception as e:
            print(f"Error en repositorio buscando códigos postales: {e}")
            return [], db_path, db_config

    def __del__(self):
        # Cerrar sesión y engine al destruir el repositorio
        if self._main_session:
            try:
                self._main_session.close()
            except:
                pass
        if self._engine:
            try:
                self._engine.dispose()
            except:
                pass
