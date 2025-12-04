# -----------------------------
# core/db.py
# -----------------------------
"""Gestión de base de datos con SQLAlchemy."""

from sqlalchemy import create_engine
import logging
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from core.models import Base
import os
from sqlalchemy import inspect, text
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Date, Float, Text

# Importar configuración de entornos
from .config import config as env_config

# Configuraciones de base de datos disponibles
DATABASE_CONFIGS = {
    'main': env_config.get_database_url('main'),
    'artstudio3d': env_config.get_database_url('artstudio3d'),
    'current': env_config.get_database_url('main')  # Para compatibilidad
}

# Base de datos por defecto
DEFAULT_DB = os.environ.get('CREATIVE_ERP_DEFAULT_DB', 'main')

# Motor de base de datos actual
_current_db = DEFAULT_DB
_current_engine = None
_current_session = None

def get_database_url(db_name='main'):
    """Obtiene la URL de conexión para una base de datos específica."""
    return DATABASE_CONFIGS.get(db_name, DATABASE_CONFIGS['main'])

def set_current_database(db_name):
    """Cambia la base de datos actual."""
    global _current_db, _current_engine, _current_session

    if db_name not in DATABASE_CONFIGS:
        raise ValueError(f"Base de datos '{db_name}' no configurada. Opciones disponibles: {list(DATABASE_CONFIGS.keys())}")

    _current_db = db_name
    db_url = get_database_url(db_name)

    # Crear nuevo motor
    _current_engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False} if 'sqlite' in db_url else {}
    )

    # Crear nueva sesión
    _current_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=_current_engine)
    )

    logger = logging.getLogger(__name__)
    logger.debug("Database switched to: %s (%s)", _current_db, db_url)

def get_current_database():
    """Obtiene el nombre de la base de datos actual."""
    return _current_db

def get_engine():
    """Obtiene el motor de base de datos actual."""
    global _current_engine
    if _current_engine is None:
        set_current_database(_current_db)
    return _current_engine

def get_session():
    """Obtiene una sesión de base de datos para la base de datos actual."""
    global _current_session
    if _current_session is None:
        set_current_database(_current_db)
    return _current_session()

# Inicializar con la base de datos por defecto
set_current_database(DEFAULT_DB)

# Alias para compatibilidad hacia atrás
DB_PATH = get_database_url(DEFAULT_DB)
engine = get_engine()
SessionLocal = _current_session


def get_session():
    """Obtiene una sesión de base de datos para la base de datos actual."""
    global _current_session
    if _current_session is None:
        set_current_database(_current_db)
    return _current_session()


def _is_company_database_pointing_to_artstudio3d() -> bool:
    """
    Verifica si la base de datos actual es de una empresa que apunta a artstudio3d.
    """
    current_db = get_current_database()

    # Verificar si es una base de datos de empresa (formato: company_X)
    if not current_db.startswith('company_'):
        return False

    try:
        # Extraer el ID de la empresa
        company_id = int(current_db.split('_')[1])

        # Verificar la configuración de la empresa
        from .config import get_database_url_for_company
        url = get_database_url_for_company(company_id)

        # Verificar si la URL contiene 'artstudio3d'
        return 'artstudio3d' in url

    except (ValueError, IndexError):
        return False


def init_db(db_name=None, initiator: str | None = None):
    """Crea todas las tablas específicas de módulos en la base de datos especificada.

    Argumentos:
    - db_name: si se proporciona, usa esa BD; por defecto usa la BD actual.
    - initiator: (opcional) nombre/identificador de usuario que solicitó la operación
      (este valor se registra en logs para auditoría).
    """
    # Setup logger for init_db actions
    logger = logging.getLogger('core.db.init')
    if not logger.handlers:
        # Ensure logs dir exists
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        try:
            os.makedirs(logs_dir, exist_ok=True)
            fh = logging.FileHandler(os.path.join(logs_dir, 'init_db.log'))
            fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(fmt)
            logger.addHandler(fh)
            logger.setLevel(logging.INFO)
        except Exception:
            # fallback to default logger configuration
            logging.basicConfig()

    if db_name:
        original_db = get_current_database()
        set_current_database(db_name)
        current_engine = get_engine()
    else:
        current_engine = get_engine()

    # Crear tablas según la base de datos actual
    logger.info(f"init_db requested for database: {get_current_database()} by {initiator}")
    if get_current_database() == 'main':
        # Base de datos principal: tablas globales
        from . import models as core_models
        try:
            core_models.Base.metadata.create_all(bind=current_engine)
            logger.info("Global tables created in the main database")
        except Exception as e:
            logger.exception(f"ERROR creating global tables: {e}")
            raise

    elif get_current_database() == 'artstudio3d' or _is_company_database_pointing_to_artstudio3d():
        # Base de datos ArtStudio3D o base de datos de empresa que apunta a ArtStudio3D: tablas específicas de clientes
        from modules.clientes import models as clientes_models
        from modules.tipo_cliente import models as tipo_cliente_models
        from modules.articulos import models as articulos_models

        try:
            clientes_models.Base.metadata.create_all(bind=current_engine)
            logger.info(f"Customers tables created in {get_current_database()}")
        except Exception as e:
            logger.exception(f"Error creating customer tables: {e}")

        try:
            tipo_cliente_models.Base.metadata.create_all(bind=current_engine)
            logger.info(f"Customer type tables created in {get_current_database()}")
        except Exception as e:
            logger.exception(f"Error creating customer type tables: {e}")

        try:
            articulos_models.Base.metadata.create_all(bind=current_engine)
            logger.info(f"Article tables created in {get_current_database()}")
        except Exception as e:
            logger.exception(f"Error creating article tables: {e}")

    else:
        # Otras bases de datos: tablas específicas de módulos
        from modules.clientes import models as clientes_models
        from modules.facturas import models as facturas_models
        from modules.articulos import models as articulos_models

        try:
            clientes_models.Base.metadata.create_all(bind=current_engine)
        except Exception as e:
            logger.exception(f"Error creating customer tables: {e}")

        try:
            facturas_models.Base.metadata.create_all(bind=current_engine)
        except Exception as e:
            logger.exception(f"Error creating invoice tables: {e}")

        try:
            articulos_models.Base.metadata.create_all(bind=current_engine)
        except Exception as e:
            logger.exception(f"Error creating article tables: {e}")

    # Intentar agregar columnas faltantes (migración automática simple)
    db_url = get_database_url(get_current_database())
    is_sqlite = 'sqlite' in db_url
    is_mysql = 'mysql' in db_url or 'mariadb' in db_url

    if is_sqlite or is_mysql:
        dialect = 'sqlite' if is_sqlite else 'mysql'
        
        if get_current_database() == 'artstudio3d':
            try:
                _ensure_columns(clientes_models.Base, dialect, engine=current_engine)
            except Exception:
                logger.exception("Error ensuring columns for clientes")
            try:
                _ensure_columns(tipo_cliente_models.Base, dialect, engine=current_engine)
            except Exception:
                logger.exception("Error ensuring columns for tipo_cliente")
        else:
            try:
                _ensure_columns(clientes_models.Base, dialect, engine=current_engine)
            except Exception:
                logger.exception("Error ensuring columns for clientes (other)")
            try:
                _ensure_columns(facturas_models.Base, dialect, engine=current_engine)
            except Exception:
                logger.exception("Error ensuring columns for facturas (other)")

    # Restaurar base de datos original si se cambió
    if db_name:
        set_current_database(original_db)


def init_main_db():
    """Inicializa las tablas globales en la base de datos principal."""
    init_db('main')


def init_artstudio3d_db():
    """Inicializa las tablas específicas en la base de datos ArtStudio3D."""
    init_db('artstudio3d')


def _get_sql_type(sa_type, dialect):
    """Mapea tipos de SQLAlchemy a tipos SQL según el dialecto."""
    if dialect == 'sqlite':
        if isinstance(sa_type, Integer): return 'INTEGER'
        if isinstance(sa_type, Float): return 'REAL'
        if isinstance(sa_type, DateTime): return 'DATETIME'
        if isinstance(sa_type, Date): return 'DATE'
        if isinstance(sa_type, Text): return 'TEXT'
        if isinstance(sa_type, String):
            return f'VARCHAR({sa_type.length})' if sa_type.length else 'VARCHAR'
        return 'TEXT'
    elif dialect == 'mysql':
        if isinstance(sa_type, Integer): return 'INT'
        if isinstance(sa_type, Float): return 'DOUBLE'
        if isinstance(sa_type, DateTime): return 'DATETIME'
        if isinstance(sa_type, Date): return 'DATE'
        if isinstance(sa_type, Text): return 'TEXT'
        if isinstance(sa_type, String):
            return f'VARCHAR({sa_type.length})' if sa_type.length else 'VARCHAR(255)'
        return 'TEXT'
    return 'TEXT'


def _ensure_columns(base, dialect, engine=None):
    """Asegura que las columnas del modelo existan en la base de datos.

    Use the `engine` passed in; default to get_engine(). Using a specific engine
    avoids accidentally operating on the global `engine` variable bound at import
    time and prevents unintended writes to the wrong DB.
    """
    if engine is None:
        engine = get_engine()

    inspector = inspect(engine)
    for table_name, table_obj in base.metadata.tables.items():
        if not inspector.has_table(table_name):
            continue
        existing_cols = {c['name'] for c in inspector.get_columns(table_name)}
        for col in table_obj.columns:
            col_name = col.name
            if col_name in existing_cols:
                continue
            # Skip primary key additions
            if col.primary_key:
                continue
            
            # Obtener tipo SQL
            sql_type = _get_sql_type(col.type, dialect)

            # Compose ALTER TABLE statement. Make column nullable to avoid issues.
            stmt = text(f'ALTER TABLE "{table_name}" ADD COLUMN "{col_name}" {sql_type}')
            
            # MySQL/MariaDB syntax uses backticks usually, but double quotes might work in ANSI mode.
            # Safer to use no quotes or backticks for MySQL if standard quotes fail, 
            # but SQLAlchemy 'text' usually passes raw SQL.
            # Let's try to be dialect specific for quoting if needed, but simple names usually work.
            if dialect == 'mysql':
                 stmt = text(f'ALTER TABLE `{table_name}` ADD COLUMN `{col_name}` {sql_type}')

            try:
                with engine.connect() as conn:
                    conn.execute(stmt)
                    logging.getLogger(__name__).info("Column added: %s.%s (%s)", table_name, col_name, sql_type)
            except Exception as e:
                # best-effort: ignore failures to avoid breaking startup
                logging.getLogger(__name__).warning("Error adding column %s.%s: %s", table_name, col_name, e)
                continue


# Funciones para gestión dinámica de bases de datos por empresa
def set_database_for_company(company_id: int, init: bool = False, initiator: str | None = None):
    """
    Configura la base de datos actual según la empresa seleccionada.
    Busca la configuración en la tabla empresas y cambia dinámicamente.
    """
    from .config import get_database_url_for_company

    try:
        url = get_database_url_for_company(company_id)

        # Agregar dinámicamente la configuración de la empresa
        db_key = f'company_{company_id}'
        DATABASE_CONFIGS[db_key] = url

        # Cambiar a la base de datos de la empresa
        set_current_database(db_key)

        logging.getLogger(__name__).debug("Database switched for company %s", company_id)

        # Optionally initialize the DB for the company (explicit init only)
        if init:
            logger = logging.getLogger('core.db.init')
            logger.info(f"init_db will run for company_{company_id} requested by {initiator}")
            init_db(initiator=initiator)

    except Exception as e:
        logging.getLogger(__name__).exception("ERROR configuring database for company %s: %s", company_id, e)
        raise

def get_company_database_info(company_id: int) -> dict:
    """
    Obtiene información de la base de datos configurada para una empresa.
    """
    from .config import get_database_url_for_company
    from core.models import Empresa

    # Cambiar temporalmente a BD principal
    original_db = get_current_database()
    set_current_database('main')

    try:
        session = get_session()
        empresa = session.query(Empresa).filter_by(id=company_id).first()

        if not empresa:
            raise ValueError(f"Empresa con ID {company_id} no encontrada")

        info = {
            'company_id': company_id,
            'company_name': empresa.nombre_fiscal,
            'motor_base_datos': empresa.motor_base_datos,
            'database_name': (empresa.nombre_base_datos_maria_db
                            if empresa.motor_base_datos == 'mariadb'
                            else empresa.nombre_base_datos_postgresql),
            'host': (empresa.host_mariadb
                    if empresa.motor_base_datos == 'mariadb'
                    else empresa.host_postgresql),
            'port': (empresa.puerto_mariadb
                    if empresa.motor_base_datos == 'mariadb'
                    else empresa.puerto_postgresql),
            'username': (empresa.usuario_mariadb
                        if empresa.motor_base_datos == 'mariadb'
                        else empresa.usuario_postgresql),
            'database_url': get_database_url_for_company(company_id)
        }

        return info

    finally:
        set_current_database(original_db)
        session.close()

def list_available_databases() -> list:
    """Lista todas las bases de datos configuradas."""
    return list(DATABASE_CONFIGS.keys())

def refresh_database_configs():
    """Refresca las configuraciones de base de datos desde el archivo de configuración."""
    from .config import config as env_config

    DATABASE_CONFIGS.update({
        'main': env_config.get_database_url('main'),
        'artstudio3d': env_config.get_database_url('artstudio3d'),
        'current': env_config.get_database_url('main')
    })

    logging.getLogger(__name__).debug("Database configurations refreshed")

def get_france_db_path():
    """Obtiene la ruta completa a la base de datos de Francia."""
    return os.path.join(os.path.dirname(__file__), '..', 'datos', 'france.db')

def get_qsql_database(connection_name: str = None):
    """
    Crea una conexión QSqlDatabase compatible con la configuración actual de SQLAlchemy.
    Soporta MySQL/MariaDB, PostgreSQL y SQLite automáticamente.
    Para uso con DBConsultaView y otros componentes Qt que requieren QSqlDatabase.
    """
    from PySide6.QtSql import QSqlDatabase
    
    # Usar la base de datos actual si no se especifica nombre
    if not connection_name:
        connection_name = f"qt_connection_{_current_db}"
    
    # Obtener URL de la base de datos actual
    db_url = DATABASE_CONFIGS.get(_current_db, DATABASE_CONFIGS['main'])
    
    # Remover conexión existente si existe
    if QSqlDatabase.contains(connection_name):
        QSqlDatabase.removeDatabase(connection_name)
    
    try:
        # MySQL/MariaDB
        if db_url.startswith('mysql+pymysql://'):
            url_without_prefix = db_url[16:]  # Quitar 'mysql+pymysql://'
            
            if '@' in url_without_prefix:
                auth_part, host_db_part = url_without_prefix.split('@', 1)
                user, password = auth_part.split(':', 1)
                
                if '/' in host_db_part:
                    host_port, database = host_db_part.split('/', 1)
                    if ':' in host_port:
                        host, port = host_port.split(':', 1)
                        port = int(port)
                    else:
                        host = host_port
                        port = 3306
                else:
                    host = host_db_part
                    port = 3306
                    database = ''
            else:
                user, password, host, port, database = '', '', 'localhost', 3306, ''
            
            # Probar diferentes drivers MySQL disponibles
            mysql_drivers = ['QMARIADB', 'QMYSQL']
            available_drivers = QSqlDatabase.drivers()
            
            for driver in mysql_drivers:
                if driver in available_drivers:
                    db = QSqlDatabase.addDatabase(driver, connection_name)
                    db.setHostName(host)
                    db.setPort(port)
                    db.setDatabaseName(database)
                    db.setUserName(user)
                    db.setPassword(password)
                    
                    if db.open():
                        logging.getLogger(__name__).info("QSqlDatabase connection created (%s): %s -> %s", driver, connection_name, database)
                        return db
                    else:
                        logging.getLogger(__name__).warning("Connection failed with %s: %s", driver, db.lastError().text())
                        QSqlDatabase.removeDatabase(connection_name)
            
            # Si MySQL falla, crear fallback con SQLite temporal
            logging.getLogger(__name__).warning("MySQL not available, using SQLite fallback for queries...")
            return _create_sqlite_fallback(connection_name)
        
        # PostgreSQL
        elif db_url.startswith('postgresql://') or db_url.startswith('postgresql+psycopg2://'):
            prefix_len = 13 if db_url.startswith('postgresql://') else 21
            url_without_prefix = db_url[prefix_len:]
            
            if '@' in url_without_prefix:
                auth_part, host_db_part = url_without_prefix.split('@', 1)
                user, password = auth_part.split(':', 1)
                
                if '/' in host_db_part:
                    host_port, database = host_db_part.split('/', 1)
                    if ':' in host_port:
                        host, port = host_port.split(':', 1)
                        port = int(port)
                    else:
                        host = host_port
                        port = 5432
                else:
                    host = host_db_part
                    port = 5432
                    database = ''
            else:
                user, password, host, port, database = '', '', 'localhost', 5432, ''
            
            if 'QPSQL' in QSqlDatabase.drivers():
                db = QSqlDatabase.addDatabase('QPSQL', connection_name)
                db.setHostName(host)
                db.setPort(port)
                db.setDatabaseName(database)
                db.setUserName(user)
                db.setPassword(password)
                
                if db.open():
                    logging.getLogger(__name__).info("QSqlDatabase connection created (QPSQL): %s -> %s", connection_name, database)
                    return db
                else:
                    logging.getLogger(__name__).warning("PostgreSQL connection failed: %s", db.lastError().text())
                    QSqlDatabase.removeDatabase(connection_name)
            
            # Fallback a SQLite para PostgreSQL
            logging.getLogger(__name__).warning("PostgreSQL not available, using SQLite fallback for queries...")
            return _create_sqlite_fallback(connection_name)
        
        # SQLite
        elif db_url.startswith('sqlite:///'):
            db_path = db_url[10:]  # Quitar 'sqlite:///'
            
            if 'QSQLITE' in QSqlDatabase.drivers():
                db = QSqlDatabase.addDatabase('QSQLITE', connection_name)
                db.setDatabaseName(db_path)
                
                if db.open():
                    logging.getLogger(__name__).info("QSqlDatabase connection created (QSQLITE): %s -> %s", connection_name, db_path)
                    return db
                else:
                    logging.getLogger(__name__).warning("Error opening SQLite connection: %s", db.lastError().text())
                    QSqlDatabase.removeDatabase(connection_name)
        
        logging.getLogger(__name__).warning("Unsupported database type: %s", db_url)
        return None
        
    except Exception as e:
        logging.getLogger(__name__).exception("Error al crear conexión QSqlDatabase")
        if QSqlDatabase.contains(connection_name):
            QSqlDatabase.removeDatabase(connection_name)
        return None

def _create_sqlite_fallback(connection_name: str):
    """
    Crea una base de datos SQLite temporal en memoria y copia los datos necesarios
    para que DBConsultaView funcione sin problemas.
    """
    from PySide6.QtSql import QSqlDatabase
    import tempfile
    import os
    
    try:
        # Crear archivo temporal SQLite
        temp_fd, temp_path = tempfile.mkstemp(suffix='.db', prefix='creative_erp_temp_')
        os.close(temp_fd)  # Cerrar el descriptor de archivo
        
        # Crear conexión SQLite
        if 'QSQLITE' in QSqlDatabase.drivers():
            db = QSqlDatabase.addDatabase('QSQLITE', connection_name)
            db.setDatabaseName(temp_path)

            if db.open():
                logging.getLogger(__name__).info("SQLite temporal creado: %s", temp_path)

                # Marcar como temporal para limpieza posterior
                db._temp_path = temp_path
                return db
            else:
                os.unlink(temp_path)  # Limpiar archivo si falla
                return None
        
        os.unlink(temp_path)  # Limpiar si no hay QSQLITE
        return None
        
    except Exception:
        logging.getLogger(__name__).exception("Error creando SQLite temporal")
        return None

def populate_sqlite_temp_with_data(qt_db, table_name: str, data: list, columns: list):
    """
    Llena una tabla SQLite temporal con datos para usar en DBConsultaView
    """
    from PySide6.QtSql import QSqlQuery
    
    try:
        query = QSqlQuery(qt_db)
        
        # Crear tabla
        columns_sql = ", ".join([f"{col} TEXT" for col in columns])
        if not query.exec(f"CREATE TABLE {table_name} ({columns_sql})"):
            logging.getLogger(__name__).warning("Error creando tabla temporal: %s", query.lastError().text())
            return False
        
        # Insertar datos
        placeholders = ", ".join(['?' for _ in columns])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        query.prepare(insert_sql)
        
        for row_data in data:
            for i, col in enumerate(columns):
                query.addBindValue(row_data.get(col, ''))
            
            if not query.exec():
                logging.getLogger(__name__).warning("Error insertando fila: %s", query.lastError().text())
                continue
        
        logging.getLogger(__name__).info("Tabla temporal %s poblada con %d registros", table_name, len(data))
        return True
        
    except Exception:
        logging.getLogger(__name__).exception("Error poblando tabla temporal")
        return False