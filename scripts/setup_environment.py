#!/usr/bin/env python3
"""
Script de configuración de variables de entorno para diferentes entornos
Genera archivos .env para desarrollo, testing y producción
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

# Directorio raíz del proyecto
ROOT_DIR = Path(__file__).parent

# Archivo de configuración base
CONFIG_FILE = ROOT_DIR / "core" / "config.json"

def load_base_config() -> Dict[str, Any]:
    """Carga la configuración base desde config.json."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {CONFIG_FILE}")

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_env_file(env_name: str, config: Dict[str, Any]) -> str:
    """
    Genera el contenido de un archivo .env para un entorno específico.
    """
    lines = [
        f"# Creative ERP - Variables de entorno para {env_name.upper()}",
        f"# Generado automáticamente - NO EDITAR MANUALMENTE",
        f"",
        f"# Entorno actual",
        f"ENVIRONMENT={env_name}",
        f"",
        f"# Base de datos principal (Creative ERP Main)",
        f"MAIN_DB_HOST={config['databases']['main']['host']}",
        f"MAIN_DB_PORT={config['databases']['main']['port']}",
        f"MAIN_DB_NAME={config['databases']['main']['database']}",
        f"MAIN_DB_USER={config['databases']['main']['username']}",
        f"MAIN_DB_PASSWORD={config['databases']['main']['password']}",
        f"",
        f"# Base de datos ArtStudio3D",
        f"ARTSTUDIO_DB_HOST={config['databases']['artstudio3d']['host']}",
        f"ARTSTUDIO_DB_PORT={config['databases']['artstudio3d']['port']}",
        f"ARTSTUDIO_DB_NAME={config['databases']['artstudio3d']['database']}",
        f"ARTSTUDIO_DB_USER={config['databases']['artstudio3d']['username']}",
        f"ARTSTUDIO_DB_PASSWORD={config['databases']['artstudio3d']['password']}",
        f"",
        f"# Configuración de logging",
        f"LOG_LEVEL={config['logging']['level']}",
        f"LOG_FILE={config['logging']['file']}",
        f"",
        f"# Configuración de UI",
        f"UI_THEME={config['ui']['theme']}",
        f"UI_LANGUAGE={config['ui']['language']}",
        f"",
        f"# Configuración de seguridad",
        f"SECRET_KEY={config['security']['secret_key']}",
        f"SESSION_TIMEOUT={config['security']['session_timeout']}",
        f"",
        f"# Configuración de backups",
        f"BACKUP_ENABLED={config['backup']['enabled']}",
        f"BACKUP_PATH={config['backup']['path']}",
        f"BACKUP_RETENTION_DAYS={config['backup']['retention_days']}",
        f"",
        f"# Configuración de email (para notificaciones)",
        f"SMTP_SERVER={config['email']['smtp_server']}",
        f"SMTP_PORT={config['email']['smtp_port']}",
        f"SMTP_USER={config['email']['smtp_user']}",
        f"SMTP_PASSWORD={config['email']['smtp_password']}",
        f"EMAIL_FROM={config['email']['from_address']}",
        f"",
        f"# Configuración específica por entorno",
    ]

    # Configuración específica del entorno
    if env_name == "development":
        lines.extend([
            f"DEBUG=True",
            f"SQLALCHEMY_ECHO=True",
            f"TESTING=False",
            f"ALLOWED_HOSTS=localhost,127.0.0.1",
        ])
    elif env_name == "testing":
        lines.extend([
            f"DEBUG=False",
            f"SQLALCHEMY_ECHO=False",
            f"TESTING=True",
            f"ALLOWED_HOSTS=localhost,127.0.0.1,test.example.com",
        ])
    elif env_name == "production":
        lines.extend([
            f"DEBUG=False",
            f"SQLALCHEMY_ECHO=False",
            f"TESTING=False",
            f"ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com",
        ])

    lines.append(f"")
    return "\n".join(lines)

def create_env_files():
    """Crea archivos .env para todos los entornos."""
    try:
        # Cargar configuración base
        base_config = load_base_config()

        # Entornos a generar
        environments = ["development", "testing", "production"]

        print("🎨 Creative ERP - Generador de Variables de Entorno")
        print("=" * 60)

        for env in environments:
            if env in base_config['environments']:
                env_config = base_config['environments'][env]

                # Generar contenido del archivo .env
                env_content = generate_env_file(env, env_config)

                # Nombre del archivo
                env_file = ROOT_DIR / f".env.{env}"

                # Escribir archivo
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(env_content)

                print(f"✅ Archivo .env.{env} generado exitosamente")
                print(f"   Ubicación: {env_file}")
            else:
                print(f"⚠️  Configuración para entorno '{env}' no encontrada")

        print(f"\n📝 Instrucciones:")
        print(f"   1. Revisar y ajustar los valores en los archivos .env.* según su entorno")
        print(f"   2. Copiar el archivo apropiado a .env (ej: cp .env.development .env)")
        print(f"   3. Para producción, usar .env.production como base")
        print(f"   4. NUNCA subir archivos .env al control de versiones")

    except Exception as e:
        print(f"❌ Error generando archivos de entorno: {e}")
        return False

    return True

def validate_env_files():
    """Valida que los archivos .env generados sean correctos."""
    print("\n🔍 Validando archivos .env generados...")

    environments = ["development", "testing", "production"]
    required_vars = [
        "ENVIRONMENT", "MAIN_DB_HOST", "MAIN_DB_NAME", "ARTSTUDIO_DB_HOST",
        "LOG_LEVEL", "UI_THEME", "SECRET_KEY", "DEBUG"
    ]

    all_valid = True

    for env in environments:
        env_file = ROOT_DIR / f".env.{env}"

        if not env_file.exists():
            print(f"❌ Archivo .env.{env} no encontrado")
            all_valid = False
            continue

        try:
            # Leer archivo
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verificar variables requeridas
            missing_vars = []
            for var in required_vars:
                if f"{var}=" not in content:
                    missing_vars.append(var)

            if missing_vars:
                print(f"❌ .env.{env} - Variables faltantes: {', '.join(missing_vars)}")
                all_valid = False
            else:
                print(f"✅ .env.{env} - Validación exitosa")

        except Exception as e:
            print(f"❌ Error validando .env.{env}: {e}")
            all_valid = False

    return all_valid

def create_env_example():
    """Crea un archivo .env.example con valores de ejemplo."""
    example_content = """# Creative ERP - Archivo de ejemplo de variables de entorno
# Copiar este archivo a .env y ajustar los valores según el entorno

# Entorno actual (development, testing, production)
ENVIRONMENT=development

# Base de datos principal (Creative ERP Main)
MAIN_DB_HOST=localhost
MAIN_DB_PORT=3306
MAIN_DB_NAME=creative_erp_main
MAIN_DB_USER=erp_user
MAIN_DB_PASSWORD=your_password_here

# Base de datos ArtStudio3D
ARTSTUDIO_DB_HOST=localhost
ARTSTUDIO_DB_PORT=3306
ARTSTUDIO_DB_NAME=artstudio3d
ARTSTUDIO_DB_USER=erp_user
ARTSTUDIO_DB_PASSWORD=your_password_here

# Configuración de logging
LOG_LEVEL=INFO
LOG_FILE=logs/creative_erp.log

# Configuración de UI
UI_THEME=default
UI_LANGUAGE=es

# Configuración de seguridad
SECRET_KEY=your_secret_key_here_generate_random_string
SESSION_TIMEOUT=3600

# Configuración de backups
BACKUP_ENABLED=true
BACKUP_PATH=backups/
BACKUP_RETENTION_DAYS=30

# Configuración de email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=noreply@creativeerp.com

# Configuración específica por entorno
DEBUG=True
SQLALCHEMY_ECHO=True
TESTING=False
ALLOWED_HOSTS=localhost,127.0.0.1
"""

    example_file = ROOT_DIR / ".env.example"
    with open(example_file, 'w', encoding='utf-8') as f:
        f.write(example_content)

    print(f"✅ Archivo .env.example creado: {example_file}")

def main():
    """Función principal."""
    print("🎨 Creative ERP - Configuración de Variables de Entorno")
    print("=" * 60)

    # Crear archivos .env
    if create_env_files():
        # Validar archivos
        if validate_env_files():
            print("\n✅ Todos los archivos .env generados y validados correctamente")
        else:
            print("\n❌ Algunos archivos .env tienen problemas de validación")
    else:
        print("\n❌ Error generando archivos .env")
        return

    # Crear archivo de ejemplo
    create_env_example()

    print(f"\n📋 Resumen:")
    print(f"   - Archivos .env.* generados para development, testing, production")
    print(f"   - Archivo .env.example creado como referencia")
    print(f"   - Para usar: copiar el archivo apropiado a .env")
    print(f"   - Ejemplo: cp .env.development .env")

if __name__ == "__main__":
    main()