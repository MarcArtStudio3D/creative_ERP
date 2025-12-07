"""
Script de diagnóstico para MariaDB (modo JSON).

Comportamiento:
- Lee credenciales desde variables de entorno (MARIADB_HOST, MARIADB_PORT, MARIADB_USER,
  MARIADB_PASSWORD, MARIADB_DB). Si no están definidas usa valores por defecto de desarrollo.
- Ejecuta 4 comprobaciones: conexión directa (pymysql), listar bases, conexión SQLAlchemy, y
  comprobación de modelos (metadata).
- Escribe un JSON resumen en stdout y en logs/test_mariadb_result.json.
"""

import sys
from pathlib import Path
import os
import json
import logging

# Root del proyecto
project_root = Path(__file__).resolve().parents[2]
log_dir = project_root / 'logs'
os.makedirs(log_dir, exist_ok=True)
result_path = log_dir / 'test_mariadb_result.json'
log_file = log_dir / 'test_mariadb_run.log'

# Logging básico (fichero + consola)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Añadir la raíz del proyecto al sys.path
sys.path.insert(0, str(project_root))

import pymysql
from sqlalchemy import text, inspect
from core.db import get_engine_from_url

# Obtener credenciales desde variables de entorno con defaults de desarrollo
HOST = os.getenv('MARIADB_HOST', '127.0.0.1')
PORT = int(os.getenv('MARIADB_PORT', '3306'))
USER = os.getenv('MARIADB_USER', 'root')
PASSWORD = os.getenv('MARIADB_PASSWORD', '1234')
DB = os.getenv('MARIADB_DB', 'creative_erp')
MARIADB_URL = os.getenv('MARIADB_URL', f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

def run_checks():
    result = {
        'ok': True,
        'host': HOST,
        'port': PORT,
        'user': USER,
        'database': DB,
        'checks': {
            'pymysql_connect': None,
            'list_databases': None,
            'sqlalchemy_connect': None,
            'models_metadata': None
        }
    }

    # 1) pymysql connect
    try:
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB, connect_timeout=5)
        cur = conn.cursor()
        cur.execute('SELECT VERSION()')
        version = cur.fetchone()
        cur.execute('SELECT DATABASE()')
        current_db = cur.fetchone()
        cur.execute('SHOW TABLES')
        tables = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()

        result['checks']['pymysql_connect'] = {
            'ok': True,
            'version': version[0] if version else None,
            'current_db': current_db[0] if current_db else None,
            'tables_count': len(tables),
            'tables': tables[:50]
        }
    except Exception as e:
        logging.exception('Error connecting with pymysql')
        result['ok'] = False
        result['checks']['pymysql_connect'] = {'ok': False, 'error': str(e)}

    # 2) list databases
    try:
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, connect_timeout=5)
        cur = conn.cursor()
        cur.execute('SHOW DATABASES')
        dbs = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()
        result['checks']['list_databases'] = {'ok': True, 'databases': dbs}
    except Exception as e:
        logging.exception('Error listing databases')
        result['ok'] = False
        result['checks']['list_databases'] = {'ok': False, 'error': str(e)}

    # 3) SQLAlchemy connection + inspector
    try:
        engine = get_engine_from_url(MARIADB_URL)
        with engine.connect() as conn:
            res = conn.execute(text('SELECT DATABASE()'))
            db_name = res.fetchone()[0]
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        result['checks']['sqlalchemy_connect'] = {'ok': True, 'database': db_name, 'tables': tables[:200], 'tables_count': len(tables)}
    except Exception as e:
        logging.exception('Error connecting with SQLAlchemy')
        result['ok'] = False
        result['checks']['sqlalchemy_connect'] = {'ok': False, 'error': str(e)}

    # 4) Models metadata
    try:
        # Usar SQLModel.metadata (no hay 'Base' en core.models con SQLModel)
        from sqlmodel import SQLModel
        # Importar módulos que definen modelos para asegurarnos de que metadata se registre
        import core.models as core_models
        import modules.clientes.models as clientes_models
        import modules.tipo_cliente.models as tipo_cliente_models
        tables = list(SQLModel.metadata.tables.keys())
        result['checks']['models_metadata'] = {'ok': True, 'defined_tables': tables}
    except Exception as e:
        logging.exception('Error loading models metadata')
        result['ok'] = False
        result['checks']['models_metadata'] = {'ok': False, 'error': str(e)}

    return result

def main():
    out = run_checks()
    # Escribir JSON en fichero de resultado
    try:
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
    except Exception:
        logging.exception('Error escribiendo resultado JSON')

    # Imprimir JSON en stdout para pipelines
    print(json.dumps(out, indent=2, ensure_ascii=False))

    # Exit code non-zero si fallo
    if not out.get('ok', False):
        sys.exit(2)

if __name__ == '__main__':
    main()
