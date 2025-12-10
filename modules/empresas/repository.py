"""
Repository Peewee para el módulo de Empresas.
Migración completa desde SQLModel a Peewee.
"""

import logging
import os
import sqlite3
from typing import List, Optional

from core.peewee_db import get_current_database, set_current_database
from core.models import BusinessGroup, Empresa


def remove_accents(input_str):
    """Elimina acentos de una cadena."""
    import unicodedata

    if input_str is None:
        return ""
    nfkd_form = unicodedata.normalize("NFKD", str(input_str))
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


class EmpresaRepository:
    """Repository para gestión de empresas usando Peewee."""

    def __init__(self):
        """Inicializar repository."""
        # Con Peewee no necesitamos gestionar sesiones manualmente
        pass

    def _ensure_main_db(self):
        """Asegura que estamos en la BD main."""
        current = get_current_database()
        if current != "main":
            set_current_database("main")
        return current

    def obtener_todos(self) -> List[Empresa]:
        """Obtiene todas las empresas."""
        try:
            original_db = self._ensure_main_db()
            try:
                empresas = list(Empresa.select().order_by(Empresa.nombre_fiscal))
                return empresas
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            logging.getLogger(__name__).exception("Error obteniendo empresas: %s", e)
            return []

    def obtener_grupos(self) -> List[BusinessGroup]:
        """Obtiene todos los grupos empresariales."""
        try:
            original_db = self._ensure_main_db()
            try:
                grupos = list(BusinessGroup.select())
                return grupos
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            logging.getLogger(__name__).exception("Error obteniendo grupos: %s", e)
            return []

    def obtener_por_id(self, id_: int) -> Optional[Empresa]:
        """Obtiene una empresa por ID."""
        try:
            original_db = self._ensure_main_db()
            try:
                empresa = Empresa.get_by_id(id_)
                return empresa
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Empresa.DoesNotExist:
            return None
        except Exception as e:
            logging.getLogger(__name__).exception("Error obteniendo empresa por ID: %s", e)
            return None

    def guardar(self, empresa: Empresa) -> Empresa:
        """Guarda una empresa (crea o actualiza)."""
        try:
            original_db = self._ensure_main_db()
            try:
                empresa.save()
                return empresa
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            logging.getLogger(__name__).exception("Error guardando empresa: %s", e)
            raise

    def borrar(self, empresa: Empresa) -> None:
        """Elimina una empresa."""
        try:
            original_db = self._ensure_main_db()
            try:
                empresa.delete_instance()
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            logging.getLogger(__name__).exception("Error borrando empresa: %s", e)
            raise

    # Métodos para utilidades geográficas (Países y CP)
    def obtener_paises(self):
        """Obtiene la lista de países (es, fr) desde la base de datos auxiliar."""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, "datos", "paises_es_fr.sqlite")

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
            logging.getLogger(__name__).exception("Error obteniendo países: %s", e)
            return []

    def buscar_poblacion(self, cp: str, pais: str):
        """
        Busca población por código postal.
        Retorna una tupla: (resultados, db_path, db_config)
        """
        # Map country names to database files and table structures
        country_db_map = {
            "francia": ("france.db", "villes", "code_postal", "nom_standard_majuscule", "dep_nom"),
            "france": ("france.db", "villes", "code_postal", "nom_standard_majuscule", "dep_nom"),
            "españa": ("spain.sqlite", "cp_info", "cp", "poblacion", "provincia"),
            "spain": ("spain.sqlite", "cp_info", "cp", "poblacion", "provincia"),
            "espagne": ("spain.sqlite", "cp_info", "cp", "poblacion", "provincia"),
        }

        db_config = country_db_map.get(pais.lower())
        if not db_config:
            db_config = country_db_map["francia"]

        db_filename, table_name, cp_col, city_col, prov_col = db_config

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, "datos", db_filename)

        if not os.path.exists(db_path):
            return [], None, None

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = f"SELECT {city_col}, {prov_col} FROM {table_name} WHERE {cp_col} = ?"
            cursor.execute(query, (cp,))
            results = cursor.fetchall()
            conn.close()

            if len(results) == 1:
                return results, db_path, db_config
            elif len(results) > 1:
                return results, db_path, db_config
            else:
                return [], db_path, db_config

        except Exception as e:
            logging.getLogger(__name__).exception("Error buscando población: %s", e)
            return [], None, None

    def buscar_cp_por_poblacion(self, poblacion: str, pais: str):
        """Busca códigos postales por nombre de población."""
        country_db_map = {
            "francia": ("france.db", "villes", "code_postal", "nom_standard_majuscule", "dep_nom"),
            "france": ("france.db", "villes", "code_postal", "nom_standard_majuscule", "dep_nom"),
            "españa": ("spain.sqlite", "cp_info", "cp", "poblacion", "provincia"),
            "spain": ("spain.sqlite", "cp_info", "cp", "poblacion", "provincia"),
            "espagne": ("spain.sqlite", "cp_info", "cp", "poblacion", "provincia"),
        }

        db_config = country_db_map.get(pais.lower())
        if not db_config:
            db_config = country_db_map["francia"]

        db_filename, table_name, cp_col, city_col, prov_col = db_config

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, "datos", db_filename)

        if not os.path.exists(db_path):
            return []

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Búsqueda case-insensitive
            query = f"SELECT {cp_col}, {city_col}, {prov_col} FROM {table_name} WHERE LOWER({city_col}) LIKE LOWER(?)"
            cursor.execute(query, (f"%{poblacion}%",))
            results = cursor.fetchall()
            conn.close()

            return results

        except Exception as e:
            logging.getLogger(__name__).exception("Error buscando CP por población: %s", e)
            return []

