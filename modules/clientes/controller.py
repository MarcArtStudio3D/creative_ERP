import os
import sqlite3
from typing import List, Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from sqlalchemy.orm import Session

from modules.clientes.models import Cliente
from modules.clientes.repository import ClienteRepository


class ClientesController(QObject):
    """Controlador para el módulo de Clientes."""

    # Señales para comunicar eventos a la vista
    data_changed = Signal()
    error_occurred = Signal(str)
    operation_success = Signal(str)
    cliente_changed = Signal(int)  # Emite el ID del cliente cuando cambia

    def __init__(self, session: Session, parent=None):
        super().__init__(parent)
        self.session = session
        self.repository = ClienteRepository(session)
        self.model = QStandardItemModel(0, 5)
        self.model.setHorizontalHeaderLabels(
            ["Código", "NIF/CIF", "Nombre Fiscal", "Teléfono", "Email"]
        )
        self._cliente_actual: Optional[Cliente] = None
        self._view_reference = parent  # Referencia a la vista para callbacks

    @property
    def cliente_actual(self) -> Optional[Cliente]:
        return self._cliente_actual

    @cliente_actual.setter
    def cliente_actual(self, value: Optional[Cliente]):
        self._cliente_actual = value
        if value and hasattr(value, "id"):
            self.cliente_changed.emit(value.id)

    def cargar_clientes(self, filtro: str = ""):
        """Carga los clientes en el modelo."""
        self.model.removeRows(0, self.model.rowCount())
        try:
            clientes = self.repository.obtener_todos(filtro)
            for cliente in clientes:
                items = [
                    QStandardItem(getattr(cliente, "codigo_cliente", "") or ""),
                    QStandardItem(getattr(cliente, "cif_nif_siren", "") or ""),
                    QStandardItem(
                        getattr(cliente, "nombre_fiscal", "")
                        or (
                            cliente.nombre_completo()
                            if hasattr(cliente, "nombre_completo")
                            else ""
                        )
                    ),
                    QStandardItem(getattr(cliente, "telefono1", "") or ""),
                    QStandardItem(getattr(cliente, "email", "") or ""),
                ]
                # Guardar el ID del cliente en el primer item
                items[0].setData(cliente.id)

                for item in items:
                    item.setEditable(False)
                self.model.appendRow(items)
            self.data_changed.emit()
        except Exception as e:
            self.error_occurred.emit(f"No se pudieron cargar clientes: {e}")

    def obtener_cliente(self, id_: int) -> Optional[Cliente]:
        """Obtiene un cliente por ID."""
        try:
            cliente = self.repository.obtener_por_id(id_)
            if cliente:
                self.cliente_actual = cliente
                return cliente
            else:
                self.error_occurred.emit("Cliente no encontrado")
                return None
        except Exception as e:
            self.error_occurred.emit(f"Error al obtener cliente: {e}")
            return None

    def obtener_cliente_por_codigo(self, codigo: str) -> Optional[Cliente]:
        """Obtiene un cliente por su código."""
        try:
            cliente = self.repository.obtener_por_codigo(codigo)
            if cliente:
                self.cliente_actual = cliente
                return cliente
            return None
        except Exception as e:
            self.error_occurred.emit(f"Error al obtener cliente por código: {e}")
            return None

    def nuevo_cliente(self):
        """Prepara para un nuevo cliente."""
        self.cliente_actual = None

    def guardar_cliente(self, cliente: Cliente) -> Optional[Cliente]:
        """Guarda el cliente actual y devuelve el cliente guardado."""
        try:
            # Determinar si es creación o actualización
            if cliente.id:
                cliente_guardado = self.repository.actualizar(cliente)
                mensaje = "Cliente actualizado correctamente"
            else:
                cliente_guardado = self.repository.crear(cliente)
                mensaje = "Cliente creado correctamente"

            self.cliente_actual = cliente_guardado
            self.cargar_clientes()
            self.operation_success.emit(mensaje)
            return cliente_guardado
        except Exception as e:
            self.error_occurred.emit(f"Error al guardar: {e}")
            return None

    def borrar_cliente(self, id_: int) -> bool:
        """Borra un cliente por ID."""
        try:
            self.repository.eliminar(id_)
            self.cargar_clientes()
            self.operation_success.emit("Cliente eliminado correctamente")
            return True
        except Exception as e:
            self.error_occurred.emit(f"Error al borrar: {e}")
            return False

    def buscar_clientes(self, termino: str) -> List[Cliente]:
        """Busca clientes por término de búsqueda."""
        try:
            return self.repository.buscar(termino)
        except Exception as e:
            self.error_occurred.emit(f"Error al buscar: {e}")
            return []

    def obtener_paises(self) -> List[tuple]:
        """Obtiene la lista de países desde la base de datos paises_es_fr.sqlite."""
        try:
            # Ruta a la base de datos
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_path = os.path.join(base_dir, "datos", "paises_es_fr.sqlite")

            if not os.path.exists(db_path):
                self.error_occurred.emit(
                    f"Base de datos de países no encontrada: {db_path}"
                )
                return []

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT pais_es, pais_fr FROM paises ORDER BY pais_es")
            paises = cursor.fetchall()
            conn.close()

            return paises
        except Exception as e:
            self.error_occurred.emit(f"Error al cargar países: {e}")
            return []

    def buscar_poblacion_por_cp(self, cp: str, pais: str = "Francia"):
        """Busca poblaciones por código postal - DELEGADO AL REPOSITORY.

        Args:
            cp: Código postal a buscar
            pais: País (por defecto Francia)

        Returns:
            Tupla (resultados, db_path, db_config)
        """
        try:
            return self.repository.buscar_poblacion_por_cp(cp, pais)
        except Exception as e:
            self.error_occurred.emit(f"Error al buscar población: {e}")
            return [], "", None

    def buscar_cp_por_poblacion_simple(self, poblacion: str, pais: str = "Francia"):
        """Busca códigos postales por nombre de población - DELEGADO AL REPOSITORY.

        Args:
            poblacion: Nombre de la población a buscar
            pais: País (por defecto Francia)

        Returns:
            Tupla (resultados, db_path, db_config)
        """
        try:
            return self.repository.buscar_cp_por_poblacion(poblacion, pais)
        except Exception as e:
            self.error_occurred.emit(f"Error al buscar código postal: {e}")
            return [], "", None

    def obtener_cliente_en_posicion(self, posicion: int) -> Optional[Cliente]:
        """Obtiene el cliente en una posición específica del modelo."""
        try:
            if 0 <= posicion < self.model.rowCount():
                item = self.model.item(posicion, 0)
                if item:
                    cliente_id = item.data()
                    if cliente_id:
                        return self.obtener_cliente(cliente_id)
            return None
        except Exception as e:
            self.error_occurred.emit(f"Error al obtener cliente en posición: {e}")
            return None

    def obtener_posicion_cliente(self, cliente_id: int) -> int:
        """Obtiene la posición de un cliente en el modelo por su ID."""
        try:
            for row in range(self.model.rowCount()):
                item = self.model.item(row, 0)
                if item and item.data() == cliente_id:
                    return row
            return -1
        except Exception as e:
            self.error_occurred.emit(f"Error al obtener posición: {e}")
            return -1

    def buscar_poblacion_por_cp_alternativa(self, cp: str, pais: str = "Francia"):
        """Busca población por código postal para direcciones alternativas"""
        try:
            if len(cp) < 5:  # French postal codes are 5 digits
                return

            results = self.buscar_poblacion_por_cp(cp, pais)

            if len(results) == 1:
                # Single result - update view directly
                poblacion, provincia = results[0]
                # Usar método específico de la vista para direcciones alternativas
                if hasattr(self, "_view_reference"):
                    self._view_reference.actualizar_campos_alternativa(
                        poblacion=poblacion, provincia=provincia
                    )
            elif len(results) > 1:
                # Multiple results - show dialog through view
                self._show_selection_dialog_alternativa(results, cp, is_cp_search=True)
        except Exception as e:
            self.error_occurred.emit(f"Error al buscar población alternativa: {e}")

    def buscar_cp_por_poblacion_alternativa(
        self, poblacion: str, pais: str = "Francia"
    ):
        """Busca código postal por población para direcciones alternativas"""
        try:
            if len(poblacion) < 3:
                return

            results = self.buscar_cp_por_poblacion_simple(poblacion, pais)

            if len(results) == 1:
                # Single result - update view directly
                cp, poblacion_nombre, provincia = results[0]
                # Usar método específico de la vista para direcciones alternativas
                if hasattr(self, "_view_reference"):
                    self._view_reference.actualizar_campos_alternativa(
                        cp=cp, poblacion=poblacion_nombre, provincia=provincia
                    )
                else:
                    pass
            elif len(results) > 1:
                # Multiple results - show dialog through view
                self._show_selection_dialog_alternativa(
                    results, poblacion, is_cp_search=False
                )
            else:
                pass
        except Exception as e:
            self.error_occurred.emit(f"Error al buscar CP alternativo: {e}")

    def _show_selection_dialog_alternativa(
        self, results, search_term, is_cp_search=True
    ):
        """Delega mostrar diálogo de selección a la vista"""
        try:
            # La vista debe implementar este método para mostrar el diálogo
            if hasattr(self, "_view_reference"):
                self._view_reference.mostrar_dialogo_poblacion_alternativa(
                    results, search_term, is_cp_search
                )
        except Exception as e:
            self.error_occurred.emit(f"Error al mostrar diálogo alternativo: {e}")
