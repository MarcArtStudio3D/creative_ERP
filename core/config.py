#!/usr/bin/env python3
"""
Sistema de configuración de entornos para Creative ERP
Gestiona diferentes configuraciones para desarrollo, testing y producción
"""

import os
from pathlib import Path
from typing import Dict, Any
import json

class EnvironmentConfig:
    """Gestor de configuración de entornos."""

    def __init__(self):
        self.current_env = os.environ.get('CREATIVE_ERP_ENV', 'development')
        self.config_dir = Path(__file__).parent / 'config'
        self.config_dir.mkdir(exist_ok=True)

        # Configuraciones por defecto para cada entorno
        self.default_configs = {
            'development': {
                'database': {
                    'main': {
                        'driver': 'mysql+pymysql',
                        'host': '127.0.0.1',
                        'port': 3306,
                        'database': 'creative_erp_main',
                        'username': 'admin',
                        'password': 'admin123'
                    },
                    'artstudio3d': {
                        'driver': 'mysql+pymysql',
                        'host': '127.0.0.1',
                        'port': 3306,
                        'database': 'artstudio3d',
                        'username': 'admin',
                        'password': 'admin123'
                    }
                },
                'logging': {
                    'level': 'DEBUG',
                    'file': 'logs/creative_erp_dev.log'
                },
                'ui': {
                    'theme': 'default',
                    'language': 'es'
                }
            },
            'testing': {
                'database': {
                    'main': {
                        'driver': 'mysql+pymysql',
                        'host': '127.0.0.1',
                        'port': 3306,
                        'database': 'creative_erp_test',
                        'username': 'admin',
                        'password': 'admin123'
                    },
                    'artstudio3d': {
                        'driver': 'mysql+pymysql',
                        'host': '127.0.0.1',
                        'port': 3306,
                        'database': 'artstudio3d_test',
                        'username': 'admin',
                        'password': 'admin123'
                    }
                },
                'logging': {
                    'level': 'INFO',
                    'file': 'logs/creative_erp_test.log'
                },
                'ui': {
                    'theme': 'default',
                    'language': 'es'
                }
            },
            'production': {
                'database': {
                    'main': {
                        'driver': 'mysql+pymysql',
                        'host': os.environ.get('DB_HOST', 'localhost'),
                        'port': int(os.environ.get('DB_PORT', 3306)),
                        'database': os.environ.get('DB_NAME_MAIN', 'creative_erp_prod'),
                        'username': os.environ.get('DB_USER', 'creative_erp'),
                        'password': os.environ.get('DB_PASSWORD', '')
                    },
                    'artstudio3d': {
                        'driver': 'mysql+pymysql',
                        'host': os.environ.get('DB_HOST', 'localhost'),
                        'port': int(os.environ.get('DB_PORT', 3306)),
                        'database': os.environ.get('DB_NAME_ARTSTUDIO3D', 'artstudio3d_prod'),
                        'username': os.environ.get('DB_USER', 'creative_erp'),
                        'password': os.environ.get('DB_PASSWORD', '')
                    }
                },
                'logging': {
                    'level': 'WARNING',
                    'file': '/var/log/creative_erp/creative_erp.log'
                },
                'ui': {
                    'theme': 'professional',
                    'language': 'es'
                }
            }
        }

        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración para el entorno actual."""
        # Cargar configuración por defecto
        config = self.default_configs.get(self.current_env, self.default_configs['development']).copy()

        # Cargar configuración personalizada si existe
        config_file = self.config_dir / f'{self.current_env}.json'
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    custom_config = json.load(f)
                    self._merge_config(config, custom_config)
            except Exception as e:
                print(f"⚠️  Error cargando configuración personalizada: {e}")

        # Sobrescribir con variables de entorno
        self._override_with_env_vars(config)

        return config

    def _merge_config(self, base_config: Dict[str, Any], custom_config: Dict[str, Any]):
        """Fusiona configuración personalizada con la base."""
        for key, value in custom_config.items():
            if isinstance(value, dict) and key in base_config and isinstance(base_config[key], dict):
                self._merge_config(base_config[key], value)
            else:
                base_config[key] = value

    def _override_with_env_vars(self, config: Dict[str, Any]):
        """Sobrescribe configuración con variables de entorno."""
        # Database overrides
        if 'DB_HOST' in os.environ:
            for db_config in config['database'].values():
                if isinstance(db_config, dict):
                    db_config['host'] = os.environ['DB_HOST']

        if 'DB_PORT' in os.environ:
            for db_config in config['database'].values():
                if isinstance(db_config, dict):
                    db_config['port'] = int(os.environ['DB_PORT'])

        if 'DB_USER' in os.environ:
            for db_config in config['database'].values():
                if isinstance(db_config, dict):
                    db_config['username'] = os.environ['DB_USER']

        if 'DB_PASSWORD' in os.environ:
            for db_config in config['database'].values():
                if isinstance(db_config, dict):
                    db_config['password'] = os.environ['DB_PASSWORD']

    def get_database_url(self, db_name: str) -> str:
        """Obtiene la URL de conexión para una base de datos específica."""
        if db_name not in self.config['database']:
            raise ValueError(f"Base de datos '{db_name}' no configurada para entorno '{self.current_env}'")

        db_config = self.config['database'][db_name]
        return (f"{db_config['driver']}://{db_config['username']}:{db_config['password']}@"
                f"{db_config['host']}:{db_config['port']}/{db_config['database']}")

    def get(self, key: str, default=None):
        """Obtiene un valor de configuración usando notación de puntos."""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set_custom_config(self, key: str, value: Any):
        """Establece una configuración personalizada para el entorno actual."""
        config_file = self.config_dir / f'{self.current_env}.json'
        custom_config = {}

        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    custom_config = json.load(f)
            except:
                pass

        # Establecer valor usando notación de puntos
        keys = key.split('.')
        current = custom_config

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value

        # Guardar configuración
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(custom_config, f, indent=2, ensure_ascii=False)

        # Recargar configuración
        self.config = self._load_config()

    def get_current_env(self) -> str:
        """Obtiene el entorno actual."""
        return self.current_env

    def list_available_envs(self) -> list:
        """Lista los entornos disponibles."""
        return list(self.default_configs.keys())

    def create_env_file(self, env_name: str):
        """Crea un archivo de ejemplo para un entorno."""
        if env_name not in self.default_configs:
            raise ValueError(f"Entorno '{env_name}' no válido")

        config_file = self.config_dir / f'{env_name}.json'
        if not config_file.exists():
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)
            print(f"✅ Archivo de configuración creado: {config_file}")

# Instancia global de configuración
config = EnvironmentConfig()

def get_database_url_for_company(company_id: int) -> str:
    """
    Obtiene la URL de base de datos para una empresa específica.
    Busca la configuración en la tabla empresas.
    """
    from core.db import set_current_database, get_session
    from core.models import Empresa

    # Cambiar a base de datos principal para consultar empresas
    original_db = None
    try:
        from core.db import get_current_database
        original_db = get_current_database()
    except:
        pass

    set_current_database('main')

    try:
        session = get_session()
        empresa = session.query(Empresa).filter_by(id=company_id).first()

        if not empresa:
            raise ValueError(f"Empresa con ID {company_id} no encontrada")

        # Normalizar motor
        motor = empresa.motor_base_datos.strip().lower() if empresa.motor_base_datos else 'mariadb'

        # Determinar qué base de datos usar según el motor configurado
        if motor == 'postgresql':
            if not empresa.nombre_base_datos_postgresql:
                raise ValueError(f"Empresa {company_id} no tiene configurada base de datos PostgreSQL")

            # Construir URL para PostgreSQL
            url = (f"postgresql://{empresa.usuario_postgresql}:{empresa.password_postgresql}@"
                   f"{empresa.host_postgresql}:{empresa.puerto_postgresql}/"
                   f"{empresa.nombre_base_datos_postgresql}")

        elif motor in ['mariadb', 'mysql']:
            if not empresa.nombre_base_datos_maria_db:
                raise ValueError(f"Empresa {company_id} no tiene configurada base de datos MariaDB")

            # Construir URL para MariaDB/MySQL
            url = (f"mysql+pymysql://{empresa.usuario_mariadb}:{empresa.password_mariadb}@"
                   f"{empresa.host_mariadb}:{empresa.puerto_mariadb}/"
                   f"{empresa.nombre_base_datos_maria_db}")

        elif motor == 'sqlite':
            # Usar ruta configurada o por defecto
            ruta = getattr(empresa, 'ruta_base_datos_sqlite', None)
            if not ruta:
                # Fallback a convención por defecto
                ruta = f"datos/company_{company_id}.sqlite"
            
            # Asegurar ruta absoluta si es necesario o relativa al proyecto
            import os
            if not os.path.isabs(ruta):
                # Asumir relativa a la raíz del proyecto
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ruta = os.path.join(base_dir, ruta)
                
            url = f"sqlite:///{ruta}"

        else:
            raise ValueError(f"Motor de base de datos '{empresa.motor_base_datos}' no soportado")

        return url

    finally:
        # Restaurar base de datos original
        if original_db:
            set_current_database(original_db)
        session.close()

def set_database_for_company(company_id: int):
    """
    Configura la base de datos actual según la empresa seleccionada.
    Esta función actualiza el sistema de base de datos para usar la BD de la empresa.
    """
    from core.db import DATABASE_CONFIGS

    url = get_database_url_for_company(company_id)

    # Agregar dinámicamente la configuración de la empresa
    DATABASE_CONFIGS[f'company_{company_id}'] = url

    # Cambiar a la base de datos de la empresa
    from core.db import set_current_database
    set_current_database(f'company_{company_id}')

    # Asegurar que las tablas existan en la base de datos de la empresa
    from core.db import init_db
    init_db()

    print(f"Database switched for company {company_id}: {url}")

if __name__ == "__main__":
    # Ejemplo de uso
    print(f"Entorno actual: {config.get_current_env()}")
    print(f"URL BD main: {config.get_database_url('main')}")
    print(f"URL BD artstudio3d: {config.get_database_url('artstudio3d')}")

    # Listar entornos disponibles
    print(f"Entornos disponibles: {config.list_available_envs()}")

    # Crear archivo de configuración para desarrollo si no existe
    config.create_env_file('development')