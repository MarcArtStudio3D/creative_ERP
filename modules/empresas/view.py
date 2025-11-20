from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QDialog,
    QDialogButtonBox, QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from app.views.ui_frmempresas import Ui_FrmEmpresas
from modules.empresas.repository import EmpresaRepository
from core.models import Empresa


class EmpresasView(QWidget):
    """Vista mínima para listar y editar empresas."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = EmpresaRepository()
        self._build_ui()
        self.cargar_empresas()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Botones de acciones
        btn_layout = QHBoxLayout()
        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_editar = QPushButton("Editar")
        self.btn_borrar = QPushButton("Borrar")
        self.btn_refrescar = QPushButton("Refrescar")

        btn_layout.addWidget(self.btn_nuevo)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_borrar)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_refrescar)

        layout.addLayout(btn_layout)

        # Tabla
        self.table = QTableView()
        self.model = QStandardItemModel(0, 5, self)
        self.model.setHorizontalHeaderLabels(["ID", "Código", "Nombre Fiscal", "CIF/NIF", "Población"])
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        layout.addWidget(self.table)

        # Conexiones
        self.btn_nuevo.clicked.connect(self.nuevo)
        self.btn_editar.clicked.connect(self.editar)
        self.btn_borrar.clicked.connect(self.borrar)
        self.btn_refrescar.clicked.connect(self.cargar_empresas)

    def cargar_empresas(self):
        self.model.removeRows(0, self.model.rowCount())
        try:
            empresas = self.repo.obtener_todos()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar empresas: {e}")
            return

        for row, e in enumerate(empresas):
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

        # Ajustar ancho
        try:
            self.table.resizeColumnsToContents()
        except Exception:
            pass

    def _get_selected_id(self) -> Optional[int]:
        sel = self.table.selectionModel()
        if not sel.hasSelection():
            return None
        idx = sel.currentIndex()
        try:
            return int(self.model.item(idx.row(), 0).text())
        except Exception:
            return None

    def nuevo(self):
        dlg = EmpresaFormDialog(parent=self)
        if dlg.exec() == QDialog.Accepted:
            empresa = dlg.get_empresa()
            try:
                self.repo.guardar(empresa)
                self.cargar_empresas()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al guardar: {e}")

    def editar(self):
        id_ = self._get_selected_id()
        if id_ is None:
            QMessageBox.information(self, "Selecciona", "Selecciona una empresa primero.")
            return
        empresa = self.repo.obtener_por_id(id_)
        if not empresa:
            QMessageBox.warning(self, "Error", "Empresa no encontrada")
            return
        dlg = EmpresaFormDialog(empresa=empresa, parent=self)
        if dlg.exec() == QDialog.Accepted:
            empresa = dlg.get_empresa()
            try:
                self.repo.guardar(empresa)
                self.cargar_empresas()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al guardar: {e}")

    def borrar(self):
        id_ = self._get_selected_id()
        if id_ is None:
            QMessageBox.information(self, "Selecciona", "Selecciona una empresa primero.")
            return
        empresa = self.repo.obtener_por_id(id_)
        if not empresa:
            QMessageBox.warning(self, "Error", "Empresa no encontrada")
            return
        reply = QMessageBox.question(self, "Confirmar", f"Borrar empresa {empresa.nombre_fiscal}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.repo.borrar(empresa)
                self.cargar_empresas()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al borrar: {e}")


class EmpresaFormDialog(QDialog):
    """Dialogo que utiliza Ui_FrmEmpresas para crear/editar una Empresa."""

    def __init__(self, empresa: Empresa = None, parent=None):
        super().__init__(parent)
        self.ui = Ui_FrmEmpresas()
        self.ui.setupUi(self)
        self.empresa = empresa
        self._map_from_model()

        # Botones estándar
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.ui.gridLayout_14.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def _map_from_model(self):
        if not self.empresa:
            return
        # Mapear campos existentes del modelo a los widgets del UI
        try:
            w = self.ui
            if hasattr(w, 'txtcodigo') and getattr(self.empresa, 'codigo_empresa', None) is not None:
                w.txtcodigo.setText(str(self.empresa.codigo_empresa))
            if hasattr(w, 'txtEmpresa'):
                w.txtEmpresa.setText(getattr(self.empresa, 'nombre_fiscal', '') or '')
            if hasattr(w, 'txtNombreComercial'):
                w.txtNombreComercial.setText(getattr(self.empresa, 'nombre_comercial', '') or '')
            if hasattr(w, 'txtcif'):
                w.txtcif.setText(getattr(self.empresa, 'cif_nif', '') or '')
            if hasattr(w, 'txtdireccion1'):
                w.txtdireccion1.setText(getattr(self.empresa, 'direccion', '') or '')
            if hasattr(w, 'txtcp'):
                w.txtcp.setText(getattr(self.empresa, 'cp', '') or '')
            if hasattr(w, 'txtpoblacion'):
                w.txtpoblacion.setText(getattr(self.empresa, 'poblacion', '') or '')
            if hasattr(w, 'txtprovincia'):
                w.txtprovincia.setText(getattr(self.empresa, 'provincia', '') or '')
            if hasattr(w, 'txttelefono1'):
                w.txttelefono1.setText(getattr(self.empresa, 'telefono', '') or '')
            if hasattr(w, 'txtcMail'):
                w.txtcMail.setText(getattr(self.empresa, 'email', '') or '')
            if hasattr(w, 'txtweb'):
                w.txtweb.setText(getattr(self.empresa, 'web', '') or '')
        except Exception:
            pass

    def get_empresa(self) -> Empresa:
        """Construye/actualiza un objeto Empresa desde el formulario."""
        if self.empresa is None:
            self.empresa = Empresa()
        w = self.ui
        try:
            if hasattr(w, 'txtcodigo'):
                self.empresa.codigo_empresa = w.txtcodigo.text()
            if hasattr(w, 'txtEmpresa'):
                self.empresa.nombre_fiscal = w.txtEmpresa.text()
            if hasattr(w, 'txtNombreComercial'):
                self.empresa.nombre_comercial = w.txtNombreComercial.text()
            if hasattr(w, 'txtcif'):
                self.empresa.cif_nif = w.txtcif.text()
            if hasattr(w, 'txtdireccion1'):
                self.empresa.direccion = w.txtdireccion1.text()
            if hasattr(w, 'txtcp'):
                self.empresa.cp = w.txtcp.text()
            if hasattr(w, 'txtpoblacion'):
                self.empresa.poblacion = w.txtpoblacion.text()
            if hasattr(w, 'txtprovincia'):
                self.empresa.provincia = w.txtprovincia.text()
            if hasattr(w, 'txttelefono1'):
                self.empresa.telefono = w.txttelefono1.text()
            if hasattr(w, 'txtcMail'):
                self.empresa.email = w.txtcMail.text()
            if hasattr(w, 'txtweb'):
                self.empresa.web = w.txtweb.text()
        except Exception:
            pass
        return self.empresa
