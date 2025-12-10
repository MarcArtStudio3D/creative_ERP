#!/usr/bin/env python3
"""
Módulo de integración con Qt para gestión de empresas y bases de datos
Ejemplo de cómo integrar la selección de empresa con el cambio automático de base de datos
"""

import logging
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))


class CompanyDatabaseManager:
    """Gestor de bases de datos por empresa para integración con Qt."""

    def __init__(self):
        self.current_company_id = None
        self.company_info = None

    def select_company(self, company_id: int) -> bool:
        """
        Selecciona una empresa y configura su base de datos.
        Retorna True si la selección fue exitosa.
        """
        try:
            # Usar el sistema Peewee
            from core.peewee_db import set_database_for_company as peewee_set_db
            from core.peewee_db import get_company_database_info

            # Usar el nuevo sistema Peewee
            peewee_set_db(company_id)

            # Obtener información de la empresa
            self.company_info = get_company_database_info(company_id)
            self.current_company_id = company_id

            logging.getLogger(__name__).info(
                "Company %s selected: %s",
                company_id,
                self.company_info.get("company_name"),
            )
            logging.getLogger(__name__).debug(
                "DB engine: %s", self.company_info.get("motor_base_datos")
            )
            logging.getLogger(__name__).debug(
                "Database: %s", self.company_info.get("database_name")
            )

            return True

        except Exception:
            logging.getLogger(__name__).exception(
                "Error seleccionando empresa %s", company_id
            )
            self.current_company_id = None
            self.company_info = None
            return False

    def get_current_company(self) -> dict | None:
        """Obtiene información de la empresa actualmente seleccionada."""
        if not self.company_info:
            return None
        return self.company_info.copy()

    def get_available_companies(self) -> list:
        """
        Obtiene la lista de empresas disponibles desde la base de datos principal.
        Migrado a Peewee.
        """
        try:
            from core.peewee_db import get_current_database, set_current_database
            from core.models import Empresa

            # Guardar base de datos actual
            original_db = get_current_database()

            # Cambiar a base de datos principal
            set_current_database("main")

            try:
                # Query con Peewee
                empresas = Empresa.select().where(Empresa.activa == 1)

                companies = []
                for empresa in empresas:
                    companies.append(
                        {
                            "id": empresa.id,
                            "codigo": empresa.codigo_empresa,
                            "nombre": empresa.nombre_fiscal,
                            "motor_bd": empresa.motor_base_datos,
                            "bd_mariadb": empresa.nombre_base_datos_maria_db,
                            "bd_postgresql": empresa.nombre_base_datos_postgresql,
                        }
                    )

                return companies

            finally:
                # Restaurar base de datos original
                if original_db:
                    set_current_database(original_db)

        except Exception:
            logging.getLogger(__name__).exception("ERROR getting companies")
            return []

    def validate_company_database(self, company_id: int) -> dict:
        """
        Valida que la configuración de base de datos de una empresa sea correcta.
        Retorna un diccionario con el estado de validación.
        Migrado a Peewee.
        """
        try:
            from core.peewee_db import get_company_database_info, create_database

            info = get_company_database_info(company_id)

            # Intentar conectar con Peewee
            try:
                db = create_database(info["database_url"])
                # Test de conexión simple
                db.execute_sql("SELECT 1")
                db.close()
            except Exception as e:
                raise Exception(f"Error de conexión Peewee: {str(e)}")

            return {"valid": True, "message": "Conexión exitosa", "company_info": info}

        except Exception as e:
            return {
                "valid": False,
                "message": f"Error de conexión: {str(e)}",
                "company_info": None,
            }

    def update_company_database_config(self, company_id: int, config: dict) -> bool:
        """
        Actualiza la configuración de base de datos de una empresa.
        config debe contener: motor_base_datos, nombre_base_datos_maria_db/postgresql, etc.
        Migrado a Peewee.
        """
        try:
            from core.peewee_db import get_current_database, set_current_database
            from core.models import Empresa

            # Guardar base de datos actual
            original_db = get_current_database()

            # Cambiar a base de datos principal
            if original_db != "main":
                set_current_database("main")

            try:
                # Obtener empresa con Peewee
                empresa = Empresa.get_by_id(company_id)

                if not empresa:
                    raise ValueError(f"Empresa con ID {company_id} no encontrada")

                # Actualizar configuración
                for key, value in config.items():
                    if hasattr(empresa, key):
                        setattr(empresa, key, value)

                # Guardar con Peewee
                empresa.save()

                logging.getLogger(__name__).info(
                    "Database configuration updated for company %s", company_id
                )
                return True

            finally:
                # Restaurar BD original
                if original_db and original_db != "main":
                    set_current_database(original_db)

        except Exception:
            logging.getLogger(__name__).exception("ERROR updating configuration")
            return False


# Instancia global del gestor
company_manager = CompanyDatabaseManager()


# Funciones de utilidad para Qt
def setup_company_selection_combo(combo_box):
    """
    Configura un QComboBox para selección de empresas.
    Ejemplo de integración con Qt.
    """
    try:
        # Esto sería código Qt - aquí solo mostramos la lógica
        companies = company_manager.get_available_companies()

        # Limpiar combo
        combo_box.clear()

        # Agregar opción por defecto
        combo_box.addItem("Seleccionar empresa...", None)

        # Agregar empresas
        for company in companies:
            display_text = f"{company['codigo']} - {company['nombre']}"
            combo_box.addItem(display_text, company["id"])

        logging.getLogger(__name__).info(
            "Company combo configured with %d companies", len(companies)
        )

    except Exception:
        logging.getLogger(__name__).exception("ERROR configuring company combo")


def on_company_selected(company_id: int) -> bool:
    """
    Función que se ejecuta cuando se selecciona una empresa en la UI.
    Retorna True si la selección fue exitosa.
    """
    if not company_id:
        logging.getLogger(__name__).warning("No company selected")
        return False

    # Validar configuración antes de seleccionar
    validation = company_manager.validate_company_database(company_id)
    if not validation["valid"]:
        logging.getLogger(__name__).warning(
            "Invalid DB configuration: %s", validation.get("message")
        )
        return False

    # Seleccionar empresa
    success = company_manager.select_company(company_id)
    if success:
        # Aquí se podría emitir una señal Qt para actualizar la UI
        logging.getLogger(__name__).info(
            "Company selected successfully - DB configured"
        )
        return True
    else:
        logging.getLogger(__name__).error("ERROR selecting company")
        return False


def get_current_company_context() -> dict:
    """
    Obtiene el contexto de la empresa actual para usar en la aplicación.
    Útil para mostrar información en la UI.
    """
    company_info = company_manager.get_current_company()
    if not company_info:
        return {
            "has_company": False,
            "company_name": "Ninguna empresa seleccionada",
            "database_info": None,
        }

    return {
        "has_company": True,
        "company_id": company_info["company_id"],
        "company_name": company_info["company_name"],
        "motor_bd": company_info["motor_base_datos"],
        "database_name": company_info["database_name"],
        "database_info": company_info,
    }


if __name__ == "__main__":
    # Ejemplo de uso del gestor de empresas (modo CLI)
    logger = logging.getLogger(__name__)
    logger.info("Creative ERP - Company and Database Manager")
    logger.info("%s", "=" * 60)

    # Listar empresas disponibles
    logger.info("Available companies:")
    companies = company_manager.get_available_companies()
    for company in companies:
        logger.info(
            "  %s: %s - %s",
            company.get("id"),
            company.get("codigo"),
            company.get("nombre"),
        )
        logger.debug("     Motor BD: %s", company.get("motor_bd"))
        if company.get("bd_mariadb"):
            logger.debug("     MariaDB: %s", company.get("bd_mariadb"))
        if company.get("bd_postgresql"):
            logger.debug("     PostgreSQL: %s", company.get("bd_postgresql"))

    if companies:
        # Seleccionar primera empresa como ejemplo
        first_company = companies[0]
        logger.info("\nSelecting company: %s", first_company.get("codigo"))

        # Validar configuración
        validation = company_manager.validate_company_database(first_company["id"])
        if validation["valid"]:
            logger.info("Configuration valid")

            # Seleccionar empresa
            success = company_manager.select_company(first_company["id"])
            if success:
                logger.info("Company selected successfully")

                # Mostrar contexto actual
                context = get_current_company_context()
                logger.info("Current context: %s", context.get("company_name"))
                logger.debug("   Base de datos: %s", context.get("database_name"))
        else:
            logger.warning("Invalid DB configuration: %s", validation.get("message"))

    logger.info("\nNote: To integrate with Qt:")
    logger.info("   1. Importar company_manager en tu módulo Qt")
    logger.info("   2. Usar setup_company_selection_combo() para configurar QComboBox")
    logger.info("   3. Conectar señal currentIndexChanged a on_company_selected()")
    logger.info("   4. Usar get_current_company_context() para mostrar info en UI")
