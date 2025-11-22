from typing import Optional
from PySide6.QtWidgets import QWidget, QMessageBox, QTableView, QHeaderView
from PySide6.QtCore import Qt

from app.views.ui_frmempresas import Ui_FrmEmpresas
from modules.empresas.controller import EmpresasController
from core.models import Empresa


class EmpresasView(QWidget):
    """Vista de empresas integrada en la ventana principal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Instanciar controlador
        self.controller = EmpresasController(self)
        
        # Configurar UI
        self.ui = Ui_FrmEmpresas()
        self.ui.setupUi(self)
        
        # Configurar tabla
        self.ui.tableView.setModel(self.controller.model)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.ui.tableView.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Conectar señales de UI
        self.ui.tableView.doubleClicked.connect(self.editar)
        self.ui.btn_guardar_nuevo.clicked.connect(self.guardar)
        self.ui.btn_salir.clicked.connect(self.cancelar)
        # Conectar botón Descartar/Deshacer
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(self.deshacer)
        
        # Conectar señales del controlador
        self.controller.error_occurred.connect(self.mostrar_error)
        self.controller.operation_success.connect(self.mostrar_exito)
        
        # Cargar datos y mostrar lista
        self.controller.cargar_empresas()
        self.ui.stackedWidget.setCurrentIndex(1)  # Mostrar lista por defecto

    def mostrar_error(self, mensaje: str):
        QMessageBox.warning(self, "Error", mensaje)

    def mostrar_exito(self, mensaje: str):
        QMessageBox.information(self, "Éxito", mensaje)

    def _get_selected_id(self) -> Optional[int]:
        sel = self.ui.tableView.selectionModel()
        if not sel.hasSelection():
            return None
        idx = sel.currentIndex()
        try:
            # Usar el modelo del controlador
            return int(self.controller.model.item(idx.row(), 0).text())
        except Exception:
            return None

    def nuevo(self):
        """Prepara el formulario para una nueva empresa."""
        self.controller.nueva_empresa()
        self._limpiar_formulario()
        self.ui.stackedWidget.setCurrentIndex(0)  # Ir al formulario

    def editar(self):
        """Carga la empresa seleccionada en el formulario."""
        id_ = self._get_selected_id()
        if id_ is None:
            QMessageBox.information(self, "Selecciona", "Selecciona una empresa primero.")
            return
            
        empresa = self.controller.obtener_empresa(id_)
        if empresa:
            self._map_to_form(empresa)
            self.ui.stackedWidget.setCurrentIndex(0)  # Ir al formulario

    def borrar(self):
        """Borra la empresa seleccionada."""
        id_ = self._get_selected_id()
        if id_ is None:
            QMessageBox.information(self, "Selecciona", "Selecciona una empresa primero.")
            return
            
        # Obtener nombre para confirmación (opcional, requiere acceso al objeto)
        # Por simplicidad, preguntamos genéricamente o accedemos al modelo
        idx = self.ui.tableView.selectionModel().currentIndex()
        nombre = self.controller.model.item(idx.row(), 2).text()
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Borrar empresa {nombre}?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.borrar_empresa(id_)

    def guardar(self):
        """Guarda los cambios del formulario."""
        empresa = self._map_from_form()
        self.controller.guardar_empresa(empresa)
        # No volvemos al listado, nos quedamos en la ficha

    def deshacer(self):
        """Deshace los cambios recargando los datos de la empresa actual."""
        if self.controller.empresa_actual:
            self._map_to_form(self.controller.empresa_actual)
            QMessageBox.information(self, "Deshacer", "Cambios descartados. Datos recargados.")
        else:
            # Si es una nueva empresa, limpiamos el formulario
            self._limpiar_formulario()

    def cancelar(self):
        """Cancela la edición y vuelve a la lista."""
        self.ui.stackedWidget.setCurrentIndex(1)

    def accept(self):
        """Método requerido por Ui_FrmEmpresas (generado para QDialog)."""
        self.cancelar()

    def _limpiar_formulario(self):
        """Limpia los campos del formulario."""
        w = self.ui
        # Limpiar QLineEdits
        for widget_name in dir(w):
            widget = getattr(w, widget_name)
            if hasattr(widget, 'clear') and callable(widget.clear):
                if "txt" in widget_name or "lineEdit" in widget_name:
                    widget.clear()

    def _map_to_form(self, empresa: Empresa):
        """Rellena el formulario con los datos de la empresa."""
        w = self.ui
        try:
            if hasattr(w, 'txtcodigo') and getattr(empresa, 'codigo_empresa', None) is not None:
                w.txtcodigo.setText(str(empresa.codigo_empresa))
            if hasattr(w, 'txtEmpresa'):
                w.txtEmpresa.setText(getattr(empresa, 'nombre_fiscal', '') or '')
            if hasattr(w, 'txtNombreComercial'):
                w.txtNombreComercial.setText(getattr(empresa, 'nombre_comercial', '') or '')
            if hasattr(w, 'txtcif'):
                w.txtcif.setText(getattr(empresa, 'cif_nif', '') or '')
            if hasattr(w, 'txtdireccion1'):
                w.txtdireccion1.setText(getattr(empresa, 'direccion', '') or '')
            if hasattr(w, 'txtcp'):
                w.txtcp.setText(getattr(empresa, 'cp', '') or '')
            if hasattr(w, 'txtpoblacion'):
                w.txtpoblacion.setText(getattr(empresa, 'poblacion', '') or '')
            if hasattr(w, 'txtprovincia'):
                w.txtprovincia.setText(getattr(empresa, 'provincia', '') or '')
            if hasattr(w, 'txttelefono1'):
                w.txttelefono1.setText(getattr(empresa, 'telefono', '') or '')
            if hasattr(w, 'txtcMail'):
                w.txtcMail.setText(getattr(empresa, 'email', '') or '')
            if hasattr(w, 'txtweb'):
                w.txtweb.setText(getattr(empresa, 'web', '') or '')
        except Exception:
            pass

    def _map_from_form(self) -> Empresa:
        """Crea/Actualiza el objeto Empresa con los datos del formulario."""
        # Usar la empresa actual del controlador o crear una nueva
        if self.controller.empresa_actual is None:
            empresa = Empresa()
        else:
            empresa = self.controller.empresa_actual
            
        w = self.ui
        
        try:
            if hasattr(w, 'txtcodigo'):
                empresa.codigo_empresa = w.txtcodigo.text()
            if hasattr(w, 'txtEmpresa'):
                empresa.nombre_fiscal = w.txtEmpresa.text()
            if hasattr(w, 'txtNombreComercial'):
                empresa.nombre_comercial = w.txtNombreComercial.text()
            if hasattr(w, 'txtcif'):
                empresa.cif_nif = w.txtcif.text()
            if hasattr(w, 'txtdireccion1'):
                empresa.direccion = w.txtdireccion1.text()
            if hasattr(w, 'txtcp'):
                empresa.cp = w.txtcp.text()
            if hasattr(w, 'txtpoblacion'):
                empresa.poblacion = w.txtpoblacion.text()
            if hasattr(w, 'txtprovincia'):
                empresa.provincia = w.txtprovincia.text()
            if hasattr(w, 'txttelefono1'):
                empresa.telefono = w.txttelefono1.text()
            if hasattr(w, 'txtcMail'):
                empresa.email = w.txtcMail.text()
            if hasattr(w, 'txtweb'):
                empresa.web = w.txtweb.text()
        except Exception:
            pass
            
        return empresa
