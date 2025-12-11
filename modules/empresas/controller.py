import logging
from typing import List, Optional

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel

from modules.empresas.repository_sql import EmpresaRepository
from modules.empresas.models import Empresa
from core.models_dataclass import BusinessGroup


class EmpresasController(QObject):
    """Controlador para el módulo de Empresas."""

    # Señales para comunicar eventos a la vista
    data_changed = Signal()
    error_occurred = Signal(str)
    operation_success = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = EmpresaRepository()
        self.model = QStandardItemModel(0, 4)
        self.model.setHorizontalHeaderLabels(
            ["Código", "Nombre Fiscal", "CIF/NIF", "Población"]
        )
        self._empresa_actual: Optional[Empresa] = None

    @property
    def empresa_actual(self) -> Optional[Empresa]:
        return self._empresa_actual

    @empresa_actual.setter
    def empresa_actual(self, value: Optional[Empresa]):
        self._empresa_actual = value

    def cargar_empresas(self):
        """Carga las empresas en el modelo."""
        self.model.removeRows(0, self.model.rowCount())
        try:
            empresas = self.repo.obtener_todos()
            for e in empresas:
                items = [
                    QStandardItem(e.codigo_empresa or ""),
                    QStandardItem(e.nombre_fiscal or ""),
                    QStandardItem(e.cif_nif or ""),
                    QStandardItem(e.poblacion or ""),
                ]
                for it in items:
                    it.setEditable(False)

                # Almacenar el ID en la primera columna como datos ocultos
                items[0].setData(e.id, Qt.ItemDataRole.UserRole)

                self.model.appendRow(items)
            self.data_changed.emit()
        except Exception as e:
            self.error_ocurrido.emit(f"No se pudieron cargar empresas: {e}")

    def obtener_empresa(self, id_: int) -> Optional[Empresa]:
        """Obtiene una empresa por ID."""
        try:
            empresa = self.repo.obtener_por_id(id_)
            if empresa:
                self.empresa_actual = empresa
                return empresa
            else:
                self.error_occurred.emit("Empresa no encontrada")
                return None
        except Exception as e:
            self.error_occurred.emit(f"Error al obtener empresa: {e}")
            return None

    def nueva_empresa(self):
        """Prepara para una nueva empresa."""
        self.empresa_actual = None

    def guardar_empresa(self, empresa: Empresa) -> bool:
        """Guarda la empresa actual."""
        try:
            self.repo.guardar(empresa)
            self.empresa_actual = empresa
            self.cargar_empresas()
            self.operation_success.emit("Empresa guardada correctamente")
            return True
        except Exception as e:
            self.error_occurred.emit(f"Error al guardar: {e}")
            return False

    def borrar_empresa(self, id_: int) -> bool:
        """Borra una empresa por ID."""
        try:
            empresa = self.repo.obtener_por_id(id_)
            if not empresa:
                self.error_occurred.emit("Empresa no encontrada")
                return False

            self.repo.borrar(empresa)
            self.cargar_empresas()
            self.operation_success.emit("Empresa borrada correctamente")
            return True
        except Exception as e:
            self.error_occurred.emit(f"Error al borrar: {e}")
            return False

    def cargar_grupos(self) -> List[BusinessGroup]:
        """Carga todos los grupos empresariales."""
        try:
            return self.repo.obtener_grupos()
        except Exception as e:
            self.error_occurred.emit(f"Error al cargar grupos: {e}")
            return []

    def llenar_combo_grupos(self, combo):
        """Llena un QComboBox con los grupos empresariales."""
        grupos = self.cargar_grupos()
        combo.clear()
        for grupo in grupos:
            combo.addItem(grupo.name, grupo.id)

    def obtener_paises(self):
        """Obtiene la lista de países."""
        return self.repo.obtener_paises()

    def buscar_poblacion(self, cp: str, pais: str):
        """Busca población por código postal."""
        return self.repo.buscar_poblacion(cp, pais)

    def buscar_codigos_postales(self, poblacion: str, pais: str):
        """Busca códigos postales por nombre de población."""
        return self.repo.buscar_codigos_postales(poblacion, pais)

    def crear_y_inicializar_db(
        self, company_id: int, engine_type: str, initiator: str | None = None
    ) -> bool:
        """Crea la base de datos en el motor especificado y la inicializa (init_db).

        engine_type: 'mariadb' or 'postgresql'
        initiator: username or id for audit logs
        Returns True on success, False on failure.
        """
        logger = logging.getLogger("modules.empresas.controller")

        try:
            empresa = self.obtener_por_id_internal(company_id)
            if not empresa:
                self.error_ocurrido.emit(self.tr("Empresa no encontrada"))
                return False

            # Pick DB connection info depending on engine type
            if engine_type == "mariadb":
                host = getattr(empresa, "host_mariadb", None)
                port = int(getattr(empresa, "puerto_mariadb", 3306) or 3306)
                dbname = getattr(empresa, "nombre_base_datos_maria_db", None)
                user = getattr(empresa, "usuario_mariadb", None)
                pwd = getattr(empresa, "password_mariadb", None)
                default_db = "mysql"
                driver = "mysql+pymysql"
            else:
                # default to postgresql
                host = getattr(empresa, "host_postgresql", None)
                port = int(getattr(empresa, "puerto_postgresql", 5432) or 5432)
                dbname = getattr(empresa, "nombre_base_datos_postgresql", None)
                user = getattr(empresa, "usuario_postgresql", None)
                pwd = getattr(empresa, "password_postgresql", None)
                default_db = "postgres"
                driver = "postgresql+psycopg2"

            if not host or not dbname:
                self.error_ocurrido.emit(
                    self.tr("Faltan datos de conexión para crear la BD")
                )
                return False

            # Try to connect to the server (default database) and create the DB
            try:
                # If credentials missing, try using main DB admin credentials from config
                if not user:
                    from core.config import config as env_config

                    # attempt to use main database credentials as fallback
                    main_url = env_config.get_database_url("main")
                    # parse main_url (simple split) to extract user/pwd
                    # format: driver://user:pass@host:port/db
                    try:
                        suffix = main_url.split("://", 1)[1]
                        creds_host = suffix.split("@", 1)[0]
                        if ":" in creds_host:
                            u, p = creds_host.split(":", 1)
                            user = user or u
                            pwd = pwd or p
                    except Exception:
                        pass

                engine_url = f"{driver}://{user}:{pwd}@{host}:{port}/{default_db}"

                from core.db import get_engine_from_url

                tmp_engine = get_engine_from_url(engine_url)
                with tmp_engine.connect() as conn:
                    # Create database for MariaDB/Postgres with safe charset/collation for MySQL
                    if engine_type == "mariadb":
                        stmt = text(
                            f"CREATE DATABASE IF NOT EXISTS `{dbname}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                        )
                    else:
                        # PostgreSQL: try to create database (requires superuser normally)
                        stmt = text(f'CREATE DATABASE "{dbname}";')
                    try:
                        conn.execute(stmt)
                    except Exception as e:
                        # Some servers may disallow CREATE DATABASE in transactions; log and continue
                        logger.info(f"DB create stmt failed: {e}")
                        # attempt raw SQL execution
                        try:
                            conn.execute(text(str(stmt)))
                        except Exception:
                            logger.exception(
                                "Failed to create database (may need admin privileges)"
                            )
                            # continue, maybe DB exists or admin required

            except Exception as outer_e:
                logger.exception(
                    f"Error conectando al servidor para crear la BD: {outer_e}"
                )
                # still proceed to initialization attempt (it may already exist)

            # Now initialize schema in the target DB (this will create tables via init_db)
            try:
                set_database_for_company(company_id, init=True, initiator=initiator)
                self.operation_success.emit(
                    self.tr("Base de datos creada/inicializada")
                )
                return True
            except Exception as e:
                logger.exception(f"Error inicializando BD para la empresa: {e}")
                self.error_ocurrido.emit(str(e))
                return False

        except Exception as e:
            logger.exception(f"Unexpected error en crear_y_inicializar_db: {e}")
            self.error_ocurrido.emit(str(e))
            return False

    def obtener_por_id_internal(self, id_: int) -> Optional[Empresa]:
        """Helper internal: obtiene empresa sin emitir señales."""
        try:
            return self.repo.obtener_por_id(id_)
        except Exception:
            return None
