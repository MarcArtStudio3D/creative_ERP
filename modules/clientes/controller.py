"""
Controller Peewee para el módulo de Clientes.
Maneja la lógica de negocio entre la vista y el repositorio.
"""

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel

from .repository import ClienteRepository

logger = logging.getLogger(__name__)


class ClientesController(QObject):
    """Controlador para el módulo de Clientes usando Peewee."""

    # Señales para comunicar eventos a la vista
    data_changed = Signal()
    error_occurred = Signal(str)
    operation_success = Signal(str)
    cliente_changed = Signal(int)  # Emite el ID del cliente cuando cambia

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repository = ClienteRepository()
        self._current_cliente: Optional[Dict] = None
        self._clientes_cache: List[Dict] = []
        self._current_index: int = -1

        # Modelo Qt para la tabla (compatibilidad con vista)
        self.model = QStandardItemModel(0, 5)
        self.model.setHorizontalHeaderLabels(
            ["Código", "NIF/CIF", "Nombre Fiscal", "Teléfono", "Email"]
        )

        logger.debug("ClientesController inicializado con Peewee")

    # ========== Propiedades ==========

    def get_current_cliente(self) -> Optional[Dict]:
        """Obtiene el cliente actual."""
        return self._current_cliente

    def set_current_cliente(self, cliente: Dict):
        """Establece el cliente actual."""
        self._current_cliente = cliente
        if cliente and cliente.get('id'):
            self.cliente_changed.emit(cliente['id'])

    # ========== Propiedades de compatibilidad ==========

    @property
    def cliente_actual(self) -> Optional[Dict]:
        """Propiedad para compatibilidad con vista."""
        return self._current_cliente

    @cliente_actual.setter
    def cliente_actual(self, value: Optional[Dict]):
        """Setter para compatibilidad con vista."""
        self._current_cliente = value
        if value and value.get('id'):
            self.cliente_changed.emit(value['id'])

    # ========== Carga de datos ==========

    def get_clientes(self, filtro: str = "", limit: int = None, offset: int = 0) -> List[Dict]:
        """Obtiene lista de clientes."""
        try:
            clientes = self.repository.get_all(filtro=filtro, limit=limit, offset=offset)
            self._clientes_cache = clientes
            return clientes
        except Exception as e:
            logger.exception("Error getting clientes: %s", e)
            self.error_occurred.emit(f"Error al cargar clientes: {str(e)}")
            return []

    def load_by_id(self, id_cliente: int) -> bool:
        """Carga un cliente por su ID."""
        try:
            cliente = self.repository.get_by_id(id_cliente)
            if cliente:
                self._current_cliente = cliente
                self.cliente_changed.emit(id_cliente)
                return True
            return False
        except Exception as e:
            logger.exception("Error loading cliente by id: %s", e)
            self.error_occurred.emit(f"Error al cargar cliente: {str(e)}")
            return False

    def load_by_codigo(self, codigo: str) -> bool:
        """Carga un cliente por su código."""
        try:
            cliente = self.repository.get_by_codigo(codigo)
            if cliente:
                self._current_cliente = cliente
                if cliente.get('id'):
                    self.cliente_changed.emit(cliente['id'])
                return True
            return False
        except Exception as e:
            logger.exception("Error loading cliente by codigo: %s", e)
            self.error_occurred.emit(f"Error al cargar cliente: {str(e)}")
            return False

    # ========== CRUD ==========

    def add_new(self) -> bool:
        """Inicia la creación de un nuevo cliente."""
        try:
            # Crear cliente vacío
            self._current_cliente = {
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
            return True
        except Exception as e:
            logger.exception("Error in add_new: %s", e)
            self.error_occurred.emit(f"Error al crear nuevo cliente: {str(e)}")
            return False

    def save_current_cliente(self) -> bool:
        """Guarda el cliente actual."""
        try:
            if not self._current_cliente:
                return False

            if self._current_cliente.get('id'):
                # Actualizar existente
                cliente = self.repository.update(self._current_cliente['id'], self._current_cliente)
            else:
                # Crear nuevo
                cliente = self.repository.create(self._current_cliente)

            if cliente:
                self._current_cliente = cliente
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
            success = self.repository.delete(id_cliente)
            if success:
                self.operation_success.emit("Cliente eliminado correctamente")
                self.data_changed.emit()
                if self._current_cliente and self._current_cliente.get('id') == id_cliente:
                    self._current_cliente = None
            return success
        except Exception as e:
            logger.exception("Error deleting cliente: %s", e)
            self.error_occurred.emit(f"Error al eliminar cliente: {str(e)}")
            return False

    def undo_current_cliente(self):
        """Deshace cambios en el cliente actual."""
        try:
            if self._current_cliente and self._current_cliente.get('id'):
                # Recargar desde BD
                self.load_by_id(self._current_cliente['id'])
        except Exception as e:
            logger.exception("Error undoing cliente: %s", e)

    # ========== Navegación ==========

    def next_cliente(self) -> bool:
        """Navega al siguiente cliente."""
        try:
            if not self._current_cliente or not self._current_cliente.get('id'):
                return False

            next_cliente = self.repository.get_next(self._current_cliente['id'])
            if next_cliente:
                self._current_cliente = next_cliente
                self.cliente_changed.emit(next_cliente['id'])
                return True
            return False
        except Exception as e:
            logger.exception("Error navigating to next cliente: %s", e)
            return False

    def prev_cliente(self) -> bool:
        """Navega al cliente anterior."""
        try:
            if not self._current_cliente or not self._current_cliente.get('id'):
                return False

            prev_cliente = self.repository.get_prev(self._current_cliente['id'])
            if prev_cliente:
                self._current_cliente = prev_cliente
                self.cliente_changed.emit(prev_cliente['id'])
                return True
            return False
        except Exception as e:
            logger.exception("Error navigating to prev cliente: %s", e)
            return False

    # ========== Utilidades ==========

    def count(self, filtro: str = "") -> int:
        """Cuenta el número total de clientes."""
        try:
            return self.repository.count(filtro)
        except Exception as e:
            logger.exception("Error counting clientes: %s", e)
            return 0

    def search(self, filtro: str) -> List[Dict]:
        """Busca clientes por filtro."""
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
                items = [
                    QStandardItem(cliente.get("codigo_cliente", "") or ""),
                    QStandardItem(cliente.get("cif_nif_siren", "") or ""),
                    QStandardItem(cliente.get("nombre_fiscal", "") or ""),
                    QStandardItem(cliente.get("telefono1", "") or ""),
                    QStandardItem(cliente.get("email", "") or ""),
                ]
                # Guardar el ID del cliente en el primer item para recuperarlo al hacer doble click
                items[0].setData(cliente.get("id"))
                self.model.appendRow(items)
            self.data_changed.emit()
        except Exception as e:
            logger.exception("Error loading clientes: %s", e)
            self.error_occurred.emit(f"Error al cargar clientes: {str(e)}")

    def obtener_cliente(self, id_cliente: int) -> Optional[Dict]:
        """Obtiene un cliente por ID (compatibilidad con vista)."""
        return self.repository.get_by_id(id_cliente)

    def obtener_cliente_por_codigo(self, codigo: str) -> Optional[Dict]:
        """Obtiene un cliente por código (compatibilidad con vista)."""
        return self.repository.get_by_codigo(codigo)

    def nuevo_cliente(self) -> Dict:
        """Crea un nuevo cliente vacío (compatibilidad con vista)."""
        self.add_new()
        return self._current_cliente

    def guardar_cliente(self, cliente: Dict) -> Optional[Dict]:
        """Guarda un cliente (compatibilidad con vista)."""
        try:
            self._current_cliente = cliente
            if self.save_current_cliente():
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

    def buscar_poblacion_por_cp(self, cp: str, pais: str = "Francia"):
        """Busca población por código postal (stub para compatibilidad)."""
        # TODO: Implementar si se necesita
        logger.warning("buscar_poblacion_por_cp not implemented yet")
        return [], None, None

    def buscar_cp_por_poblacion_simple(self, poblacion: str, pais: str = "Francia"):
        """Busca CP por población (stub para compatibilidad)."""
        # TODO: Implementar si se necesita
        logger.warning("buscar_cp_por_poblacion_simple not implemented yet")
        return []

    def buscar_poblacion_por_cp_alternativa(self, cp: str, pais: str = "Francia"):
        """Busca población por CP alternativa (stub para compatibilidad)."""
        # TODO: Implementar si se necesita
        logger.warning("buscar_poblacion_por_cp_alternativa not implemented yet")
        return []

    def buscar_cp_por_poblacion_alternativa(self, poblacion: str, pais: str = "Francia"):
        """Busca CP por población alternativa (stub para compatibilidad)."""
        # TODO: Implementar si se necesita
        logger.warning("buscar_cp_por_poblacion_alternativa not implemented yet")
        return []

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
                if cliente.get('id') == cliente_id:
                    return i
            return -1
        except:
            return -1
