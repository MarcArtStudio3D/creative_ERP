#!/usr/bin/env python3
"""
Módulo de integración con Qt para gestión de empresas y bases de datos
Ejemplo de cómo integrar la selección de empresa con el cambio automático de base de datos
"""

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
            from core.db import set_database_for_company, get_company_database_info

            # Configurar la base de datos para la empresa
            set_database_for_company(company_id)

            # Obtener información de la empresa
            self.company_info = get_company_database_info(company_id)
            self.current_company_id = company_id

            print(f"Company {company_id} selected: {self.company_info['company_name']}")
            print(f"   DB engine: {self.company_info['motor_base_datos']}")
            print(f"   Database: {self.company_info['database_name']}")

            return True

        except Exception as e:
            print(f"❌ Error seleccionando empresa {company_id}: {e}")
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
        """
        try:
            from core.db import set_current_database, get_current_database, get_session
            from core.models import Empresa

            # Guardar base de datos actual
            original_db = get_current_database()

            # Cambiar a base de datos principal
            set_current_database('main')

            try:
                session = get_session()
                empresas = session.query(Empresa).filter(Empresa.activa == 1).all()

                companies = []
                for empresa in empresas:
                    companies.append({
                        'id': empresa.id,
                        'codigo': empresa.codigo_empresa,
                        'nombre': empresa.nombre_fiscal,
                        'motor_bd': empresa.motor_base_datos,
                        'bd_mariadb': empresa.nombre_base_datos_maria_db,
                        'bd_postgresql': empresa.nombre_base_datos_postgresql
                    })

                return companies

            finally:
                # Restaurar base de datos original
                set_current_database(original_db)
                session.close()

        except Exception as e:
            print(f"ERROR getting companies: {e}")
            return []

    def validate_company_database(self, company_id: int) -> dict:
        """
        Valida que la configuración de base de datos de una empresa sea correcta.
        Retorna un diccionario con el estado de validación.
        """
        try:
            from core.db import get_company_database_info

            info = get_company_database_info(company_id)

            # Intentar conectar a la base de datos
            from sqlalchemy import create_engine, text

            engine = create_engine(info['database_url'])
            with engine.connect() as conn:
                # Probar una consulta simple
                result = conn.execute(text("SELECT 1"))
                result.fetchone()

            engine.dispose()

            return {
                'valid': True,
                'message': 'Conexión exitosa',
                'company_info': info
            }

        except Exception as e:
            return {
                'valid': False,
                'message': f'Error de conexión: {str(e)}',
                'company_info': None
            }

    def update_company_database_config(self, company_id: int, config: dict) -> bool:
        """
        Actualiza la configuración de base de datos de una empresa.
        config debe contener: motor_base_datos, nombre_base_datos_maria_db/postgresql, etc.
        """
        try:
            from core.db import set_current_database, get_current_database, get_session
            from core.models import Empresa

            # Guardar base de datos actual
            original_db = get_current_database()

            # Cambiar a base de datos principal
            set_current_database('main')

            try:
                session = get_session()
                empresa = session.query(Empresa).filter_by(id=company_id).first()

                if not empresa:
                    raise ValueError(f"Empresa con ID {company_id} no encontrada")

                # Actualizar configuración
                for key, value in config.items():
                    if hasattr(empresa, key):
                        setattr(empresa, key, value)

                session.commit()

                print(f"Database configuration updated for company {company_id}")
                return True

            finally:
                set_current_database(original_db)
                session.close()

        except Exception as e:
            print(f"ERROR updating configuration: {e}")
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
            combo_box.addItem(display_text, company['id'])

        print(f"Company combo configured with {len(companies)} companies")

    except Exception as e:
        print(f"ERROR configuring company combo: {e}")


def on_company_selected(company_id: int) -> bool:
    """
    Función que se ejecuta cuando se selecciona una empresa en la UI.
    Retorna True si la selección fue exitosa.
    """
    if not company_id:
        print("No company selected")
        return False

    # Validar configuración antes de seleccionar
    validation = company_manager.validate_company_database(company_id)
    if not validation['valid']:
        print(f"Invalid DB configuration: {validation['message']}")
        return False

    # Seleccionar empresa
    success = company_manager.select_company(company_id)
    if success:
        # Aquí se podría emitir una señal Qt para actualizar la UI
        print("Company selected successfully - DB configured")
        return True
    else:
        print("ERROR selecting company")
        return False


def get_current_company_context() -> dict:
    """
    Obtiene el contexto de la empresa actual para usar en la aplicación.
    Útil para mostrar información en la UI.
    """
    company_info = company_manager.get_current_company()
    if not company_info:
        return {
            'has_company': False,
            'company_name': 'Ninguna empresa seleccionada',
            'database_info': None
        }

    return {
        'has_company': True,
        'company_id': company_info['company_id'],
        'company_name': company_info['company_name'],
        'motor_bd': company_info['motor_base_datos'],
        'database_name': company_info['database_name'],
        'database_info': company_info
    }


if __name__ == "__main__":
    # Ejemplo de uso del gestor de empresas
    print("Creative ERP - Company and Database Manager")
    print("=" * 60)

    # Listar empresas disponibles
    print("Available companies:")
    companies = company_manager.get_available_companies()
    for company in companies:
        print(f"  {company['id']}: {company['codigo']} - {company['nombre']}")
        print(f"     Motor BD: {company['motor_bd']}")
        if company['bd_mariadb']:
            print(f"     MariaDB: {company['bd_mariadb']}")
        if company['bd_postgresql']:
            print(f"     PostgreSQL: {company['bd_postgresql']}")

    if companies:
        # Seleccionar primera empresa como ejemplo
        first_company = companies[0]
        print(f"\nSelecting company: {first_company['codigo']}")

        # Validar configuración
        validation = company_manager.validate_company_database(first_company['id'])
        if validation['valid']:
            print("Configuration valid")

            # Seleccionar empresa
            success = company_manager.select_company(first_company['id'])
            if success:
                print("Company selected successfully")

                # Mostrar contexto actual
                context = get_current_company_context()
                print(f"Current context: {context['company_name']}")
                print(f"   Base de datos: {context['database_name']}")
        else:
            print(f"Invalid DB configuration: {validation['message']}")

    print("\nNote: To integrate with Qt:")
    print("   1. Importar company_manager en tu módulo Qt")
    print("   2. Usar setup_company_selection_combo() para configurar QComboBox")
    print("   3. Conectar señal currentIndexChanged a on_company_selected()")
    print("   4. Usar get_current_company_context() para mostrar info en UI")