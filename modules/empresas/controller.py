from typing import Optional, List
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMessageBox

from modules.empresas.repository import EmpresaRepository
from core.models import Empresa


class EmpresasController(QObject):
    """Controlador para el módulo de Empresas."""
    
    # Señales para comunicar eventos a la vista
    data_changed = Signal()
    error_occurred = Signal(str)
    operation_success = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = EmpresaRepository()
        self.model = QStandardItemModel(0, 5)
        self.model.setHorizontalHeaderLabels(["ID", "Código", "Nombre Fiscal", "CIF/NIF", "Población"])
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
                    QStandardItem(str(e.id)),
                    QStandardItem(getattr(e, 'codigo_empresa', '') or ''),
                    QStandardItem(getattr(e, 'nombre_fiscal', '') or ''),
                    QStandardItem(getattr(e, 'cif_nif', '') or ''),
                    QStandardItem(getattr(e, 'poblacion', '') or ''),
                ]
                for it in items:
                    it.setEditable(False)
                self.model.appendRow(items)
            self.data_changed.emit()
        except Exception as e:
            self.error_occurred.emit(f"No se pudieron cargar empresas: {e}")

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
