"""
Controller para el módulo de Clientes usando SQL directo.
Maneja la lógica de negocio entre la vista y el repositorio.
"""

import logging
from typing import List, Optional, Dict

from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel

from .repository_sql import ClienteRepository

logger = logging.getLogger(__name__)


class ClientesController(QObject):
    """Controlador para el módulo de Clientes usando SQL directo (sin ORM)."""

    # Señales para comunicar eventos a la vista
    data_changed = Signal()
    error_occurred = Signal(str)
    operation_success = Signal(str)
    cliente_changed = Signal(int)  # Emite el ID del cliente cuando cambia

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repository = ClienteRepository()
        # Ahora guardamos dicts en lugar de modelos ORM
        self._current_cliente: Optional[Dict] = None
        self._clientes_cache: List[Dict] = []
        self._current_index: int = -1

        # Modelo Qt para la tabla (compatibilidad con vista)
        self.model = QStandardItemModel(0, 5)
        self.model.setHorizontalHeaderLabels(
            ["Código", "NIF/CIF", "Nombre Fiscal", "Teléfono", "Email"]
        )

        logger.debug("ClientesController inicializado con SQL directo")

    # ========== Propiedades ==========

    def get_current_cliente(self) -> Optional[Dict]:
        """Obtiene el cliente actual (diccionario)."""
        return self._current_cliente

    def set_current_cliente(self, cliente: Dict):
        """Establece el cliente actual."""
        self._current_cliente = cliente
        cid = cliente.get("id", None)
        if cid:
            self.cliente_changed.emit(int(cid))

    # ========== Propiedades de compatibilidad ==========

    @property
    def cliente_actual(self) -> Optional[Dict]:
        """Propiedad para compatibilidad con vista."""
        return self._current_cliente

    @cliente_actual.setter
    def cliente_actual(self, value: Optional[Dict]):
        """Setter para compatibilidad con vista."""
        self._current_cliente = value
        cid = getattr(value, "id", None)
        if cid:
            self.cliente_changed.emit(int(cid))

    # ========== Carga de datos ==========

    def get_clientes(self, filtro: str = "", limit: int = None, offset: int = 0) -> List[Dict]:
        """Obtiene lista de clientes (instancias de modelo)."""
        try:
            clientes = self.repository.obtener_todos(filtro=filtro, limit=limit, offset=offset)
            self._clientes_cache = clientes
            return clientes
        except Exception as e:
            logger.exception("Error getting clientes: %s", e)
            self.error_occurred.emit(f"Error al cargar clientes: {str(e)}")
            return []

    def load_by_id(self, id_cliente: int) -> bool:
        """Carga un cliente por su ID."""
        try:
            cliente = self.repository.obtener_por_id(id_cliente)
            if cliente:
                self._current_cliente = cliente
                cid = cliente.get("id", None)
                if cid:
                    self.cliente_changed.emit(int(cid))
                return True
            return False
        except Exception as e:
            logger.exception("Error loading cliente by id: %s", e)
            self.error_occurred.emit(f"Error al cargar cliente: {str(e)}")
            return False

    def load_by_codigo(self, codigo: str) -> bool:
        """Carga un cliente por su código."""
        try:
            cliente = self.repository.obtener_por_codigo(codigo)
            if cliente:
                self._current_cliente = cliente
                cid = cliente.get("id", None)
                if cid:
                    self.cliente_changed.emit(int(cid))
                return True
            return False
        except Exception as e:
            logger.exception("Error loading cliente by codigo: %s", e)
            self.error_occurred.emit(f"Error al cargar cliente: {str(e)}")
            return False

    # ========== CRUD ==========

    def add_new(self) -> bool:
        """Inicia la creación de un nuevo cliente. Crea instancia no guardada."""
        try:
            # Crear cliente vacío como instancia de modelo (no guardada)
            data = {
                'id': None,
                'codigo_cliente': '',
                'nombre_fiscal': '',
                'cif_nif_siren': '',
                'direccion1': '',
                'cp': '',
                'poblacion': '',
                'provincia': '',
                'pais': 'España',
                'telefono1': '',
                'email': '',
                'bloqueado': False,
                'grupo_iva': 1,
                'id_divisa': 1,
                'id_idioma_documentos': 1,
            }
            # Instancia de Cliente sin salvar
            self._current_cliente = Cliente(**{k: v for k, v in data.items() if k != 'id'})
            return True
        except Exception as e:
            logger.exception("Error in add_new: %s", e)
            self.error_occurred.emit(f"Error al crear nuevo cliente: {str(e)}")
            return False

    def save_current_cliente(self) -> bool:
        """Guarda el cliente actual en la BD usando el repositorio."""
        # nueva firma con flags para forzar comportamiento
        return self.save_current_cliente_with_flags()

    def create_cliente(self, data: Dict) -> Optional[Dict]:
        """Crea un cliente delegando al repositorio."""
        try:
            return self.repository.crear(data)
        except Exception as e:
            logger.exception("Error in create_cliente: %s", e)
            return None

    def update_cliente(self, id_cliente: int, data: Dict) -> Optional[Dict]:
        """Actualiza un cliente delegando al repositorio."""
        try:
            return self.repository.actualizar(id_cliente, data)
        except Exception as e:
            logger.exception("Error in update_cliente: %s", e)
            return None

    def save_current_cliente_with_flags(self, force_create: bool = False, force_update: bool = False) -> bool:
        """Guarda el cliente actual con control explícito de crear o actualizar.

        - force_create: forzar creación (llama a create)
        - force_update: forzar actualización (llama a update)
        Si no se fuerza, se decide por la presencia de `id` en `_current_cliente`.
        """
        try:
            if not self._current_cliente:
                return False

            data = self._current_cliente  # Ya es un dict, no necesita conversión
            cid = self._current_cliente.get('id', None)

            cliente: Optional[Dict] = None
            if force_create:
                cliente = self.create_cliente(data)
            elif force_update:
                if cid is None:
                    # No hay id para update
                    return False
                cliente = self.update_cliente(int(cid), data)
            else:
                if cid:
                    cliente = self.update_cliente(int(cid), data)
                else:
                    cliente = self.create_cliente(data)

            if cliente:
                self._current_cliente = cliente
                cid = getattr(cliente, 'id', None)
                if cid:
                    self.cliente_changed.emit(int(cid))
                self.operation_success.emit("Cliente guardado correctamente")
                self.data_changed.emit()
                return True
            return False
        except Exception as e:
            logger.exception("Error saving cliente: %s", e)
            self.error_occurred.emit(f"Error al guardar cliente: {str(e)}")
            return False

    def delete_cliente(self, id_cliente: int) -> bool:
        """Elimina un cliente."""
        try:
            success = self.repository.eliminar(id_cliente)
            if success:
                self.operation_success.emit("Cliente eliminado correctamente")
                self.data_changed.emit()
                if self._current_cliente and self._current_cliente.get('id', None) == id_cliente:
                    self._current_cliente = None
            return success
        except Exception as e:
            logger.exception("Error deleting cliente: %s", e)
            self.error_occurred.emit(f"Error al eliminar cliente: {str(e)}")
            return False

    def undo_current_cliente(self):
        """Deshace cambios en el cliente actual (recarga desde BD si existe)."""
        try:
            cid = self._current_cliente.get('id', None)
            if cid:
                self.load_by_id(int(cid))
        except Exception as e:
            logger.exception("Error undoing cliente: %s", e)

    # ========== Navegación ==========

    def next_cliente(self) -> bool:
        """Navega al siguiente cliente."""
        try:
            cid = self._current_cliente.get('id', None)
            if not cid:
                return False

            next_cliente = self.repository.obtener_siguiente(int(cid))
            if next_cliente:
                self._current_cliente = next_cliente
                self.cliente_changed.emit(int(next_cliente.get('id')))
                return True
            return False
        except Exception as e:
            logger.exception("Error navigating to next cliente: %s", e)
            return False

    def prev_cliente(self) -> bool:
        """Navega al cliente anterior."""
        try:
            cid = self._current_cliente.get('id', None)
            if not cid:
                return False

            prev_cliente = self.repository.obtener_anterior(int(cid))
            if prev_cliente:
                self._current_cliente = prev_cliente
                self.cliente_changed.emit(int(prev_cliente.get('id')))
                return True
            return False
        except Exception as e:
            logger.exception("Error navigating to prev cliente: %s", e)
            return False

    # ========== Utilidades ==========

    def count(self, filtro: str = "") -> int:
        """Cuenta el número total de clientes."""
        try:
            return self.repository.contar_todos(filtro)
        except Exception as e:
            logger.exception("Error counting clientes: %s", e)
            return 0

    def search(self, filtro: str) -> List[Dict]:
        """Busca clientes por filtro (devuelve instancias)."""
        return self.get_clientes(filtro=filtro)

    def refresh(self):
        """Refresca los datos."""
        try:
            self.data_changed.emit()
        except Exception as e:
            logger.exception("Error refreshing: %s", e)

    # ========== Métodos de compatibilidad con la vista antigua ==========

    def cargar_clientes(self, filtro: str = ""):
        """Carga los clientes en el modelo Qt (compatibilidad con vista)."""
        self.model.removeRows(0, self.model.rowCount())
        try:
            clientes = self.get_clientes(filtro=filtro)
            for cliente in clientes:
                # Obtener valores de forma segura desde el diccionario
                codigo = cliente.get('codigo_cliente', '') or ''
                nif = cliente.get('cif_nif_siren', '') or ''
                nombre = cliente.get('nombre_fiscal', '') or ''
                telefono = cliente.get('telefono1', '') or ''
                email = cliente.get('email', '') or ''

                items = [QStandardItem(codigo), QStandardItem(nif), QStandardItem(nombre), QStandardItem(telefono), QStandardItem(email)]
                # Guardar el ID del cliente en el primer item para recuperarlo al hacer doble click
                cid = cliente.get('id', None)
                if cid is not None:
                    items[0].setData(int(cid), Qt.ItemDataRole.UserRole)
                self.model.appendRow(items)
            self.data_changed.emit()
        except Exception as e:
            logger.exception("Error loading clientes: %s", e)
            self.error_occurred.emit(f"Error al cargar clientes: {str(e)}")

    def obtener_cliente(self, id_cliente: int) -> Optional[Dict]:
        """Obtiene un cliente por ID (compatibilidad con vista)."""
        return self.repository.obtener_por_id(id_cliente)

    def obtener_cliente_por_codigo(self, codigo: str) -> Optional[Dict]:
        """Obtiene un cliente por código (compatibilidad con vista)."""
        return self.repository.obtener_por_codigo(codigo)

    def nuevo_cliente(self) -> Dict:
        """Crea un nuevo cliente vacío (compatibilidad con vista)."""
        self.add_new()
        return self._current_cliente

    def guardar_cliente(self, cliente: Dict) -> Optional[Dict]:
        """Guarda un cliente (compatibilidad con vista)."""
        try:
            # Nueva firma: aceptar flags opcionales dentro de un dict especial o kwargs
            force_create = False
            force_update = False

            # Si se pasa una tupla (cliente, flags) o kwargs, soportarlo suavemente
            if isinstance(cliente, tuple) and len(cliente) >= 2:
                cliente_obj = cliente[0]
                flags = cliente[1] or {}
                force_create = bool(flags.get('force_create', False))
                force_update = bool(flags.get('force_update', False))
            elif isinstance(cliente, dict) and '___flags' in cliente:
                flags = cliente.pop('___flags')
                cliente_obj = Cliente(**{k: v for k, v in cliente.items() if k != 'id'})
                force_create = bool(flags.get('force_create', False))
                force_update = bool(flags.get('force_update', False))
            else:
                cliente_obj = cliente if not isinstance(cliente, dict) else Cliente(**{k: v for k, v in cliente.items() if k != 'id'})

            self._current_cliente = cliente_obj
            if self.save_current_cliente_with_flags(force_create=force_create, force_update=force_update):
                return self._current_cliente
            return None
        except Exception as e:
             logger.exception("Error saving cliente: %s", e)
             self.error_occurred.emit(f"Error al guardar cliente: {str(e)}")
             return None

    def borrar_cliente(self, id_cliente: int) -> bool:
        """Elimina un cliente (compatibilidad con vista)."""
        return self.delete_cliente(id_cliente)

    def buscar_clientes(self, termino: str) -> List[Dict]:
        """Busca clientes por término (compatibilidad con vista)."""
        return self.search(termino)

    def obtener_paises(self) -> List[tuple]:
        """Obtiene lista de países (stub para compatibilidad)."""
        # TODO: Implementar si se necesita
        return [("España", "España"), ("Francia", "Francia")]

    # Métodos de CP/poblacion siguen siendo stubs

    def obtener_cliente_en_posicion(self, posicion: int) -> Optional[Dict]:
        """Obtiene cliente en posición (stub para compatibilidad)."""
        try:
            if 0 <= posicion < len(self._clientes_cache):
                return self._clientes_cache[posicion]
            return None
        except:
            return None

    def obtener_posicion_cliente(self, cliente_id: int) -> int:
        """Obtiene posición de cliente en caché (stub para compatibilidad)."""
        try:
            for i, cliente in enumerate(self._clientes_cache):
                if getattr(cliente, 'id', None) == cliente_id:
                    return i
            return -1
        except:
            return -1

    # ==================== Búsqueda de Códigos Postales ====================

    def buscar_poblacion_por_cp(self, cp: str, pais: str = "España"):
        """
        Busca población por código postal en las bases de datos SQLite de países.

        Args:
            cp: Código postal a buscar
            pais: País ("España" o "Francia")

        Returns:
            Tupla (resultados, db_path, db_config) donde:
            - resultados: Lista de dicts con cp, poblacion, provincia
            - db_path: Ruta al archivo de BD
            - db_config: Configuración de conexión
        """
        import sqlite3
        import os
        from pathlib import Path

        try:
            # Determinar la base de datos según el país
            base_dir = Path(__file__).parent.parent.parent / "datos"

            # Determinar la base de datos y campos según el país
            if pais.lower() in ["francia", "france"]:
                db_path = base_dir / "france.db"
                tabla = "villes"  # Tabla correcta para Francia
                campo_cp = "code_postal"
                campo_poblacion = "nom_standard"
                campo_provincia = "dep_nom"
            else:  # España por defecto
                db_path = base_dir / "spain.sqlite"
                tabla = "codigospostales"
                campo_cp = "cp"
                campo_poblacion = "poblacion"
                campo_provincia = "provincia"

            if not db_path.exists():
                logger.warning(f"No se encontró la BD de códigos postales: {db_path}")
                return ([], str(db_path), None)

            # Conectar a SQLite
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row  # Para obtener resultados como dict
            cursor = conn.cursor()

            # Buscar código postal
            query = f"SELECT * FROM {tabla} WHERE {campo_cp} = ?"
            cursor.execute(query, (cp,))
            rows = cursor.fetchall()

            # Convertir a lista de dicts
            resultados = []
            for row in rows:
                resultados.append({
                    'cp': row[campo_cp],
                    'poblacion': row[campo_poblacion] if campo_poblacion in row.keys() else '',
                    'provincia': row[campo_provincia] if campo_provincia in row.keys() else ''
                })

            conn.close()

            # Retornar tupla con formato esperado por la vista:
            # (resultados, db_path, db_config)
            # donde db_config es una tupla de 5 elementos: (db_path, tabla, campo_cp, campo_poblacion, campo_provincia)
            db_config = (str(db_path), tabla, campo_cp, campo_poblacion, campo_provincia)
            return (resultados, str(db_path), db_config)

        except Exception as e:
            logger.error(f"Error buscando código postal {cp} en {pais}: {e}")
            return ([], "", (None, None, None, None, None))

    def buscar_poblacion_por_cp_alternativa(self, cp: str, pais: str = "España"):
        """
        Busca población por código postal para direcciones alternativas.
        Wrapper del método principal para compatibilidad.

        Args:
            cp: Código postal
            pais: País

        Returns:
            Tupla (resultados, db_path, db_config)
        """
        return self.buscar_poblacion_por_cp(cp, pais)

