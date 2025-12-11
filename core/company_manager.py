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
            # Usar MultiDBManager (nuevo sistema sin ORM)
            from core.db_manager import get_db_manager

            db_manager = get_db_manager()

            # Obtener info de la empresa desde BD principal
            empresa_info = db_manager.fetch_one(
                "SELECT * FROM empresas WHERE id = %s",
                (company_id,),
                use_main=True
            )

            if not empresa_info:
                logging.getLogger(__name__).error(
                    "Empresa %s no encontrada en la BD principal", company_id
                )
                return False

            # Determinar configuración de BD según el motor
            motor = empresa_info.get('motor_base_datos', 'mariadb')

            if motor.lower() == 'mariadb' or motor.lower() == 'mysql':
                db_config = {
                    'type': 'mariadb',
                    'host': empresa_info.get('host_mariadb', 'localhost'),
                    'port': empresa_info.get('puerto_mariadb', 3306),
                    'user': empresa_info.get('usuario_mariadb', 'admin'),
                    'password': empresa_info.get('password_mariadb', 'admin123'),
                    'database': empresa_info.get('nombre_base_datos_maria_db')
                }
            elif motor.lower() == 'sqlite':
                db_config = {
                    'type': 'sqlite',
                    'path': empresa_info.get('ruta_base_datos_sqlite')
                }
            else:
                logging.getLogger(__name__).error(
                    "Motor de BD no soportado: %s", motor
                )
                return False

            # Registrar empresa en MultiDBManager si no está registrada
            try:
                db_manager.register_empresa(company_id, db_config)
            except Exception as e:
                # Ya puede estar registrada, solo loguear
                logging.getLogger(__name__).debug(
                    "Empresa %s ya registrada o error registrando: %s", company_id, e
                )

            # Cambiar a la empresa activa
            db_manager.switch_empresa(company_id)

            # Guardar info de la empresa
            self.company_info = {
                'company_id': company_id,
                'company_name': empresa_info.get('nombre_fiscal'),
                'motor_base_datos': motor,
                'database_name': db_config.get('database') or db_config.get('path')
            }
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
        Migrado a MultiDBManager (sin ORM).
        """
        try:
            from core.db_manager import get_db_manager

            db_manager = get_db_manager()

            # Query directa a BD principal
            sql = """
                SELECT id, codigo_empresa, nombre_fiscal, motor_base_datos,
                       nombre_base_datos_maria_db, nombre_base_datos_postgresql,
                       ruta_base_datos_sqlite
                FROM empresas
                WHERE activa = 1
                ORDER BY nombre_fiscal
            """

            empresas = db_manager.fetch_all(sql, use_main=True)

            companies = []
            for empresa in empresas:
                companies.append({
                    "id": empresa['id'],
                    "codigo": empresa['codigo_empresa'],
                    "nombre": empresa['nombre_fiscal'],
                    "motor_bd": empresa['motor_base_datos'],
                    "bd_mariadb": empresa['nombre_base_datos_maria_db'],
                    "bd_postgresql": empresa['nombre_base_datos_postgresql'],
                })

            return companies

        except Exception:
            logging.getLogger(__name__).exception("ERROR getting companies")
            return []



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

    # Seleccionar empresa directamente (MultiDBManager valida internamente)
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

        # Seleccionar empresa directamente
        success = company_manager.select_company(first_company["id"])
        if success:
            logger.info("Company selected successfully")

            # Mostrar contexto actual
            context = get_current_company_context()
            logger.info("Current context: %s", context.get("company_name"))
            logger.debug("   Base de datos: %s", context.get("database_name"))
        else:
            logger.warning("Failed to select company")

    logger.info("\nNote: To integrate with Qt:")
    logger.info("   1. Importar company_manager en tu módulo Qt")
    logger.info("   2. Usar setup_company_selection_combo() para configurar QComboBox")
    logger.info("   3. Conectar señal currentIndexChanged a on_company_selected()")
    logger.info("   4. Usar get_current_company_context() para mostrar info en UI")
